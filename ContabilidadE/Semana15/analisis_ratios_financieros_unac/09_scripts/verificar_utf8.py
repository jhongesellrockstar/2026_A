from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
bad = [
    "\u00c3\u0192",
    "\u00c3\u201a",
    "\ufffd",
    "\x1c",
    "\x1d",
    "\ufffe",
    "informaci" + "?" + "n",
    "Decisi" + "?" + "n",
    "m" + "?" + "tricas",
    "\u00c2\u00be",
]
hits = []
for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix.lower() in {".tex", ".md", ".txt", ".csv", ".bib", ".bat", ".py"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in bad:
            if token in text:
                hits.append((path.relative_to(ROOT), token))

if hits:
    print("Se encontraron posibles problemas de codificación:")
    for rel, token in hits:
                print(f"- {rel}: {ascii(token)}")
    sys.exit(1)

print("OK: archivos revisados en UTF-8 sin patrones de mojibake definidos.")
