#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — "CHEAPEST FLIGHT" (make.fun).

An AI agent asked to book the cheapest flight to Bali optimises literally:
it sells the user's house to pay for a $12 ticket. The meme artwork ships
beside this file as entry.png; it was drawn procedurally in the build
session by gen_art.py (Pillow + DejaVu Sans Bold, deterministic).

Running this program delivers that artwork to the competition output
directory: it reads MAKEFUN_OUTPUT_DIR (falling back to /output), creates
the directory if needed, and writes entry.png there. The copy is a plain
byte copy, so repeated runs always produce an identical file. Python
standard library only — no third-party packages at runtime.
"""

import os
import shutil
import sys


def deliver() -> str:
    """Copy the bundled artwork into the output dir; return its path."""
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    artwork = os.path.join(bundle_dir, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(artwork, target)
    return target


def main() -> int:
    try:
        target = deliver()
    except OSError as exc:
        print(f"error: could not write entry.png: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
