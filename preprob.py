#!/usr/bin/env python3
from prepro import run_prepro

# --- KONFIGURATION BACKEND ---
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 'node_modules', 'target', 'build',
    'bin', '__pycache__', 'venv', '.gradle', '.settings', 'dist', 'out', '.mvn', 'javadoc', 'lib'
}
INCLUDE_EXTENSIONS = ('.java', '.puml')
INCLUDE_FILES = {'build.gradle', 'pom.xml', 'settings.gradle'}

def main():
    run_prepro(INCLUDE_EXTENSIONS, INCLUDE_FILES, IGNORE_DIRS, label="Backend")

if __name__ == "__main__":
    main()
