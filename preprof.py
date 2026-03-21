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
# Ordner, die komplett ignoriert werden (z.B. Library-Leichen oder Git-Daten)
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 'node_modules', 'dist', 'build', 'out', 'venv', '__pycache__', 'assets'
}

# NUR diese Dateiendungen werden in den Context aufgenommen
ALLOWED_EXTENSIONS = ('.html', '.css', '.js')


def is_web_file(filename):
    """Prüft, ob die Datei eine erlaubte Web-Endung hat."""
    return filename.lower().endswith(ALLOWED_EXTENSIONS)


def get_project_structure(start_path):
    structure = []
    for root, dirs, files in os.walk(start_path):
        # Filtert Ignorierte Ordner aus
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = os.path.relpath(root, start_path).count(os.sep)
        folder_name = os.path.basename(os.path.abspath(root))

        indent = ' ' * 4 * level

        # Wir zeigen im Strukturbaum nur Dateien an, die auch relevant sind
        relevant_files = [f for f in files if is_web_file(f)]

        # Ordner nur anzeigen, wenn er relevant ist oder relevante Dateien enthält
        if relevant_files or level == 0:
            structure.append(f"{indent}{folder_name}/")
            sub_indent = ' ' * 4 * (level + 1)
            for f in relevant_files:
                structure.append(f"{sub_indent}{f}")

    return "\n".join(structure)


def main():
    start_path = os.getcwd()
    project_name = os.path.basename(start_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"WEB_CONTEXT_{project_name}_{timestamp}.txt"
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    print(f"🌐 Analysiere Web-Projekt: {project_name}...")
    print(f"🎯 Fokus: {', '.join(ALLOWED_EXTENSIONS)}")

    output = []
    output.append(f"=== WEB PROJECT CONTEXT: {project_name} ===")
    output.append(f"Generated: {timestamp}")
    output.append(f"Allowed Extensions: {', '.join(ALLOWED_EXTENSIONS)}")
    output.append("\n--- RELEVANT DIRECTORY STRUCTURE ---")
    output.append(get_project_structure(start_path))
    output.append("\n" + "=" * 50 + "\n")

    file_count = 0
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if is_web_file(file):
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

    print(f"✅ Erfolg! {file_count} Web-Dateien zusammengefasst.")
    print(f"📄 Datei gespeichert unter: {download_path}")


if __name__ == "__main__":
    main()