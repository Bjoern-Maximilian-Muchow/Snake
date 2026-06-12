# Arduino-Uno-Firmware

Dieser Ordner enthält die Firmware-Grundstruktur für den Arduino Uno R3 im AutoSnake Remote Lab.

Der Code ist bewusst klein gehalten und nutzt keine externen Arduino-Bibliotheken. Verwendet werden nur Arduino-Core-Funktionen wie `Serial`, `millis()`, `micros()`, `pinMode()` und `digitalWrite()`.

## Struktur

- `AutoSnakeUno.ino`: Arduino-Einstiegspunkt, Bot-Aufruf, Timing und Statistik.
- `game_engine.*`: hardwareunabhängiger Snake-Zustand und Update-Logik.
- `bot_interface.h`: kompakter Spielzustand und Bewegungs-API.
- `example_bot_basic.h`: einfacher regelbasierter Level-1-Bot.
- `example_bot_safe.h`: Level-2-Bot mit Kollisions- und Hindernisprüfung.
- `example_bot_bfs.h`: zeitlich begrenzter Level-3-Bot mit BFS und Freiraumprüfung.
- `led_grid.*`: aktuell No-Library-Platzhalter mit eingebauter LED; später Anschluss an das reale LED-Grid.
- `perf_monitor.*`: Live-Statistik zu Schrittzeit und RAM.

Der Arduino Uno hat wenig RAM. Deshalb vermeidet die Firmware dynamische Speicherallokation. Der Snake-Körper liegt als 256-Byte-Ringpuffer vor. Snake-Belegung und Hindernisse nutzen jeweils ein 32-Byte-Bitfeld.

## Level auf dem Uno

Über den seriellen Monitor können Befehle gesendet werden:

- `1`: Level 1 mit einfachem Regelbot und ohne Hindernisse.
- `2`: Level 2 mit sicherem Bot und Hindernissen.
- `3`: Level 3 mit begrenzter BFS, Freiraumprüfung und mehr Hindernissen.
- `r`: aktuelles Level zurücksetzen.
- `c`: zwischen lesbarer Textausgabe und CSV wechseln.
- `h`: Hilfe ausgeben.

## Live-Statistik

Die Firmware schreibt jede Sekunde eine Zeile über Serial mit `115200` Baud:

```text
level=3 steps=42 score=1 len=4 state=ok food=1 collisions=0 bot_us=120 engine_us=18 render_us=8 max_bot_us=310 max_engine_us=24 max_render_us=10 avg_work_us=146 load_pct=0.081 free_ram=1240 min_free_ram=1236
```

Bedeutung:

- `steps`: ausgeführte Spielschritte.
- `score`: Punktzahl.
- `len`: aktuelle Snake-Länge.
- `state`: letzter Schrittzustand (`ok`, `food`, `wall`, `self`, `obstacle`).
- `food`: Anzahl gefressener Futterstücke seit dem letzten Reset.
- `collisions`: Anzahl erkannter Kollisionen.
- `bot_us`: Laufzeit der Bot-Entscheidung in Mikrosekunden.
- `engine_us`: Laufzeit des Engine-Schritts.
- `render_us`: Laufzeit der aktuellen Ausgabeabstraktion.
- `max_*_us`: jeweilige Maximalzeit seit dem letzten Reset.
- `avg_work_us`: durchschnittliche aktive Rechenzeit pro Spielschritt.
- `load_pct`: aktive Rechenzeit relativ zum konfigurierten 180-ms-Spielintervall.
- `free_ram`: aktuell freier RAM in Bytes.
- `min_free_ram`: niedrigster bisher gemessener freier RAM.

Im CSV-Modus wird eine maschinenlesbare Zeile pro Statistikintervall ausgegeben. Damit können Messwerte später aufgezeichnet und grafisch ausgewertet werden.

## Aktuelle Build-Auslastung

PlatformIO meldet für den aktuellen Stand mit drei Bots und Hindernissen:

```text
RAM:   770 / 2048 Byte (37,6 %)
Flash: 7958 / 32256 Byte (24,7 %)
```

Der jeweils exakte Wert wird bei jedem PlatformIO-Build neu ausgegeben. Diese statischen Build-Werte ergänzen die Live-Werte aus der Firmware.

## Seriellen Monitor öffnen

Unter Windows kann der einfache Monitor genutzt werden:

```powershell
.\scripts\monitor_uno.ps1 -Port COM3
```

Der Port kann abweichen. Der aktuell erkannte Uno hing beim Einrichten an `COM3`.

Alle drei Level lassen sich automatisiert vergleichen, wenn das Skript mit einer Python-Umgebung mit `pyserial` gestartet wird. Die PlatformIO-Python-Umgebung enthält diese Abhängigkeit bereits:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\python.exe" .\scripts\sample_uno.py --port COM3
```

## Kompilieren und Flashen

### PlatformIO in VS Code

Im Repository-Stamm liegt eine `platformio.ini`. Sie verwendet direkt den vorhandenen Firmware-Ordner und ist für Arduino Uno, `COM3` und `115200` Baud konfiguriert.

Über die PlatformIO-Seitenleiste:

1. `PROJECT TASKS` öffnen.
2. Unter `uno` den Eintrag `Build` wählen.
3. Danach `Upload` wählen.
4. Für die Live-Statistik `Monitor` öffnen.

Alternativ im PlatformIO-Terminal:

```powershell
platformio run --environment uno
platformio run --environment uno --target upload
platformio device monitor --environment uno
```

Der Build zeigt außerdem die statische Flash- und RAM-Belegung des Programms an. Die Firmware ergänzt diese Werte zur Laufzeit um Schrittzeiten und freien RAM.

### Arduino IDE

Mit Arduino IDE:

1. `firmware/arduino_uno/AutoSnakeUno/AutoSnakeUno.ino` öffnen.
2. Board: `Arduino Uno`.
3. Port auswählen, z.B. `COM3`.
4. Hochladen.
5. Seriellen Monitor auf `115200` Baud stellen.

### Arduino CLI, falls installiert

```sh
arduino-cli compile --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno
arduino-cli upload -p COM3 --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno
```
