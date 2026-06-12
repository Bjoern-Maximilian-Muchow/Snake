# Didaktischer Lernpfad

AutoSnake trennt Referenzlösungen konsequent von den eigentlichen Lernaufgaben.

## Gemeinsamer Ablauf

1. **Demo:** Eine Referenzstrategie beobachten und den nächsten Zug vorhersagen.
2. **Aufgabe:** Eigene Regeln oder eigenen Code entwickeln.
3. **Test:** Bekannte Situationen mit verständlichem Feedback prüfen.
4. **Challenge:** Eine unbekannte Karte bearbeiten.
5. **Hardware:** Erst nach erfolgreichen Tests auf die einzelne Uno-Station wechseln.
6. **Reflexion:** Entscheidung, Laufzeit und Speicherbedarf erklären.

## Level 1: Regeln sichtbar machen

Lernende bauen im Browser eine geordnete Liste aus Bedingungs- und Aktionsblöcken. Die erste passende Regel bestimmt den Zug. Dadurch werden Bedingungen, Prioritäten, Rückfallregeln und Ursache-Wirkung sichtbar, ohne dass Syntax im Weg steht.

Das Erfolgserlebnis entsteht durch unmittelbare Ausführung, Einzelschritte und eine Challenge mit unbekannter Karte. Der Blockeditor prüft, ob eine Rückfallregel, eine Sicherheitsreaktion und mindestens eine Futterregel vorhanden sind.

## Level 2: Vom Modell zum Python-Code

Die visuelle Logik wird in Funktionen übertragen:

- `is_blocked` modelliert das Spielfeld.
- `safe_moves` erzeugt gültige Kandidaten.
- `choose_move` trifft eine begründete Entscheidung.

Die Tests sind absichtlich zunächst rot. Lernende arbeiten schrittweise bis alle Tests grün sind und ergänzen danach eigene Randfälle.

## Level 3: Embedded-Entscheidungen

Die gleiche Bot-Idee wird als C++-Funktion auf dem Arduino umgesetzt. Lernende müssen feste Speichergrenzen, Laufzeitlimit, Fallback und Messdaten berücksichtigen. PlatformIO und die Live-Telemetrie machen Flash, SRAM und Botzeit sichtbar.

## Motivation ohne Lösungswahl

Beispielbots bleiben im Demo-Modus als Vergleichsmaßstab. Im Aufgaben- und Challenge-Modus werden keine fertigen Lösungen ausgewählt. Fortschritt entsteht durch eigene Regeln, bestandene Tests, unbekannte Karten und messbare Verbesserungen.
