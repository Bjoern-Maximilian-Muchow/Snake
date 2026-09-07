from __future__ import annotations

import argparse
import ast
import base64
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import json
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / ".station-runtime"
CPP_RUNTIME_DIR = RUNTIME_DIR / "level3"
CPP_RUNTIME_HEADER = CPP_RUNTIME_DIR / "student_bot.h"
RULE_RUNTIME_DIR = RUNTIME_DIR / "level1"
RULE_RUNTIME_HEADER = RULE_RUNTIME_DIR / "student_bot.h"
LOCK_FILE = RUNTIME_DIR / "hardware.lock"
MAX_CODE_BYTES = 24_000
PYTHON_TIMEOUT_SECONDS = 12
BUILD_TIMEOUT_SECONDS = 90
UPLOAD_TIMEOUT_SECONDS = 60
VIRTUAL_TIMEOUT_SECONDS = 30
UNO_RAM_BYTES = 2048
UNO_FLASH_BYTES = 32256


class StationError(RuntimeError):
    pass


FORBIDDEN_PYTHON_NODES = (
    ast.AsyncFunctionDef,
    ast.Await,
    ast.ClassDef,
    ast.Global,
    ast.Nonlocal,
    ast.With,
    ast.AsyncWith,
    ast.Yield,
    ast.YieldFrom,
)
SAFE_PYTHON_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "dict",
    "enumerate",
    "float",
    "int",
    "len",
    "list",
    "max",
    "min",
    "range",
    "reversed",
    "set",
    "sorted",
    "sum",
    "tuple",
    "zip",
}
SAFE_METHODS = {
    "add",
    "append",
    "copy",
    "count",
    "discard",
    "get",
    "index",
    "items",
    "keys",
    "pop",
    "remove",
    "values",
}


def decode_code(value: str) -> str:
    try:
        raw = base64.b64decode(value, validate=True)
    except (ValueError, TypeError) as exc:
        raise StationError("Der übertragene Code ist nicht gültig kodiert.") from exc

    if len(raw) > MAX_CODE_BYTES:
        raise StationError(f"Der Code ist größer als {MAX_CODE_BYTES} Byte.")

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StationError("Der Code muss UTF-8-Text sein.") from exc


def run_command(command: list[str], *, cwd: Path, timeout: int) -> int:
    print("$ " + " ".join(command), flush=True)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        if exc.stdout:
            print(exc.stdout, end="")
        raise StationError(f"Zeitlimit von {timeout} Sekunden überschritten.") from exc

    print(result.stdout, end="")
    return result.returncode


def validate_python(code: str) -> None:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise StationError(f"Python-Syntaxfehler in Zeile {exc.lineno}: {exc.msg}") from exc

    imported_names: set[str] = set()
    function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_PYTHON_NODES):
            raise StationError(f"Python-Konstrukt nicht erlaubt: {type(node).__name__}")
        if isinstance(node, ast.Import):
            raise StationError("Direkte Python-Importe sind nicht erlaubt.")
        if isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue
            if node.module != "autosnake_sim":
                raise StationError("Es dürfen nur Namen aus autosnake_sim importiert werden.")
            imported_names.update(alias.asname or alias.name for alias in node.names)
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise StationError("Dunder-Zugriffe sind nicht erlaubt.")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise StationError("Dunder-Namen sind nicht erlaubt.")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                allowed_names = SAFE_PYTHON_BUILTINS | imported_names | function_names
                if node.func.id not in allowed_names:
                    raise StationError(f"Funktionsaufruf nicht erlaubt: {node.func.id}")
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in SAFE_METHODS:
                    raise StationError(f"Methodenaufruf nicht erlaubt: {node.func.attr}")
            else:
                raise StationError("Dynamische Funktionsaufrufe sind nicht erlaubt.")


def run_python(code: str) -> int:
    validate_python(code)
    print("AutoSnake Level 2: Python-Tests", flush=True)
    with tempfile.TemporaryDirectory(prefix="autosnake-python-") as temp_name:
        workspace = Path(temp_name)
        learning_dir = workspace / "learning" / "level2"
        simulator_dir = workspace / "simulator" / "python"
        learning_dir.mkdir(parents=True)
        simulator_dir.mkdir(parents=True)

        shutil.copy2(ROOT / "learning" / "level2" / "test_student_bot.py", learning_dir)
        shutil.copy2(ROOT / "simulator" / "python" / "autosnake_sim.py", simulator_dir)
        (learning_dir / "student_bot.py").write_text(code, encoding="utf-8")

        return_code = run_command(
            [sys.executable, "-m", "pytest", "-q", "learning/level2/test_student_bot.py"],
            cwd=workspace,
            timeout=PYTHON_TIMEOUT_SECONDS,
        )

    if return_code == 0:
        print("ERGEBNIS: Alle Level-2-Tests sind bestanden.")
    else:
        print("ERGEBNIS: Die Lösung ist noch nicht vollständig.")
    return return_code


def run_python_virtual(code: str) -> int:
    validate_python(code)
    sys.path.insert(0, str(ROOT / "simulator" / "python"))
    from autosnake_sim import BotSnapshot, Direction, Point

    namespace = {"__name__": "student_bot"}
    try:
        exec(compile(code, "student_bot.py", "exec"), namespace)
    except Exception as exc:
        raise StationError(f"Python-Bot konnte nicht geladen werden: {exc}") from exc
    choose_move = namespace.get("choose_move")
    if not callable(choose_move):
        raise StationError("Python-Bot enthält keine Funktion choose_move.")

    executable = platformio_executable()
    build_result = subprocess.run(
        [executable, "run", "--environment", "virtual-python"],
        cwd=ROOT,
        timeout=BUILD_TIMEOUT_SECONDS,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    print(build_result.stdout, end="")
    if build_result.returncode != 0:
        return build_result.returncode

    program = ROOT / ".pio" / "build" / "virtual-python" / ("program.exe" if sys.platform == "win32" else "program")
    if not program.exists():
        raise StationError("Das virtuelle Python-Arduino-Programm wurde nicht gefunden.")

    process = subprocess.Popen(
        [str(program)],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    assert process.stdout is not None and process.stdin is not None
    try:
        for line in process.stdout:
            print(line, end="")
            if not line.startswith("AUTOSNAKE_REQUEST "):
                continue
            try:
                payload = json.loads(line[len("AUTOSNAKE_REQUEST "):])
                body = [unpack_point(value) for value in payload["body"]]
                obstacles = list(bitset_points(payload["obstacles"]))
                snapshot = BotSnapshot(
                    head=Point(*payload["head"]),
                    food=Point(*payload["food"]),
                    direction=Direction(["up", "right", "down", "left"][payload["direction"]]),
                    snake=tuple(body),
                    obstacles=tuple(obstacles),
                    score=payload["score"],
                )
                move = choose_move(snapshot)
                if not isinstance(move, Direction):
                    move = Direction(move)
                process.stdin.write(f"AUTOSNAKE_MOVE {[Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT].index(move)}\n")
                process.stdin.flush()
            except Exception as exc:
                raise StationError(f"Python-Bot konnte keinen Zug liefern: {exc}") from exc
        return_code = process.wait(timeout=VIRTUAL_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        process.kill()
        raise StationError("Virtueller Python-Arduino-Lauf hat das Zeitlimit überschritten.") from exc
    finally:
        if process.poll() is None:
            process.kill()
    print("ERGEBNIS: Virtueller Python-Arduino erfolgreich beendet." if return_code == 0 else "ERGEBNIS: Virtueller Python-Arduino fehlgeschlagen.")
    return return_code


def unpack_point(value: int):
    from autosnake_sim import Point
    return Point(value & 0x0F, value >> 4)


def bitset_points(values: list[int]):
    from autosnake_sim import Point
    for index, value in enumerate(values):
        for bit in range(8):
            if value & (1 << bit):
                packed = index * 8 + bit
                yield Point(packed & 0x0F, packed >> 4)


def validate_cpp(code: str) -> None:
    required = ("chooseStudentMove", "#include", "return")
    forbidden = ("malloc(", "calloc(", "realloc(", "free(", "new ", "delete ")

    missing = [token for token in required if token not in code]
    used_forbidden = [token.strip() for token in forbidden if token in code]
    if missing:
        raise StationError("C++-Schnittstelle unvollständig: " + ", ".join(missing))
    if used_forbidden:
        raise StationError(
            "Dynamische Speicherallokation ist auf dem Uno nicht erlaubt: "
            + ", ".join(used_forbidden)
        )

    includes = re.findall(r"^\s*#\s*include\s*([<\"][^>\"]+[>\"])", code, re.MULTILINE)
    if any(include != '"bot_interface.h"' for include in includes):
        raise StationError("Es darf nur bot_interface.h eingebunden werden.")


RULE_CONDITIONS = {"food_right", "food_left", "food_down", "food_up", "front_blocked", "left_free", "right_free", "always"}
RULE_ACTIONS = {"right", "left", "down", "up", "forward", "turn_left", "turn_right"}


def decode_rules(value: str) -> list[dict[str, str]]:
    try:
        decoded = decode_code(value)
        rules = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise StationError("Die Level-1-Regeln sind kein gültiges JSON.") from exc
    if not isinstance(rules, list) or not 1 <= len(rules) <= 8:
        raise StationError("Level 1 benötigt 1 bis 8 Regeln.")
    validated = []
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("condition") not in RULE_CONDITIONS or rule.get("action") not in RULE_ACTIONS:
            raise StationError("Ungültige Bedingung oder Aktion in den Level-1-Regeln.")
        validated.append({"condition": rule["condition"], "action": rule["action"]})
    return validated


def generate_rule_bot(rules: list[dict[str, str]]) -> str:
    conditions = {
        "food_right": "snapshot.food.x > snapshot.head.x",
        "food_left": "snapshot.food.x < snapshot.head.x",
        "food_down": "snapshot.food.y > snapshot.head.y",
        "food_up": "snapshot.food.y < snapshot.head.y",
        "front_blocked": "snapshotBlocked(snapshot, movedPoint(snapshot.head, snapshot.currentDirection))",
        "left_free": "!snapshotBlocked(snapshot, movedPoint(snapshot.head, turnLeft(snapshot.currentDirection)))",
        "right_free": "!snapshotBlocked(snapshot, movedPoint(snapshot.head, turnRight(snapshot.currentDirection)))",
        "always": "true",
    }
    actions = {
        "right": "DIR_RIGHT", "left": "DIR_LEFT", "down": "DIR_DOWN", "up": "DIR_UP",
        "forward": "snapshot.currentDirection",
        "turn_left": "turnLeft(snapshot.currentDirection)",
        "turn_right": "turnRight(snapshot.currentDirection)",
    }
    checks = "\n".join(
        f"  if ({conditions[rule['condition']]}) return {actions[rule['action']]};"
        for rule in rules
    )
    return f'''#ifndef AUTOSNAKE_STUDENT_BOT_H
#define AUTOSNAKE_STUDENT_BOT_H

#include "bot_interface.h"

inline Direction turnLeft(Direction direction) {{
  return static_cast<Direction>((static_cast<uint8_t>(direction) + 3) % 4);
}}

inline Direction turnRight(Direction direction) {{
  return static_cast<Direction>((static_cast<uint8_t>(direction) + 1) % 4);
}}

inline Direction chooseStudentMove(const BotSnapshot& snapshot) {{
{checks}
  return snapshot.currentDirection;
}}

#endif
'''


def run_virtual_environment(environment_name: str) -> int:
    executable = platformio_executable()
    build_result = subprocess.run(
        [executable, "run", "--environment", environment_name],
        cwd=ROOT,
        timeout=BUILD_TIMEOUT_SECONDS,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    print(build_result.stdout, end="")
    if build_result.returncode != 0:
        return build_result.returncode
    program = ROOT / ".pio" / "build" / environment_name / ("program.exe" if sys.platform == "win32" else "program")
    if not program.exists():
        raise StationError("Das virtuelle Arduino-Programm wurde nicht gefunden.")
    return run_command([str(program)], cwd=ROOT, timeout=VIRTUAL_TIMEOUT_SECONDS)


def run_rules(encoded_rules: str) -> int:
    rules = decode_rules(encoded_rules)
    RULE_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    with hardware_lock():
        RULE_RUNTIME_HEADER.write_text(generate_rule_bot(rules), encoding="utf-8")
        check_uno_budget("uno-rules")
        print("AutoSnake Level 1: Virtuellen Arduino starten", flush=True)
        return_code = run_virtual_environment("virtual-rules")
    print("ERGEBNIS: Virtueller Regelbot erfolgreich beendet." if return_code == 0 else "ERGEBNIS: Virtueller Regelbot fehlgeschlagen.")
    return return_code


def platformio_executable() -> str:
    configured = os.environ.get("AUTOSNAKE_PLATFORMIO")
    candidates = [
        configured,
        shutil.which("platformio"),
        shutil.which("pio"),
        str(Path.home() / ".platformio" / "penv" / "Scripts" / "platformio.exe"),
        str(Path.home() / ".platformio" / "penv" / "bin" / "platformio"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise StationError("PlatformIO wurde nicht gefunden.")


def check_uno_budget(environment_name: str) -> None:
    result = subprocess.run(
        [platformio_executable(), "run", "--environment", environment_name],
        cwd=ROOT,
        timeout=BUILD_TIMEOUT_SECONDS,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        raise StationError("Uno-Budget-Build fehlgeschlagen.")
    ram_match = re.search(r"RAM:.*?\(.*?(\d+) bytes from (\d+) bytes\)", result.stdout)
    flash_match = re.search(r"Flash:.*?\(.*?(\d+) bytes from (\d+) bytes\)", result.stdout)
    if not ram_match or not flash_match:
        raise StationError("PlatformIO-Speicherwerte konnten nicht gelesen werden.")
    ram_used, ram_total = map(int, ram_match.groups())
    flash_used, flash_total = map(int, flash_match.groups())
    if ram_used > UNO_RAM_BYTES or flash_used > UNO_FLASH_BYTES:
        raise StationError(
            f"Arduino-Budget überschritten: RAM {ram_used}/{ram_total}, Flash {flash_used}/{flash_total}."
        )


@contextmanager
def hardware_lock():
    RUNTIME_DIR.mkdir(exist_ok=True)
    try:
        descriptor = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise StationError("Die Arduino-Station wird gerade von einer anderen Ausführung benutzt.") from exc

    try:
        with os.fdopen(descriptor, "w", encoding="ascii") as lock:
            lock.write(f"pid={os.getpid()} time={time.time()}\n")
        yield
    finally:
        LOCK_FILE.unlink(missing_ok=True)


def run_cpp(code: str, *, upload: bool, port: str, virtual_run: bool = False, strict: bool = False) -> int:
    validate_cpp(code)
    CPP_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    with hardware_lock():
        CPP_RUNTIME_HEADER.write_text(code, encoding="utf-8")
        if virtual_run or strict:
            check_uno_budget("uno-student")
        executable = platformio_executable()
        environment_name = "virtual-student" if virtual_run else "uno-student"
        environment = os.environ.copy()
        environment["AUTOSNAKE_UPLOAD_PORT"] = port

        command = [executable, "run", "--environment", environment_name]
        if upload:
            command.extend(["--target", "upload", "--upload-port", port])

        if upload and virtual_run:
            raise StationError("Virtueller Arduino kann nicht hochgeladen werden.")

        action = "Virtueller Build" if virtual_run else ("Build und Upload" if upload else "Build")
        print("AutoSnake Level 3: " + action, flush=True)
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                timeout=UPLOAD_TIMEOUT_SECONDS if upload else BUILD_TIMEOUT_SECONDS,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                env=environment,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            if exc.stdout:
                print(exc.stdout, end="")
            raise StationError("PlatformIO hat das Zeitlimit überschritten.") from exc

        print(result.stdout, end="")

    if result.returncode == 0:
        if strict:
            hex_path = ROOT / ".pio" / "build" / "uno-student" / "firmware.hex"
            print("AutoSnake Level 3: Strikte AVR-Simulation starten", flush=True)
            return run_command(
                ["node", str(ROOT / "scripts" / "run_avr_simulator.js"), str(hex_path), "16000000"],
                cwd=ROOT,
                timeout=VIRTUAL_TIMEOUT_SECONDS,
            )
        if virtual_run:
            program_candidates = [
                ROOT / ".pio" / "build" / environment_name / "program.exe",
                ROOT / ".pio" / "build" / environment_name / "program",
            ]
            program = next((candidate for candidate in program_candidates if candidate.exists()), None)
            if program is None:
                raise StationError("Das virtuelle Arduino-Programm wurde nicht gefunden.")
            print("AutoSnake Level 3: Virtuellen Arduino starten", flush=True)
            return_code = run_command(
                [str(program)],
                cwd=ROOT,
                timeout=VIRTUAL_TIMEOUT_SECONDS,
            )
            print("ERGEBNIS: Virtueller Arduino erfolgreich beendet." if return_code == 0 else "ERGEBNIS: Virtueller Arduino fehlgeschlagen.")
            return return_code
        print("ERGEBNIS: Firmware erfolgreich " + ("auf den Uno geladen." if upload else "gebaut."))
    else:
        print("ERGEBNIS: Build oder Upload fehlgeschlagen.")
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Begrenzter AutoSnake-Stationsrunner")
    parser.add_argument("mode", choices=("python", "cpp", "rules"))
    parser.add_argument("--base64", required=True, dest="encoded_code")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--virtual", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--port", default=os.environ.get("AUTOSNAKE_PORT", "COM3"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        code = decode_code(args.encoded_code)
        if args.mode == "python" and args.virtual:
            return run_python_virtual(code)
        if args.mode == "python":
            return run_python(code)
        if args.mode == "rules":
            return run_rules(args.encoded_code)
        return run_cpp(code, upload=args.upload, port=args.port, virtual_run=args.virtual, strict=args.strict)
    except StationError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
