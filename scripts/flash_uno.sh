#!/usr/bin/env sh
set -eu

echo "Arduino flashing is not configured yet."
echo "Later this can use Arduino CLI, for example:"
echo "arduino-cli compile --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno"
echo "arduino-cli upload -p <PORT> --fqbn arduino:avr:uno firmware/arduino_uno/AutoSnakeUno"
