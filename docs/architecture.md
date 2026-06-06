# Architektur

AutoSnake Remote Lab ist in kleine Komponenten aufgeteilt, damit Lernende Bot-Logik entwickeln und testen können, bevor echte Hardware verfügbar ist.

## Komponenten

### Game Engine

Die Game Engine verwaltet den Snake-Zustand: Rastergröße, Snake-Körper, Futter, Richtung, Punktzahl, Kollisionen und Spielschritte. Sie soll möglichst hardwareunabhängig bleiben, damit dasselbe Verhalten in Arduino-Firmware, Browser-Simulator und Python-Testsimulator abgebildet werden kann.

### Bot-Schnittstelle

Die Bot-Schnittstelle stellt einen kompakten Spielzustand bereit und erwartet eine Bewegungsentscheidung. Auf dem Arduino Uno muss diese Schnittstelle dynamische Speicherallokation und große Datenkopien vermeiden. Im Python-Simulator wird dieselbe Idee mit einfachen Datenklassen und reinen Funktionen umgesetzt.

### LED-Renderer

Der LED-Renderer übersetzt den abstrakten Spielzustand in Pixel für ein 16x16 RGB-LED-Grid. Während der Simulationsphase ersetzt der Browser-Renderer die physischen LEDs.

### Simulator

Der Simulator besteht aus zwei Teilen:

- Ein Web-Simulator zeigt das 16x16 Grid und dient zunächst als visuelle Kameraersatzansicht.
- Ein Python-Simulator kann von Tests und Bot-Implementierungen ohne Arduino-Hardware genutzt werden.

### Tests

Die Tests prüfen Bewegung, Kollisionen, Futterverhalten, Bot-Ausgaben und grundlegende Level-Anforderungen. Sie laufen ohne Arduino-Hardware und geben Lernenden und Maintainerinnen schnelles Feedback.

### Edrys-Lite-Station

Die edrys-Lite-Station verbindet später die Lernendenoberfläche mit dem physischen Arduino Uno R3, LED-Grid, Kamerastream und der Code-Ausführungsumgebung. Aktuell dokumentieren die Stationsdateien die geplanten Integrationspunkte.

## Hardwareunabhängigkeit

Die Game Engine soll nicht direkt von LED-Bibliotheken, Kamera-APIs, serieller Übertragung oder edrys-Lite-Details abhängen. Hardware-spezifischer Code gehört in Renderer-, Stations- oder Transportschichten. Dadurch bleibt die Kernlogik testbar und simuliertes sowie physisches Verhalten lassen sich leichter vergleichen.
