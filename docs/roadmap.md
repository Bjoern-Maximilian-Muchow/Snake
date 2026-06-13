# Technische Roadmap

Diese Roadmap beschreibt die nächsten größeren Ausbaustufen nach der aktuellen Simulation-first-Phase. Ziel ist, vorhandenen Code weiterzuverwenden und Hardwaredetails klar von Game Engine, Bots und Lernaufgaben zu trennen.

## 1. Echtes 16x16-RGB-LED-Grid

### Was erhalten bleibt

- Game Engine, Bot-Schnittstelle und alle drei Level
- Kollisions-, Hindernis- und Futterlogik
- Live-Telemetrie für Laufzeit, SRAM und Flash
- Python- und Browser-Simulator als Vorab-Testplatz
- automatisierte Tests und Challenge-Szenarien

Der Simulator wird nicht überflüssig. Er bleibt als digitaler Zwilling für paralleles Arbeiten, Fehlersuche und Tests ohne reservierte Hardware bestehen.

### Was angepasst wird

Der aktuelle Platzhalter `LedGrid::setPixel(...)` in `firmware/arduino_uno/AutoSnakeUno/led_grid.cpp` wird durch einen hardwarespezifischen Treiber ersetzt. `LedGrid::render(...)` soll weiterhin nur Spielobjekte in Farben übersetzen und keine Details des elektrischen Protokolls kennen.

Vor der Implementierung müssen Grid-Typ, Signalprotokoll, Verdrahtung, Stromversorgung, Farbreihenfolge und physische Pixelanordnung dokumentiert werden. Besonders zu prüfen ist, ob der Uno ein vollständiges RGB-Framebuffer mit 768 Byte halten muss oder ob Pixel direkt beziehungsweise zeilenweise übertragen werden können.

### Vorgesehene Aufteilung

```text
firmware/arduino_uno/AutoSnakeUno/
├── led_grid.h              gemeinsame Renderer-Schnittstelle
├── led_grid.cpp            Farben und Spielzustand
└── drivers/
    ├── led_driver.h        kleine hardwareneutrale Treiberschnittstelle
    └── led_driver_*.cpp    konkretes Grid-Protokoll
```

Der Browser-Renderer bleibt vollständig unter `simulator/web/`. Hardwaretreiber werden nicht in die Engine verschoben. So kann später ein anderer Grid-Typ ausgetauscht werden, ohne Bots oder Spielregeln zu verändern.

## 2. Kamera und kombinierte Darstellung

Die Kamera wird auf das reale Grid ausgerichtet und liefert den Nachweis, dass tatsächlich die physische Station läuft. Die digitale Anzeige bleibt parallel erhalten.

Empfohlene Edrys-Ansicht:

- links oder oben: Live-Kamerabild der realen Matrix
- rechts oder darunter: digitaler Sollzustand aus Engine oder serieller Telemetrie
- gemeinsam sichtbar: Score, Länge, letzter Zug, Status und Laufzeitwerte

Diese Kombination ermöglicht den direkten Soll-Ist-Vergleich. Fehler in Verdrahtung, Pixelzuordnung, Farbreihenfolge oder Übertragung werden sichtbar, obwohl die Engine intern einen korrekten Zustand meldet.

Später kann optional eine Bildauswertung ergänzt werden, die das Kamerabild auf 16x16 Zellen entzerrt und erkannte Farben mit dem Sollzustand vergleicht. Sie ist eine eigene Stationskomponente und darf nicht Teil der Game Engine werden.

```text
Arduino -> serielle Telemetrie -> Stationsdienst -> digitale Ansicht
Kamera  -> Videodienst         -> Edrys          -> Live-Ansicht
```

## 3. Docker und Raspberry Pi

Das gesamte Stationssystem soll später reproduzierbar in Containern auf einem Raspberry Pi laufen. Der Pi übernimmt Stationsserver, Edrys-Anbindung, Kamera-Stream, Tests und PlatformIO-Aufrufe. Der Arduino bleibt für Game Engine und LED-Ausgabe zuständig.

Vorgesehene Struktur:

```text
deploy/
├── Dockerfile
├── compose.yaml
├── entrypoint.sh
└── README.md
```

Der Container benötigt später kontrollierten Zugriff auf:

- Arduino, typischerweise `/dev/ttyACM0` oder `/dev/ttyUSB0`
- Kamera, typischerweise `/dev/video0`
- einen persistenten PlatformIO-Cache
- den Stationsport für die lokale Edrys-Verbindung

Die Portnamen dürfen nicht fest im Code stehen. `COM3` bleibt die Windows-Entwicklungsvorgabe; auf dem Pi werden Arduino-Port, Kamera-Gerät und Serveradresse über Umgebungsvariablen konfiguriert.

Für den ersten Pi-Prototyp ist ein gemeinsamer Stationscontainer ausreichend. Später können Stationsrunner und Kamera-Streaming in getrennte Container aufgeteilt werden. Der Arduino-Upload bleibt durch den vorhandenen Hardware-Lock exklusiv.

### Noch zu klärende Punkte

- Raspberry-Pi-Modell und Betriebssystem
- CPU-Architektur und PlatformIO-Unterstützung
- konkretes Kameramodell und Streaming-Protokoll
- USB-Gerätenamen und stabile Gerätezuordnung
- Grid-Typ, Strombedarf und Pegelanpassung
- Zugriffsschutz, Neustartverhalten und Log-Rotation

## Empfohlene Reihenfolge

1. Konkretes LED-Grid auswählen und elektrisches Konzept festlegen.
2. LED-Treiber hinter der bestehenden Renderer-Schnittstelle implementieren.
3. Kamera lokal anbinden und Soll-/Ist-Ansicht in Edrys ergänzen.
4. Stationskonfiguration vollständig über Umgebungsvariablen steuerbar machen.
5. Docker- und Compose-Konfiguration erstellen.
6. Container auf dem Raspberry Pi mit Arduino und Kamera testen.
7. Dauerbetrieb, Wiederanlauf und Einzelstationszugriff absichern.
