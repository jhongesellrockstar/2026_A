from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTS = {".tex", ".md", ".bib", ".csv"}
SKIP_DIRS = {"backup_codificacion_previa"}
PATTERNS = [
    "informaci?n",
    "Decisi?n",
    "m?tricas",
    "Â¾",
    "\x1c",
    "\x1d",
    "ï¿¾",
    "Ãƒ",
    "Ã‚",
    "ï¿½",
    "\ufffd",
    "?n",
    "m?",
]


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main():
    errors = []
    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append((path, 0, f"No es UTF-8 valido: {exc}"))
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pattern in PATTERNS:
                if pattern in line:
                    errors.append((path, i, pattern))
    if errors:
        print("ERROR: patrones problematicos encontrados")
        for path, line, pattern in errors:
            rel = path.relative_to(ROOT)
            print(f"{rel}:{line}: {pattern}")
        return 1
    print("OK: no se encontraron patrones problematicos de codificacion")
    return 0


if __name__ == "__main__":
    sys.exit(main())
