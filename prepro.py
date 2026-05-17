#!/usr/bin/env python3
import os
from datetime import datetime

"""
WAS TUT DIESES SKRIPT?
---------------------------------------------
Dieses Skript hilft dir, dein gesamtes Programmierprojekt in eine einzige Textdatei zu packen.
Warum? Damit du diese Datei einfach kopieren und einer KI (wie ChatGPT, Claude oder Gemini)
geben kannst. So "weiß" die KI über dein ganzes Projekt Bescheid und kann bessere Antworten geben.

WIE INSTALLIERE ICH ES?
-----------------------
1. Öffne ein Terminal (PowerShell oder CMD).
2. Gehe in diesen Ordner: `cd C:\pfad\zu\diesem\ordner`
3. Installiere es mit: `pipx install . --force`
   (Falls du kein pipx hast, installiere es erst mit `pip install pipx`)

WIE NUTZE ICH ES?
-----------------
Schreibe einfach einen dieser Befehle in dein Terminal, wenn du in deinem Projekt-Ordner bist:
- `prepro`  : Standard-Befehl (macht das gleiche wie preprob).
- `preprob` : Sammelt Backend-Dateien (z.B. Java, Gradle).
- `preprof` : Sammelt Frontend-Dateien (z.B. JavaScript, HTML, CSS).

Die fertige Datei findest du danach immer in deinem "Downloads"-Ordner.
"""

# Universelles Skript für Context Stacking (Kern-Logik)

def get_project_structure(start_path, ignore_dirs):
    structure = []
    for root, dirs, files in os.walk(start_path):
        # In-place Filterung der Verzeichnisse
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        level = os.path.relpath(root, start_path).count(os.sep)
        folder_name = os.path.basename(os.path.abspath(root))

        indent = ' ' * 4 * level
        structure.append(f"{indent}{folder_name}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{sub_indent}{f}")
    return "\n".join(structure)

def run_prepro(include_extensions, include_files, ignore_dirs, label="Projekt"):
    start_path = os.getcwd()
    project_name = os.path.basename(start_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"CONTEXT_{project_name}_{timestamp}.txt"
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    print(f"📂 Analysiere {label}: {project_name}...")
    print(f"📍 Pfad: {start_path}")
    print(f"🔍 Inkludiere Inhalte für: {', '.join(include_extensions)}")
    if include_files:
        print(f"📄 Explizit inkludierte Dateien: {', '.join(include_files)}")

    output = []
    output.append(f"=== PROJECT CONTEXT: {project_name} ({label}) ===")
    output.append(f"Generated: {timestamp}")
    output.append(f"Root Directory: {start_path}")
    output.append("\n--- DIRECTORY STRUCTURE ---")
    output.append(get_project_structure(start_path, ignore_dirs))
    output.append("\n" + "=" * 50 + "\n")

    file_count = 0
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            should_include = file.lower().endswith(include_extensions) or file in include_files
            if should_include:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start_path)

                output.append(f"FILE: {rel_path}")
                output.append("-" * 20)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        output.append(content)
                    file_count += 1
                except Exception as e:
                    output.append(f"[Fehler beim Lesen der Datei: {e}]")
                output.append("\n" + "=" * 50 + "\n")

    with open(download_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output))

    print(f"✅ Erfolg! {file_count} Dateien inkludiert.")
    print(f"📄 Datei gespeichert unter: {download_path}")

def main():
    # Lokaler Import um zirkuläre Abhängigkeiten zu vermeiden
    import preprob
    preprob.main()

if __name__ == "__main__":
    main()
