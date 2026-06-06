# Tests

Die Testsuite nutzt `pytest` und läuft ohne Arduino-Hardware.

Sie validiert:

- Snake-Bewegung.
- Wandkollisionen.
- Selbstkollisionen.
- Hinderniskollisionen ab Level 2.
- Verhalten von Futter, Länge und Punktzahl.
- Gültigkeit der Züge des Beispielbots.
- Grundanforderungen der drei Level.

Aus dem Repository-Stamm ausführen:

```sh
pytest
```
