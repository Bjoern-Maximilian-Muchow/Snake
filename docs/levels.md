# Schwierigkeitslevel

AutoSnake Remote Lab nutzt genau drei Level. Jedes Level baut auf demselben Spiel und derselben Bot-Schnittstelle auf, erwartet aber mehr Struktur, Sicherheit und Validierung.

## 1. Schüler

### Lernziele

- Snake-Grid, Richtung, Futter und Kollisionen verstehen.
- Einfache regelbasierte Steuerlogik schreiben.
- Unmittelbare Wandkollisionen vermeiden.
- Sich grob in Richtung Futter bewegen.

### Anforderungen

- Der Bot gibt nur gültige Richtungen zurück.
- Der Bot fährt nicht absichtlich direkt in sich selbst zurück.
- Der Bot nutzt einfache Vergleiche zwischen Kopfposition und Futterposition.
- Der Bot enthält einen Ausweichzug, falls die bevorzugte Richtung unsicher ist.

### Bewertungsideen

- Bot für eine feste Anzahl Schritte auf einfachen Karten laufen lassen.
- Prüfen, dass er in einfachen Situationen Wände vermeidet.
- Prüfen, dass er sich dem Futter nähert, wenn kein Hindernis im Weg ist.

## 2. Student Anfang Studium

### Lernziele

- Einen strukturierten Algorithmus mit klaren Hilfsfunktionen bauen.
- Ein Spielfeldmodell pflegen oder auswerten.
- Hindernisse als blockierte Felder berücksichtigen.
- Sichere und unsichere Züge unterscheiden.
- Optional einfache BFS-Suche nutzen, um Futter zu finden.

### Anforderungen

- Der Bot bewertet alle erlaubten Züge, bevor er entscheidet.
- Der Bot vermeidet Wände, Hindernisse und den eigenen Körper, wenn möglich.
- Der Bot trennt Analyse, Entscheidung und Ausweichlogik.
- Optional: Der Bot findet auf kleinen Spielfeldern mit BFS einen kürzesten Weg zum Futter.

### Bewertungsideen

- Gültigkeit der Züge über mehrere Spielzustände testen.
- Prüfen, dass der Bot sichere Züge gegenüber direkten, aber unsicheren Zügen bevorzugt.
- Prüfen, dass Hindernisse nicht betreten werden.
- Optionales BFS-Ergebnis mit bekannten kürzesten Wegen vergleichen.

## 3. Fortgeschrittener Student

### Lernziele

- Robuste Pfadsuche und Sicherheitsvalidierung implementieren.
- Hindernisse in die Pfadsuche und Sicherheitsprüfung einbeziehen.
- Über Sackgassen und zukünftig erreichbaren freien Raum nachdenken.
- Begrenzte Laufzeit auf eingebetteter Hardware beachten.
- Verhalten in Randfällen mit Tests absichern.

### Anforderungen

- Der Bot nutzt Pfadsuche oder eine gleichwertige systematische Strategie.
- Der Bot prüft, ob ein gewählter Pfad trotz Hindernissen genug sicheren Raum übrig lässt.
- Der Bot hat ein begrenztes Rechenzeitbudget.
- Die Firmware begrenzt die Level-3-Botentscheidung auf ungefähr 3 Millisekunden pro Spielschritt.
- Der Bot enthält Tests für kollisionsreiche Situationen und Beinahe-Sackgassen.

### Bewertungsideen

- Deterministische Challenge-Karten ausführen.
- Messen, dass die Entscheidungszeit innerhalb eines konfigurierten Limits bleibt.
- Testen, dass der Bot offensichtliche Fallen vermeidet, auch wenn Futter nahe liegt.
- Von Lernenden geschriebene Tests für fortgeschrittene Szenarien verlangen.
