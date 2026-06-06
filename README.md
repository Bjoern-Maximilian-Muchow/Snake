# AutoSnake Remote Lab

AutoSnake Remote Lab is a remote laboratory for embedded systems education. Snake runs on a 16x16 RGB LED grid, and learners automate the game by writing bots instead of playing manually.

The project follows a simulation-first approach: until the physical LED grid and camera are available, the LED output and camera view are simulated in software. Later, the same architecture can be connected to an Arduino Uno R3, the real LED grid, and a camera pointed at the hardware.

The lab has exactly three difficulty levels:

- Schueler: simple rule-based control, no wall collision, rough food targeting.
- Student Anfang Studium: structured bot, field analysis, safe moves, optional simple BFS.
- Fortgeschrittener Student: robust pathfinding, safety checks, bounded runtime, and tests.

## Repository Structure

- `docs/`: architecture, remote-lab concept, and level descriptions.
- `firmware/arduino_uno/`: Arduino Uno R3 firmware skeleton with engine, bot interface, and LED output.
- `simulator/`: browser and Python simulators for hardware-independent development.
- `tests/`: pytest-based tests for the engine, bot interface, and example bots.
- `edrys/`: edrys-Lite laboratory, station, and task placeholders.
- `scripts/`: helper scripts for tests, simulator startup, and future flashing.

## Quick Start

Run tests:

```sh
./scripts/run_tests.sh
```

Start the web simulator:

```sh
./scripts/run_simulator.sh
```

Flash the Arduino later:

```sh
./scripts/flash_uno.sh
```

The flash script is currently a placeholder for a future Arduino CLI workflow.

## Edrys-Lite Integration

The edrys-Lite configuration lives in `edrys/laboratory.yaml`.

Raw configuration URL:

```text
https://raw.githubusercontent.com/Bjoern-Maximilian-Muchow/Snake/main/edrys/laboratory.yaml
```

Open the lab in edrys-Lite:

```text
https://edrys-labs.github.io/?/deploy/https://raw.githubusercontent.com/Bjoern-Maximilian-Muchow/Snake/main/edrys/laboratory.yaml
```

The web simulator is prepared for GitHub Pages:

```text
https://bjoern-maximilian-muchow.github.io/Snake/simulator/web/
```

Enable GitHub Pages for this repository before using the simulator URL in edrys-Lite.
