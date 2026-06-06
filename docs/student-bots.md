# Eigene Bots

Lernende implementieren ihre Bot-Logik in `simulator/python/student_bot.py`.

Der Einstiegspunkt ist immer:

```python
def choose_move(snapshot: BotSnapshot) -> Direction:
    ...
```

Die Funktion bekommt einen unveränderlichen Spielzustand und muss eine Richtung zurückgeben.

## Verfügbarer Spielzustand

- `snapshot.head`: Kopfposition der Snake.
- `snapshot.food`: Position des Futters.
- `snapshot.direction`: aktuelle Bewegungsrichtung.
- `snapshot.snake`: Körper der Snake, beginnend mit dem Kopf.
- `snapshot.obstacles`: Hindernisse auf dem Spielfeld, ab Level 2 relevant.
- `snapshot.score`: aktuelle Punktzahl.

## Erlaubte Rückgabe

Der Bot muss einen Wert aus `Direction` zurückgeben:

- `Direction.UP`
- `Direction.RIGHT`
- `Direction.DOWN`
- `Direction.LEFT`

## Regeln

- Der Bot darf den Spielzustand nicht verändern.
- Der Bot soll keine direkte Rückwärtsfahrt wählen.
- Ab Level 2 müssen Hindernisse als blockierte Felder behandelt werden.
- Fortgeschrittene Bots sollen Pfadsuche und Sicherheitsprüfung kombinieren.

## Tests

Die Schnittstelle wird mit pytest geprüft:

```sh
./scripts/run_tests.sh
```

Die Tests laufen ohne Arduino-Hardware.
