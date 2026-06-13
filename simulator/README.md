# Simulator

Der Simulator ermöglicht AutoSnake-Entwicklung, bevor das physische LED-Grid und die Kamera verfügbar sind.

- `web/`: browserbasiertes visuelles 16x16 Grid mit Start/Pause, Einzelschritt, Level-Auswahl, Bot-Auswahl und Hindernissen ab Level 2. Es ersetzt zunächst die visuelle Kameraansicht.
- `python/`: deterministische Python-Game-Engine und Beispielbots, die von Tests verwendet werden. Die Engine kennt ebenfalls Hindernisse.
- `python/student_bot.py`: Vorlage und Einstiegspunkt für eigene Bots der Lernenden.

Web-Simulator aus dem Repository-Stamm starten:

```sh
./scripts/run_simulator.sh
```

Lernphasen können direkt verlinkt werden, zum Beispiel:

```text
http://localhost:8000/?mode=assignment&level=1
http://localhost:8000/?mode=challenge&level=1
```

Mit `lockLevel=1`, `lockLevel=2` oder `lockLevel=3` wird der Level-Wähler für einen edrys-Raum gesperrt:

```text
http://localhost:8000/?mode=assignment&level=2&lockLevel=2
```

Mit `lockMode=demo` wird zusätzlich die Modusauswahl ausgeblendet. Dies wird für die reine Demoansicht in der Lobby genutzt.

Tests ausführen:

```sh
./scripts/run_tests.sh
```

Eigene Bot-Logik wird hier implementiert:

```text
simulator/python/student_bot.py
```
