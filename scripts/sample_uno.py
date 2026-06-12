from __future__ import annotations

import argparse
import time

import serial


def wait_for_level(port: serial.Serial, level: int, timeout: float = 6.0) -> str:
    deadline = time.time() + timeout
    prefix = f"level={level} "
    while time.time() < deadline:
        line = port.readline().decode(errors="replace").strip()
        if line.startswith(prefix):
            return line
    return "TIMEOUT"


def main() -> None:
    parser = argparse.ArgumentParser(description="Vergleicht die AutoSnake-Level auf dem Uno.")
    parser.add_argument("--port", default="COM3")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()

    with serial.Serial(args.port, args.baud, timeout=1) as port:
        time.sleep(2)
        for level in (1, 2, 3):
            port.write(str(level).encode("ascii"))
            print(f"LEVEL{level} {wait_for_level(port, level)}")


if __name__ == "__main__":
    main()
