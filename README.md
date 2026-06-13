# AutoSnake Remote Lab

AutoSnake Remote Lab ist ein Remote-Labor für eingebettete Systeme. Snake läuft auf einem 16x16 RGB-LED-Grid, und Lernende automatisieren das Spiel, indem sie Bots schreiben statt manuell zu steuern.

Das Projekt folgt einem simulationsorientierten Ansatz: Solange das physische LED-Grid und die Kamera noch nicht verfügbar sind, werden LED-Ausgabe und Kameraansicht in Software simuliert. Später kann dieselbe Architektur mit einem Arduino Uno R3, dem echten LED-Grid und einer auf die Hardware gerichteten Kamera verbunden werden.

Das Labor hat genau drei Schwierigkeitslevel:

- Schüler: einfache regelbasierte Steuerung, keine Wandkollision, Futter grob ansteuern.
- Student Anfang Studium: strukturierter Bot, Spielfeldanalyse, Hindernisse, sichere Züge, optional einfache BFS-Suche.
- Fortgeschrittener Student: robuste Pfadsuche mit Hindernissen, Sicherheitsprüfung, begrenzte Laufzeit und Tests.

Später steht genau ein physischer Laborplatz zur Verfügung. Mehrere Lernende können parallel im Simulator arbeiten, aber die reale Arduino-Station wird nacheinander genutzt.

Der Web-Simulator enthält Start/Pause, Einzelschritt, Reset, Bot-Auswahl und ab Level 2 feste Hindernisse auf dem Spielfeld.

Der Lernarbeitsplatz trennt drei Modi: Im Demo-Modus werden Referenzbots beobachtet, im Aufgabenmodus entstehen eigene Regeln oder eigener Code, und im Challenge-Modus wird eine unbekannte Situation bewertet. Level 1 besitzt einen ausführbaren Blockeditor; Level 2 und 3 nutzen getrennte Python- und C++-Arbeitsvorlagen unter `learning/`.

Eigene Bots werden in `simulator/python/student_bot.py` implementiert. Die feste Schnittstelle ist `choose_move(snapshot)` und wird durch Tests geprüft. Details stehen in `docs/student-bots.md`.

## Projektstruktur

- `docs/`: Architektur, Didaktik, Ausführungsweg, Remote-Lab-Konzept und Levelbeschreibungen.
- `firmware/arduino_uno/`: Firmware-Grundstruktur für den Arduino Uno R3 mit Engine, Bot-Schnittstelle und LED-Ausgabe.
- `simulator/`: Browser- und Python-Simulatoren für hardwareunabhängige Entwicklung.
- `tests/`: pytest-basierte Tests für Engine, Bot-Schnittstelle und Beispielbots.
- `edrys/`: edrys-Lite-Konfiguration, Stationshinweise und Aufgaben.
- `learning/`: absichtlich unvollständige Arbeitsvorlagen und Lernendentests für Level 2 und 3.
- `station/`: begrenzter Ausführungsdienst für Edrys, Python-Tests und exklusiven Arduino-Upload.
- `scripts/`: Hilfsskripte für Tests, Simulatorstart und späteres Flashen.

## Schnellstart

Tests ausführen:

```sh
./scripts/run_tests.sh
```

Web-Simulator starten:

```sh
./scripts/run_simulator.sh
```

Arduino später flashen:

```sh
./scripts/flash_uno.sh
```

Die Arduino-Firmware nutzt keine externen Bibliotheken. Sie enthält die drei Bot-Stufen, Hindernisse ab Level 2 sowie eine Live-Statistik für Bot-, Engine- und Renderzeit, Rechenlast und freien RAM. Das Repository enthält eine `platformio.ini` für Build, Upload auf `COM3` und den seriellen Monitor. Unter Windows kann alternativ `.\scripts\monitor_uno.ps1 -Port COM3` verwendet werden.

Ein automatisierter Hardwarevergleich der drei Level ist mit `scripts/sample_uno.py` möglich. GitHub Actions kompiliert neben den Python-Tests auch die Uno-Firmware über PlatformIO.

## Edrys-Lite-Integration

Die edrys-Lite-Konfiguration liegt in `edrys/laboratory.yaml`.

Raw-Konfigurations-URL:

```text
https://raw.githubusercontent.com/Bjoern-Maximilian-Muchow/Snake/main/edrys/laboratory.yaml
```

Labor in edrys-Lite öffnen:

```text
https://edrys-labs.github.io/?/deploy/https://raw.githubusercontent.com/Bjoern-Maximilian-Muchow/Snake/main/edrys/laboratory.yaml
```

Der Web-Simulator ist für GitHub Pages vorbereitet:

```text
https://bjoern-maximilian-muchow.github.io/Snake/simulator/web/
```

Aktiviere GitHub Pages für dieses Repository, bevor du die Simulator-URL in edrys-Lite verwendest.

Die physische Station wird auf dem Arduino-Laptop gestartet:

```powershell
.\scripts\setup_station.ps1
.\scripts\start_station.ps1 -ArduinoPort COM3
```

Danach den Edrys-Raum auf demselben Laptop in der Rolle **Station** öffnen. Details stehen in `station/README.md`.
