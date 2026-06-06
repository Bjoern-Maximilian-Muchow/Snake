# Arduino-Uno-Firmware

Dieser Ordner enthält die erste Firmware-Grundstruktur für den Arduino Uno R3 im AutoSnake Remote Lab.

Der Code ist bewusst klein gehalten und aufgeteilt in:

- `game_engine.*`: hardwareunabhängiger Snake-Zustand und Update-Logik.
- `bot_interface.h`: kompakter Spielzustand und Bewegungs-API.
- `example_bot_basic.h`: einfacher regelbasierter Beispielbot.
- `led_grid.*`: Platzhalter-Abstraktion für LED-Ausgabe.
- `AutoSnakeUno.ino`: Arduino-Einstiegspunkt.

Der Arduino Uno hat wenig RAM. Deshalb vermeidet die Firmware dynamische Speicherallokation und speichert den Snake-Körper in Arrays fester Größe.
