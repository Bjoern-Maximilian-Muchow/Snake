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
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / ".station-runtime"
CPP_RUNTIME_DIR = RUNTIME_DIR / "level3"
CPP_RUNTIME_HEADER = CPP_RUNTIME_DIR / "student_bot.h"
LOCK_FILE = RUNTIME_DIR / "hardware.lock"
MAX_CODE_BYTES = 24_000
PYTHON_TIMEOUT_SECONDS = 12
BUILD_TIMEOUT_SECONDS = 90
UPLOAD_TIMEOUT_SECONDS = 60


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


def run_cpp(code: str, *, upload: bool, port: str) -> int:
    validate_cpp(code)
    CPP_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    with hardware_lock():
        CPP_RUNTIME_HEADER.write_text(code, encoding="utf-8")
        executable = platformio_executable()
        environment = os.environ.copy()
        environment["AUTOSNAKE_UPLOAD_PORT"] = port

        command = [executable, "run", "--environment", "uno-student"]
        if upload:
            command.extend(["--target", "upload", "--upload-port", port])

        print("AutoSnake Level 3: " + ("Build und Upload" if upload else "Build"), flush=True)
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
        print("ERGEBNIS: Firmware erfolgreich " + ("auf den Uno geladen." if upload else "gebaut."))
    else:
        print("ERGEBNIS: Build oder Upload fehlgeschlagen.")
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Begrenzter AutoSnake-Stationsrunner")
    parser.add_argument("mode", choices=("python", "cpp"))
    parser.add_argument("--base64", required=True, dest="encoded_code")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--port", default=os.environ.get("AUTOSNAKE_PORT", "COM3"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        code = decode_code(args.encoded_code)
        if args.mode == "python":
            return run_python(code)
        return run_cpp(code, upload=args.upload, port=args.port)
    except StationError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
