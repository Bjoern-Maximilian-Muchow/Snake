# AutoSnake-Stationsdienst

Der Stationsdienst verbindet die `runCommand`-Topics der Edrys-Monaco-Editoren mit begrenzten lokalen Aktionen:

- `autosnake-python`: Code in einer temporären Arbeitskopie mit den Level-2-Tests prüfen.
- `autosnake-cpp`: Code prüfen, als `uno-student` bauen und exklusiv auf den Arduino an `COM3` laden. Im virtuellen Stationsmodus wird stattdessen `virtual-student` gebaut und gestartet.

Lernende erhalten dabei keinen freien Terminalzugriff. Das Edrys-Terminal zeigt nur die Ausgabe des fest konfigurierten Befehls. Python wird zusätzlich auf eine begrenzte AST-Teilmenge beschränkt; dies ist eine Schutzschicht für den betreuten Lehrbetrieb, aber keine vollwertige Betriebssystem-Sandbox für unbekannte, böswillige Nutzer.

## Vorbereitung unter Windows

Das offizielle pyxtermjs-Backend verwendet POSIX-PTYs und läuft daher nicht nativ unter Windows. Dieses Repository enthält einen protokollkompatiblen, eingeschränkten Socket.IO-Server ohne freie Shell. Seine Abhängigkeiten werden isoliert installiert:

```powershell
.\scripts\setup_station.ps1
```

PlatformIO wird aus der VS-Code-Installation unter `%USERPROFILE%\.platformio` erkannt. Danach die Station starten:

```powershell
.\scripts\start_station.ps1 -ArduinoPort COM3
```

Anschließend den Edrys-Raum auf diesem Laptop in der Rolle **Station** öffnen. Die beiden Ausgabemodule verbinden sich mit `http://localhost:5000/pty`.

Für die hardwarefreie Simulation verwendet Edrys den Befehl `autosnake-run cpp $CODE --virtual`. Der Stationsdienst baut den eingereichten Bot und startet danach das native virtuelle Arduino-Programm. Es wird kein Arduino-Port benötigt.

Der Live-Monitor ist im VS-Code-Browser unter `http://localhost:5000/monitor` erreichbar. Er zeigt LED-Frames, Pin-Zustände, simulierte CPU-/RAM-Auslastung und beendet den laufenden virtuellen Arduino über **Simulation beenden**.

## Lokaler Funktionstest

Der Runner erwartet den Monaco-Inhalt Base64-kodiert:

```powershell
$code = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes((Get-Content learning\level2\student_bot.py -Raw)))
python station\runner.py python --base64 $code
```

Die Laufzeitdateien unter `.station-runtime/` sind nicht Teil des Repositorys.
