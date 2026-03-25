#!/usr/bin/env python3
import os
from datetime import datetime

# Python Script for Context Stacking, helps to ask an LLM questions about your project.
# Creates a .txt file with all relevant project information about your java project and saves it to downloads.

# Paket in den Path instellieren mit pipx install .
# Nach einer Änderung kann das Paket neu installiert werden mit pipx install . --force

# Universelles Skript für Context Stacking
# Packt den gesamten Projektinhalt in eine Textdatei für LLMs.

# --- KONFIGURATION ---
# Ordner, die komplett ignoriert werden (inkl. Inhalt)
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 'node_modules', 'target', 'build',
    'bin', '__pycache__', 'venv', '.gradle', '.settings', 'dist', 'out', '.mvn', 'javadoc', 'lib'
}

# Dateiendungen, die inkludiert werden sollen
INCLUDE_EXTENSIONS = ('.html', '.css', '.js')


def is_ignored_dir(name):
    return name in IGNORE_DIRS


def should_include_content(name):
    return name.lower().endswith(INCLUDE_EXTENSIONS)


def get_project_structure(start_path):
    structure = []
    for root, dirs, files in os.walk(start_path):
        # In-place Filterung der Verzeichnisse
        dirs[:] = [d for d in dirs if not is_ignored_dir(d)]

        level = os.path.relpath(root, start_path).count(os.sep)
        # Wenn wir im Startordner sind, nehmen wir den tatsächlichen Ordnernamen
        folder_name = os.path.basename(os.path.abspath(root))

        indent = ' ' * 4 * level
        structure.append(f"{indent}{folder_name}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            # In der Übersicht zeigen wir alle Dateien an
            structure.append(f"{sub_indent}{f}")
    return "\n".join(structure)


def main():
    start_path = os.getcwd()  # Startet immer im aktuellen Verzeichnis
    project_name = os.path.basename(start_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"CONTEXT_{project_name}_{timestamp}.txt"
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    print(f"📂 Analysiere Projekt: {project_name}...")
    print(f"📍 Pfad: {start_path}")
    print(f"🔍 Inkludiere Inhalte für: {', '.join(INCLUDE_EXTENSIONS)}")

    output = []
    output.append(f"=== PROJECT CONTEXT: {project_name} ===")
    output.append(f"Generated: {timestamp}")
    output.append(f"Root Directory: {start_path}")
    output.append("\n--- DIRECTORY STRUCTURE ---")
    output.append(get_project_structure(start_path))
    output.append("\n" + "=" * 50 + "\n")

    file_count = 0
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not is_ignored_dir(d)]

        for file in files:
            if should_include_content(file):
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

    # In Datei schreiben
    with open(download_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output))

    print(f"✅ Erfolg! {file_count} Dateien inkludiert.")
    print(f"📄 Datei gespeichert unter: {download_path}")


if __name__ == "__main__":
    main()