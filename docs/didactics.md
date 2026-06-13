# Didaktischer Lernpfad

AutoSnake trennt Referenzlösungen konsequent von den eigentlichen Lernaufgaben.

## Gemeinsamer Ablauf

1. **Demo:** Eine Referenzstrategie beobachten und den nächsten Zug vorhersagen.
2. **Aufgabe:** Eigene Regeln oder eigenen Code entwickeln.
3. **Test:** Bekannte Situationen mit verständlichem Feedback prüfen.
4. **Challenge:** Eine unbekannte Karte bearbeiten.
5. **Hardware:** Erst nach erfolgreichen Tests auf die einzelne Uno-Station wechseln.
6. **Reflexion:** Entscheidung, Laufzeit und Speicherbedarf erklären.

## Räume in edrys-Lite

Die Oberfläche trennt Orientierung und aktive Arbeit:

- **Lobby:** laufendes Beispiel, Überblick über die drei Level und Erklärung des Lernwegs
- **Room 1 / Level 1:** Regelblöcke, Einzelschritte und Challenge
- **Room 2 / Level 2:** Python-Auftrag, Codeeditor, Testausgabe und eigene Randfälle
- **Room 3 / Level 3:** Embedded-C++-Auftrag, Build-/Upload-Ausgabe und Ressourcenreflexion
- **Station:** technische Hinweise für den einzelnen physischen Arbeitsplatz

Jeder Levelraum beantwortet dieselben drei Fragen: Was ist der Auftrag? Wann ist das Level bestanden? Was kann ich danach? Dadurch müssen Lernende nicht zwischen fachlich fremden Modulen suchen und sehen ihr Ziel direkt neben dem Arbeitswerkzeug.

Der Lernlabor-Simulator ist in jedem Levelraum vorhanden und über `lockLevel` auf genau dieses Level begrenzt. Der Levelwähler wird dort vollständig ausgeblendet. In der Lobby erzwingt `lockMode=demo` eine reine Beispielansicht ohne Aufgaben- oder Challenge-Auswahl.

edrys-Lite erzeugt über `meta.defaultNumberOfRooms` die Standardräume `Room 1`, `Room 2` und `Room 3`. `showInCustom` ordnet Module diesen vorhandenen Räumen zu, erzeugt aber selbst keine Räume. Die Levelbezeichnung steht deshalb jeweils gut sichtbar im ersten Modul des Raums.

In der aktuellen edrys-Lite-Version kann die automatische Standardraumerzeugung beim ersten Rollenwechsel ausbleiben. Dann öffnet die Person, die die Klasse bereitgestellt hat, das Seitenmenü und klickt dreimal auf **Neuer Raum**. Sobald `Room 1` bis `Room 3` existieren, greift die Modulzuordnung ohne weitere Konfigurationsänderung.

Die Standardräume lassen sich in der aktuellen edrys-Lite-Oberfläche nicht über die Labor-YAML in `Level 1`, `Level 2` und `Level 3` umbenennen. Deshalb beginnt jeder Raum mit einer eindeutigen Levelüberschrift; technisch bleiben die Namen `Room 1` bis `Room 3` bestehen.

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
