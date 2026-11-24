#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

Writes a single satirical sentence to ``<output_dir>/entry.txt``.

The sentence roasts lawmakers who write the rules for AI, crypto and the
internet yet cannot convert a file to PDF. It is fixed text: the grader runs
this program twice and both runs must produce the same file, so nothing here
depends on time, randomness, the network or the environment beyond the
output directory (``MAKEFUN_OUTPUT_DIR``, default ``/output``).
"""

import os
import sys

MAX_CHARS = 320

ENTRY = (
    "The committee that writes the laws for artificial intelligence emailed "
    "its own bill to itself four times this morning, because nobody in the "
    "room knows how to turn a .docx into a PDF."
)


def validate(text: str) -> str:
    """Return the entry text, or raise ValueError if it breaks the gate."""
    text = " ".join(text.split())
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters; must be 1..{MAX_CHARS}")
    # Exactly one sentence: ends with a period and holds no sentence break.
    # (".docx" is fine: its period is followed by a letter, not a space.)
    if not text.endswith(".") or ". " in text or "? " in text or "! " in text:
        raise ValueError("entry must be exactly one sentence")
    return text


def main() -> int:
    try:
        text = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(path, encoding="utf-8") as fh:
        if fh.read() != text:
            print("round-trip check failed", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
