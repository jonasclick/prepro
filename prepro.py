#!/usr/bin/env python3
import os
import pyperclip

# Python Script for Context Stacking, helps to ask an LLM questions about your project

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
        if level == 0 and os.path.basename(root) == '.':
            # Verhindert unschöne Darstellung des Wurzelpunkts
            folder_name = os.path.basename(os.getcwd())
        else:
            folder_name = os.path.basename(root)

        indent = ' ' * 4 * level
        structure.append(f"{indent}{folder_name}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith(EXTENSIONS):
                structure.append(f"{sub_indent}{f}")
    return "\n".join(structure)


def main():
    current_dir = os.getcwd()
    # Prüfen, ob ein src-Ordner existiert, sonst aktuelles Verzeichnis nutzen
    src_path = os.path.join(current_dir, "src")
    start_path = src_path if os.path.exists(src_path) else current_dir

    print(f"📂 Analysiere Pfad: {start_path}...")

    output = []
    output.append(f"=== PROJECT CONTEXT (Source: {os.path.basename(start_path)}) ===")
    output.append("--- STRUCTURE ---")
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

    final_context = "\n".join(output)
    pyperclip.copy(final_context)

    print(f"Fertig! {file_count} Dateien aus 'src' wurden in die Zwischenablage kopiert.")


if __name__ == "__main__":
    main()