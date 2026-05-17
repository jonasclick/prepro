#!/usr/bin/env python3
from prepro import run_prepro

# --- KONFIGURATION FRONTEND ---
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 'node_modules', 'target', 'build',
    'bin', '__pycache__', 'venv', '.gradle', '.settings', 'dist', 'out', '.mvn', 'javadoc', 'lib',
    '.next', 'node_modules'
}

INCLUDE_EXTENSIONS = ('.html', '.css', '.js', '.ts', '.tsx', '.jsx')
INCLUDE_FILES = {'package.json', 'tsconfig.json', 'next.config.js', 'tailwind.config.js'}

def main():
    run_prepro(INCLUDE_EXTENSIONS, INCLUDE_FILES, IGNORE_DIRS, label="Frontend")

if __name__ == "__main__":
    main()
