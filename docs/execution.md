# Ausführung der Lernaufgaben

## Level 1

Der Blockeditor läuft vollständig im Browser. Regelblöcke werden in eine geordnete Entscheidungsstruktur übersetzt und direkt vom Web-Simulator ausgeführt. Referenzbots stehen ausschließlich im Demo-Modus zur Verfügung.

## Level 2

Python-Code wird in `learning/level2/student_bot.py` entwickelt. Die absichtlich unvollständige Vorlage wird mit folgendem Befehl geprüft:

```sh
python -m pytest learning/level2/test_student_bot.py
```

Die reguläre CI-Suite sammelt diese Tests nicht ein, weil die Lernvorlage zu Beginn bewusst rot sein soll.

## Level 3

Der C++-Arbeitsstand wird über eine eigene PlatformIO-Umgebung gebaut:

```sh
platformio run --environment uno-student
```

Mit `AUTOSNAKE_STUDENT_BOT` bindet die Firmware `learning/level3/student_bot.h` statt der Referenzbots ein. Dadurch werden exakt dieselbe Engine, Telemetrie und Hardwareausgabe verwendet.

## Edrys

Die Monaco-Editoren publizieren ihren Inhalt über zwei getrennte Topics:

- `autosnake-python`
- `autosnake-cpp`

Der nächste Stationsausbau verbindet diese Topics mit einem isolierten Ausführungsdienst. Bis dahin dokumentiert edrys die lokalen Befehle transparent, statt eine nicht vorhandene Ausführung vorzutäuschen.
