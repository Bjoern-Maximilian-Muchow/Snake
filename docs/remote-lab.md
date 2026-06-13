# Remote-Lab-Konzept

AutoSnake Remote Lab ist für Lernende gedacht, die aus der Ferne auf ein gemeinsam genutztes eingebettetes System zugreifen. Das physische Ziel ist ein Arduino Uno R3 mit einem 16x16 RGB-LED-Grid. Später beobachtet eine Kamera das Grid, damit Lernende das Ergebnis ihres Bots auf echter Hardware sehen können.

In der ersten Projektphase werden LED-Grid und Kamera simuliert. Der Browser-Simulator liefert die visuelle Grid-Ansicht, während der Python-Simulator automatisierte Tests und Algorithmenentwicklung unterstützt.

## Einzelstationsbetrieb

Das spätere physische Labor stellt nur einen Laborplatz bereit. Deshalb kann immer nur eine Person gleichzeitig aktiv an der realen Arduino-Station arbeiten. Mehrere Lernende können parallel mit Repository, Aufgaben, Tests und Simulator arbeiten, aber der Zugriff auf die Hardware muss nacheinander erfolgen.

Für den Unterricht bedeutet das:

- Der Simulator ist der Standardarbeitsplatz für alle.
- Die physische Station wird zeitlich zugeteilt.
- Vor dem Hardware-Zugriff sollen Tests lokal oder in GitHub Actions bestanden sein.
- Die Kameraansicht dient später als Nachweis, dass der Bot auf der echten LED-Matrix läuft.

## Geplanter Stationsablauf

1. Lernende lesen die Aufgabe in edrys-Lite.
2. Lernende entwickeln einen Snake-Bot gegen den Simulator.
3. Tests validieren Bot-Schnittstelle und Grundverhalten.
4. Später kann der Bot auf die Arduino-Station geflasht oder übertragen werden.
5. Die Station führt den Bot auf dem LED-Grid aus.
6. Ein Kamerastream zeigt das physische Ergebnis.

Die spätere Laboransicht soll Kamerabild und digitale Zustandsanzeige kombinieren. Damit können Lernende den erwarteten Engine-Zustand direkt mit der tatsächlichen LED-Ausgabe vergleichen.

## Spätere Stationsplattform

Stationsdienst, Tests, Arduino-Upload und Kamerastream sollen in Docker auf einem Raspberry Pi betrieben werden. Hardwarezugriffe werden über konfigurierbare Gerätepfade bereitgestellt; Windows `COM3` darf deshalb keine dauerhafte Plattformannahme werden. Details und offene Entscheidungen stehen in `docs/roadmap.md`.

## Entwurfsziele

- Game Engine deterministisch und testbar halten.
- Arduino-Firmware klein genug für die Speichergrenzen der Uno-Klasse halten.
- Einsteigerinnen und Einsteiger mit einfachen Regeln starten lassen.
- Fortgeschrittene Lernende an Pfadsuche, Sicherheitschecks, Laufzeitgrenzen und Tests arbeiten lassen.
