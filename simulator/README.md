# Simulator

Der Simulator ermöglicht AutoSnake-Entwicklung, bevor das physische LED-Grid und die Kamera verfügbar sind.

- `web/`: browserbasiertes visuelles 16x16 Grid mit Start/Pause, Einzelschritt, Level-Auswahl, Bot-Auswahl und Hindernissen ab Level 2. Es ersetzt zunächst die visuelle Kameraansicht.
- `python/`: deterministische Python-Game-Engine und Beispielbots, die von Tests verwendet werden. Die Engine kennt ebenfalls Hindernisse.

Web-Simulator aus dem Repository-Stamm starten:

```sh
./scripts/run_simulator.sh
```

Tests ausführen:

```sh
./scripts/run_tests.sh
```
