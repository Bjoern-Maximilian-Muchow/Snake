# Simulator

The simulator allows AutoSnake development before the physical LED grid and camera are available.

- `web/`: browser-based 16x16 visual grid. For now, this replaces the visual camera view.
- `python/`: deterministic Python game engine and example bots used by tests.

Start the web simulator from the repository root:

```sh
./scripts/run_simulator.sh
```

Run the tests:

```sh
./scripts/run_tests.sh
```
