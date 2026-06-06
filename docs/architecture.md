# Architecture

AutoSnake Remote Lab is split into small components so learners can develop and test bot logic before real hardware is available.

## Components

### Game Engine

The game engine owns the Snake state: grid size, snake body, food, direction, score, collisions, and step updates. It should stay as hardware-independent as possible so the same behavior can be mirrored in Arduino firmware, the browser simulator, and the Python test simulator.

### Bot Interface

The bot interface exposes a compact game snapshot and expects a move decision. On Arduino Uno, this interface must avoid dynamic allocation and large data copies. In the Python simulator, the same idea is represented with simple data classes and pure functions.

### LED Renderer

The LED renderer translates the abstract game state into pixels for a 16x16 RGB LED grid. During the simulation phase, the browser renderer replaces the physical LEDs.

### Simulator

The simulator has two parts:

- A web simulator that displays the 16x16 grid and acts as the first visual camera replacement.
- A Python simulator that can be used by tests and bot implementations without Arduino hardware.

### Tests

The tests validate movement, collisions, food behavior, bot outputs, and baseline level requirements. They run without Arduino hardware and provide quick feedback for learners and maintainers.

### Edrys-Lite Station

The edrys-Lite station will later connect the learner interface with the physical Arduino Uno R3, LED grid, camera stream, and code execution environment. For now, the station files document the intended integration points.

## Hardware Independence

The game engine should not depend directly on LED libraries, camera APIs, serial transport, or edrys-Lite details. Hardware-specific code belongs in renderer, station, or transport layers. This keeps the core logic testable and makes it easier to compare simulated and physical behavior.
