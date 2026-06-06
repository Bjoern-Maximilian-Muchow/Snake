# AutoSnake Remote Lab

AutoSnake Remote Lab ist ein Remote-Labor für eingebettete Systeme. Snake läuft auf einem 16x16 RGB-LED-Grid, und Lernende automatisieren das Spiel, indem sie Bots schreiben statt manuell zu steuern.

Das Projekt folgt einem simulationsorientierten Ansatz: Solange das physische LED-Grid und die Kamera noch nicht verfügbar sind, werden LED-Ausgabe und Kameraansicht in Software simuliert. Später kann dieselbe Architektur mit einem Arduino Uno R3, dem echten LED-Grid und einer auf die Hardware gerichteten Kamera verbunden werden.

Das Labor hat genau drei Schwierigkeitslevel:

- Schüler: einfache regelbasierte Steuerung, keine Wandkollision, Futter grob ansteuern.
- Student Anfang Studium: strukturierter Bot, Spielfeldanalyse, sichere Züge, optional einfache BFS-Suche.
- Fortgeschrittener Student: robuste Pfadsuche, Sicherheitsprüfung, begrenzte Laufzeit und Tests.

Später steht genau ein physischer Laborplatz zur Verfügung. Mehrere Lernende können parallel im Simulator arbeiten, aber die reale Arduino-Station wird nacheinander genutzt.

## Projektstruktur

- `docs/`: Architektur, Remote-Lab-Konzept und Levelbeschreibungen.
- `firmware/arduino_uno/`: Firmware-Grundstruktur für den Arduino Uno R3 mit Engine, Bot-Schnittstelle und LED-Ausgabe.
- `simulator/`: Browser- und Python-Simulatoren für hardwareunabhängige Entwicklung.
- `tests/`: pytest-basierte Tests für Engine, Bot-Schnittstelle und Beispielbots.
- `edrys/`: edrys-Lite-Konfiguration, Stationshinweise und Aufgaben.
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

Das Flash-Skript ist aktuell ein Platzhalter für einen späteren Arduino-CLI-Workflow.

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
