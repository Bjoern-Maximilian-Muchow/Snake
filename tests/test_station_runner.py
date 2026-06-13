from __future__ import annotations

import base64

import pytest

from station import runner


def station_server_module():
    return pytest.importorskip("station.server", reason="Stationsabhängigkeiten sind optional")


WORKING_PYTHON_BOT = """\
from autosnake_sim import BotSnapshot, DELTAS, Direction, OPPOSITES, Point


def is_blocked(snapshot: BotSnapshot, point: Point) -> bool:
    return not (0 <= point.x < 16 and 0 <= point.y < 16) or point in snapshot.snake or point in snapshot.obstacles


def safe_moves(snapshot: BotSnapshot) -> list[Direction]:
    result = []
    for move in Direction:
        if move == OPPOSITES[snapshot.direction]:
            continue
        dx, dy = DELTAS[move]
        point = Point(snapshot.head.x + dx, snapshot.head.y + dy)
        if not is_blocked(snapshot, point):
            result.append(move)
    return result


def choose_move(snapshot: BotSnapshot) -> Direction:
    moves = safe_moves(snapshot)
    return moves[0] if moves else snapshot.direction
"""


def test_decode_code_accepts_utf8_base64():
    encoded = base64.b64encode("Grüße vom Bot".encode()).decode()

    assert runner.decode_code(encoded) == "Grüße vom Bot"


def test_decode_code_rejects_invalid_input():
    with pytest.raises(runner.StationError):
        runner.decode_code("kein base64!")


def test_python_validation_rejects_station_access():
    with pytest.raises(runner.StationError, match="Importe"):
        runner.validate_python("import os\nos.system('whoami')")

    with pytest.raises(runner.StationError, match="aufruf"):
        runner.validate_python("def choose_move(snapshot):\n    return open('secret.txt').read()")


def test_cpp_validation_rejects_dynamic_allocation():
    code = '#include "bot_interface.h"\nDirection chooseStudentMove() { return *new Direction; }'

    with pytest.raises(runner.StationError, match="Speicherallokation"):
        runner.validate_cpp(code)


def test_cpp_validation_rejects_additional_includes():
    code = '#include "bot_interface.h"\n#include <fstream>\nDirection chooseStudentMove() { return UP; }'

    with pytest.raises(runner.StationError, match="bot_interface.h"):
        runner.validate_cpp(code)


def test_python_submission_runs_in_temporary_workspace():
    assert runner.run_python(WORKING_PYTHON_BOT) == 0


def test_station_server_accepts_only_fixed_commands():
    parse_station_command = station_server_module().parse_station_command
    encoded = base64.b64encode(b"code").decode()

    command = parse_station_command(f"autosnake-run cpp {encoded} --upload --port COM3", "COM4")
    assert command is not None
    assert command.mode == "cpp"
    assert command.upload
    assert command.port == "COM3"
    assert parse_station_command("Get-ChildItem", "COM3") is None


def test_station_health_endpoint_reports_arduino_port():
    create_app = station_server_module().create_app
    app, _socketio = create_app("COM7")

    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"port": "COM7", "status": "ok"}
