#!/usr/bin/env sh
set -eu

echo "Arduino-Flashen ist noch nicht konfiguriert."
echo "Später kann dafür zum Beispiel Arduino CLI genutzt werden:"
echo "arduino-cli compile --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno"
echo "arduino-cli upload -p <PORT> --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno"
echo "Die Firmware nutzt keine externen Arduino-Bibliotheken."
