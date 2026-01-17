#!/usr/bin/env python3
import os
from datetime import datetime

# Python Script for Context Stacking, helps to ask an LLM questions about your project.
# Creates a .txt file with all relevant project information about your java project and saves it to downloads.

# Paket in den Path instellieren mit pipx install .
# Nach einer Änderung kann das Paket neu installiert werden mit pipx install . --force


# Konfiguration
EXTENSIONS = ('.java', '.kt', '.py', '.txt', '.md', '.properties', '.xml', '.gradle', '.sql', '.json')
IGNORE_DIRS = {'.git', 'target', '.idea', 'bin', 'node_modules', 'build', '__pycache__'}


def get_project_structure(start_path):
    structure = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = os.path.relpath(root, start_path).count(os.sep)
        folder_name = os.path.basename(root) if level > 0 else os.path.basename(os.getcwd())

        indent = ' ' * 4 * level
        structure.append(f"{indent}{folder_name}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith(EXTENSIONS):
                structure.append(f"{sub_indent}{f}")
    return "\n".join(structure)


def main():
    current_dir = os.getcwd()
    src_path = os.path.join(current_dir, "src")
    start_path = src_path if os.path.exists(src_path) else current_dir
    project_name = os.path.basename(current_dir)

    # Dateiname mit Zeitstempel für den Downloads-Ordner
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"CONTEXT_{project_name}_{timestamp}.txt"
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    print(f"📂 Analysiere: {start_path}...")

    output = []
    output.append(f"=== PROJECT CONTEXT: {project_name} ===")
    output.append(f"Generated: {timestamp}")
    output.append(f"Source Directory: {start_path}")
    output.append("\n--- STRUCTURE ---")
    output.append(get_project_structure(start_path))
    output.append("\n" + "=" * 50 + "\n")

    file_count = 0
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(EXTENSIONS):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start_path)

                output.append(f"FILE: {rel_path}")
                output.append("-" * 20)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        output.append(f.read())
                    file_count += 1
                except Exception as e:
                    output.append(f"[Fehler beim Lesen: {e}]")
                output.append("\n" + "=" * 50 + "\n")

    # In Datei schreiben
    with open(download_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output))

    print(f"Erfolg! {file_count} Dateien analysiert.")
    print(f"Datei gespeichert unter: {download_path}")


if __name__ == "__main__":
    main()