# Remote Lab Concept

AutoSnake Remote Lab is designed for learners who access a shared embedded system remotely. The physical target is an Arduino Uno R3 connected to a 16x16 RGB LED grid. A camera will later observe the grid so learners can see the result of their bot on real hardware.

During the first project phase, the LED grid and camera are simulated. The browser simulator provides the visual grid, while the Python simulator supports automated tests and algorithm development.

## Planned Station Flow

1. Learner reads the task in edrys-Lite.
2. Learner develops a Snake bot against the simulator.
3. Tests validate the bot interface and basic behavior.
4. Later, the bot can be flashed or transferred to the Arduino station.
5. The station runs the bot on the LED grid.
6. A camera stream shows the physical result.

## Design Goals

- Keep the game engine deterministic and testable.
- Keep Arduino firmware small enough for Uno-class memory limits.
- Let beginners start with simple rules.
- Let advanced learners work on pathfinding, safety checks, runtime limits, and tests.
