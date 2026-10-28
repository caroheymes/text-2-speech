"""Lanceur dedie pour l'integration au menu contextuel Windows."""

import sys
from pathlib import Path

# Ajout du repertoire racine au sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.cli import main

if __name__ == "__main__":
    # Si appele avec un unique argument de fichier par l'explorateur Windows
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
        file_arg = sys.argv[1]
        sys.argv = [sys.argv[0], "--file", file_arg, "--mode", "condense", "--gui"]

    sys.exit(main())
