# Arduino-Uno-Firmware

Dieser Ordner enthält die Firmware-Grundstruktur für den Arduino Uno R3 im AutoSnake Remote Lab.

Der Code ist bewusst klein gehalten und nutzt keine externen Arduino-Bibliotheken. Verwendet werden nur Arduino-Core-Funktionen wie `Serial`, `millis()`, `micros()`, `pinMode()` und `digitalWrite()`.

## Struktur

- `AutoSnakeUno.ino`: Arduino-Einstiegspunkt, Bot-Aufruf, Timing und Statistik.
- `game_engine.*`: hardwareunabhängiger Snake-Zustand und Update-Logik.
- `bot_interface.h`: kompakter Spielzustand und Bewegungs-API.
- `example_bot_basic.h`: einfacher regelbasierter Beispielbot.
- `led_grid.*`: aktuell No-Library-Platzhalter mit eingebauter LED; später Anschluss an das reale LED-Grid.
- `perf_monitor.*`: Live-Statistik zu Schrittzeit und RAM.

Der Arduino Uno hat wenig RAM. Deshalb vermeidet die Firmware dynamische Speicherallokation und speichert den Snake-Körper in Arrays fester Größe.

## Live-Statistik

Die Firmware schreibt jede Sekunde eine Zeile über Serial mit `115200` Baud:

```text
steps=42 score=1 len=4 state=ok step_us=80 avg_us=76 max_us=132 free_ram=1210 min_free_ram=1208
```

Bedeutung:

- `steps`: ausgeführte Spielschritte.
- `score`: Punktzahl.
- `len`: aktuelle Snake-Länge.
- `state`: letzter Schrittzustand (`ok`, `food`, `wall`, `self`).
- `step_us`: Laufzeit des letzten Bot- und Engine-Schritts in Mikrosekunden.
- `avg_us`: durchschnittliche Schrittzeit.
- `max_us`: bisher höchste Schrittzeit.
- `free_ram`: aktuell freier RAM in Bytes.
- `min_free_ram`: niedrigster bisher gemessener freier RAM.

## Seriellen Monitor öffnen

Unter Windows kann der einfache Monitor genutzt werden:

```powershell
.\scripts\monitor_uno.ps1 -Port COM3
```

Der Port kann abweichen. Der aktuell erkannte Uno hing beim Einrichten an `COM3`.

## Kompilieren und Flashen

Mit Arduino IDE:

1. `firmware/arduino_uno/AutoSnakeUno/AutoSnakeUno.ino` öffnen.
2. Board: `Arduino Uno`.
3. Port auswählen, z.B. `COM3`.
4. Hochladen.
5. Seriellen Monitor auf `115200` Baud stellen.

Mit Arduino CLI, falls installiert:

```sh
arduino-cli compile --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno
arduino-cli upload -p COM3 --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno
```
