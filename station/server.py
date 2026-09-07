from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, join_room


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "station" / "runner.py"
COMMAND_PATTERN = re.compile(
    r"^autosnake-run\s+(python|cpp|rules)\s+([A-Za-z0-9+/=]+)"
    r"(?:\s+(--upload|--virtual))?(?:\s+--port\s+(COM\d+))?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class StationCommand:
    mode: str
    encoded_code: str
    upload: bool
    virtual: bool
    port: str


def parse_station_command(line: str, default_port: str) -> StationCommand | None:
    match = COMMAND_PATTERN.fullmatch(line.strip())
    if not match:
        return None
    mode, encoded_code, action, port = match.groups()
    if action == "--virtual" and mode.lower() not in {"python", "cpp", "rules"}:
        return None
    return StationCommand(
        mode=mode.lower(),
        encoded_code=encoded_code,
        upload=action == "--upload",
        virtual=action == "--virtual",
        port=(port or default_port).upper(),
    )


def create_app(default_port: str = "COM3") -> tuple[Flask, SocketIO]:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "autosnake-local-station"
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
    buffers: dict[str, str] = {}
    buffers_lock = Lock()
    active_virtual_processes: dict[str, subprocess.Popen] = {}
    processes_lock = Lock()
    last_monitor_output = ""

    def emit_output(session_id: str, output: str) -> None:
        socketio.emit("pty-output", {"output": output}, room=session_id, namespace="/pty")

    def emit_monitor(output: str) -> None:
        nonlocal last_monitor_output
        if output.startswith("AUTOSNAKE_MONITOR "):
            last_monitor_output = output
        socketio.emit("monitor-output", {"output": output}, namespace="/monitor")

    def execute(session_id: str, command: StationCommand) -> None:
        args = [
            sys.executable,
            str(RUNNER),
            command.mode,
            "--base64",
            command.encoded_code,
            "--port",
            command.port,
        ]
        if command.upload:
            args.append("--upload")
        if command.virtual:
            args.append("--virtual")

        emit_output(session_id, f"\r\nAutoSnake startet {command.mode.upper()} ...\r\n")
        process = subprocess.Popen(
            args,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if command.virtual:
            with processes_lock:
                active_virtual_processes[session_id] = process
        assert process.stdout is not None
        try:
            for line in process.stdout:
                emit_output(session_id, line.replace("\n", "\r\n"))
                if command.virtual:
                    emit_monitor(line)
            return_code = process.wait()
        finally:
            if command.virtual:
                with processes_lock:
                    active_virtual_processes.pop(session_id, None)
        emit_output(session_id, f"\r\nProzess beendet: {return_code}\r\n")
        if command.virtual:
            emit_monitor(f"AUTOSNAKE_STATUS beendet {return_code}\n")

    @app.get("/health")
    def health():
        return jsonify(status="ok", port=default_port)

    @app.get("/monitor")
    def monitor():
        return send_from_directory(str(ROOT / "simulator" / "web"), "arduino-monitor.html")

    @app.get("/arduino-monitor.css")
    def monitor_css():
        return send_from_directory(str(ROOT / "simulator" / "web"), "arduino-monitor.css")

    @app.get("/arduino-monitor.js")
    def monitor_js():
        return send_from_directory(str(ROOT / "simulator" / "web"), "arduino-monitor.js")

    @app.post("/virtual/stop")
    def stop_virtual():
        with processes_lock:
            processes = list(active_virtual_processes.values())
        stopped = 0
        for process in processes:
            if process.poll() is None:
                if sys.platform == "win32":
                    subprocess.run(
                        ["taskkill", "/T", "/F", "/PID", str(process.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False,
                    )
                else:
                    process.kill()
                stopped += 1
        emit_monitor("AUTOSNAKE_STATUS gestoppt\n")
        return jsonify(stopped=stopped, status="ok")

    @app.post("/virtual/rules")
    def start_virtual_rules():
        rules = request.get_json(silent=True)
        if not isinstance(rules, list):
            return jsonify(error="Regeln müssen als Liste übertragen werden."), 400
        encoded = base64.b64encode(json.dumps(rules).encode("utf-8")).decode("ascii")
        command = StationCommand(
            mode="rules",
            encoded_code=encoded,
            upload=False,
            virtual=True,
            port=default_port,
        )
        socketio.start_background_task(execute, "http", command)
        return jsonify(status="started")

    @app.after_request
    def allow_local_browser_access(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @socketio.on("connect", namespace="/pty")
    def connect():
        session_id = request.sid
        join_room(session_id, namespace="/pty")
        with buffers_lock:
            buffers[session_id] = ""
        emit_output(session_id, "AutoSnake-Station verbunden.\r\n")

    @socketio.on("connect", namespace="/monitor")
    def monitor_connect():
        emit_monitor("AUTOSNAKE_STATUS Monitor verbunden\n")
        if last_monitor_output:
            socketio.emit("monitor-output", {"output": last_monitor_output}, namespace="/monitor")

    @socketio.on("pty-input", namespace="/pty")
    def pty_input(data):
        session_id = request.sid
        incoming = str(data.get("input", "")).replace("\x03", "")
        with buffers_lock:
            buffer = buffers.get(session_id, "") + incoming
            lines = buffer.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            buffers[session_id] = lines.pop()

        for line in lines:
            if not line.strip():
                continue
            command = parse_station_command(line, default_port)
            if command is None:
                emit_output(session_id, "Befehl nicht erlaubt.\r\n")
                continue
            socketio.start_background_task(execute, session_id, command)

    @socketio.on("resize", namespace="/pty")
    def resize(_data):
        return None

    @socketio.on("disconnect", namespace="/pty")
    def disconnect():
        with buffers_lock:
            buffers.pop(request.sid, None)

    return app, socketio


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Windows-kompatible AutoSnake-Edrys-Station")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--arduino-port", default="COM3")
    args = parser.parse_args()

    app, socketio = create_app(args.arduino_port)
    socketio.run(app, host=args.host, port=args.port, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    main()
