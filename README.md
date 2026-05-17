# prepro - Context Stacking für LLMs

`prepro` ist ein einfaches Kommandozeilen-Werkzeug (CLI), das dein gesamtes Projekt (oder Teile davon) in eine einzige Textdatei zusammenfasst.

### Warum braucht man das?
Wenn du einer KI (wie ChatGPT, Claude oder Gemini) Fragen zu deinem Projekt stellst, fehlt ihr oft der Kontext über andere Dateien. Anstatt jede Datei einzeln zu kopieren, erstellt `prepro` eine strukturierte Übersicht und packt den Inhalt aller relevanten Dateien in ein Dokument. Dies nennt man "Context Stacking".

## Features
- **Intelligente Filterung**: Ignoriert automatisch unwichtige Ordner wie `.git`, `node_modules` oder `build`.
- **Spezialisierte Befehle**: Getrennte Befehle für Frontend- und Backend-Fokus.
- **Projektstruktur**: Fügt am Anfang der Datei einen Verzeichnisbaum hinzu.
- **Einfache Installation**: Einmal installieren, überall nutzen.

## Installation

1. Stelle sicher, dass du Python installiert hast.
2. Klone dieses Repository oder lade die Dateien herunter.
3. Öffne ein Terminal im Projektordner und führe aus:

```bash
pipx install . --force
```
*(Hinweis: Falls du `pipx` noch nicht hast, installiere es via `pip install pipx`.)*

## Nutzung

Navigiere in deinem Terminal zu deinem Programmierprojekt und gib einen der folgenden Befehle ein:

| Befehl | Fokus | Inkludierte Dateien (Beispiele) |
| :--- | :--- | :--- |
| `prepro` | Standard | (Entspricht `preprob`) |
| `preprob` | Backend | `.java`, `build.gradle`, `pom.xml`, `.puml` |
| `preprof` | Frontend | `.ts`, `.tsx`, `.js`, `.html`, `package.json` |

Die generierte Datei wird automatisch in deinem **Downloads-Ordner** gespeichert (z.B. `CONTEXT_MeinProjekt_2024-05-17.txt`).

## Anpassung für eigene Bedürfnisse

Du kannst das Skript ganz einfach erweitern, um andere Dateitypen zu unterstützen:

1. Öffne `preprob.py` (für Backend) oder `preprof.py` (für Frontend).
2. Passe die Variablen an:
   - `INCLUDE_EXTENSIONS`: Füge neue Dateiendungen hinzu (z.B. `'.py'`, `'.cpp'`).
   - `INCLUDE_FILES`: Füge exakte Dateinamen hinzu, die immer dabei sein sollen (z.B. `'README.md'`, `'Dockerfile'`).
   - `IGNORE_DIRS`: Füge Ordner hinzu, die komplett ignoriert werden sollen.
3. Führe danach erneut `pipx install . --force` aus, um die Änderungen zu aktivieren.
