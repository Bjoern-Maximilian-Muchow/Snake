#!/usr/bin/env sh
set -eu

echo "Firmware mit PlatformIO bauen und auf den Uno laden:"
echo "platformio run --environment uno --target upload"
echo "Seriellen Monitor öffnen:"
echo "platformio device monitor --environment uno"
echo "Die Firmware nutzt keine externen Arduino-Bibliotheken."
