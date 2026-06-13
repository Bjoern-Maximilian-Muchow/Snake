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

## Edrys und Stationsdienst

Die Monaco-Editoren publizieren ihren Inhalt über zwei getrennte Topics:

- `autosnake-python`
- `autosnake-cpp`

Zwei pyxtermjs-Ausgabemodule hören stationsseitig auf diese Topics. Der Windows-kompatible Socket.IO-Server unter `station/server.py` akzeptiert ausschließlich `autosnake-run python` und `autosnake-run cpp`. Der begrenzte Runner unter `station/runner.py` akzeptiert nur Base64-kodierten Editorinhalt und führt keine frei wählbaren Shell-Befehle aus.

- Python wird in eine temporäre Arbeitskopie geschrieben und mit einem Zeitlimit getestet.
- Python-Importe, Dunder-Zugriffe und Datei-/Prozessfunktionen werden vor der Ausführung per AST-Prüfung abgelehnt.
- C++ wird auf verbotene dynamische Speicherallokation geprüft, exklusiv gebaut und auf `COM3` geladen.
- `.station-runtime/hardware.lock` verhindert gleichzeitige Hardwarezugriffe.

Station unter Windows starten:

```powershell
.\scripts\setup_station.ps1
.\scripts\start_station.ps1 -ArduinoPort COM3
```

Danach muss derselbe Laptop den Edrys-Raum in der Rolle **Station** öffnen. Die Browsermodule erreichen den lokalen Dienst unter `http://localhost:5000/pty`.
