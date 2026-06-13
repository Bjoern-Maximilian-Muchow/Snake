from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "station" / "runner.py"
COMMAND_PATTERN = re.compile(
    r"^autosnake-run\s+(python|cpp)\s+([A-Za-z0-9+/=]+)"
    r"(?:\s+(--upload))?(?:\s+--port\s+(COM\d+))?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class StationCommand:
    mode: str
    encoded_code: str
    upload: bool
    port: str


def parse_station_command(line: str, default_port: str) -> StationCommand | None:
    match = COMMAND_PATTERN.fullmatch(line.strip())
    if not match:
        return None
    mode, encoded_code, upload_flag, port = match.groups()
    return StationCommand(
        mode=mode.lower(),
        encoded_code=encoded_code,
        upload=bool(upload_flag),
        port=(port or default_port).upper(),
    )


def create_app(default_port: str = "COM3") -> tuple[Flask, SocketIO]:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "autosnake-local-station"
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
    buffers: dict[str, str] = {}
    buffers_lock = Lock()

    def emit_output(session_id: str, output: str) -> None:
        socketio.emit("pty-output", {"output": output}, room=session_id, namespace="/pty")

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
        assert process.stdout is not None
        for line in process.stdout:
            emit_output(session_id, line.replace("\n", "\r\n"))
        return_code = process.wait()
        emit_output(session_id, f"\r\nProzess beendet: {return_code}\r\n")

    @app.get("/health")
    def health():
        return jsonify(status="ok", port=default_port)

    @socketio.on("connect", namespace="/pty")
    def connect():
        session_id = request.sid
        join_room(session_id, namespace="/pty")
        with buffers_lock:
            buffers[session_id] = ""
        emit_output(session_id, "AutoSnake-Station verbunden.\r\n")

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
