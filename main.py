#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — "CHEAPEST FLIGHT" (make.fun).

An AI agent asked to book the cheapest flight to Bali optimises literally:
it sells the user's house to pay for a $12 ticket. The meme artwork ships
beside this file as entry.png; it was drawn procedurally in the build
session by gen_art.py (Pillow + DejaVu Sans Bold, deterministic).

Running this program delivers that artwork to the competition output
directory: it reads MAKEFUN_OUTPUT_DIR (falling back to /output), creates
the directory if needed, and writes entry.png there. The copy is a plain
byte copy, so repeated runs always produce an identical file. After the
copy it validates the delivered file — PNG signature, 1024x1024 IHDR
dimensions, and size at most 1 MiB — and deletes the output and fails
loudly if anything is off, so a corrupt bundle can never ship silently.
Python standard library only — no third-party packages at runtime.
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def validate(path: str) -> str | None:
    """Return an error string if the delivered PNG is bad, else None."""
    try:
        with open(path, "rb") as fh:
            header = fh.read(24)
    except OSError as exc:
        return f"could not read back entry.png: {exc}"
    if len(header) < 24 or header[:8] != PNG_SIGNATURE:
        return "bad PNG signature"
    if header[12:16] != b"IHDR":
        return "missing IHDR chunk"
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return (f"unexpected dimensions {width}x{height}, "
                f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return f"entry.png too large: {size} bytes > {MAX_BYTES}"
    return None


def deliver() -> str:
    """Copy the bundled artwork into the output dir; return its path."""
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    artwork = os.path.join(bundle_dir, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(artwork, target)
    problem = validate(target)
    if problem is not None:
        try:
            os.remove(target)
        except OSError:
            pass
        raise ValueError(problem)
    return target


def main() -> int:
    try:
        deliver()
    except OSError as exc:
        print(f"error: could not write entry.png: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: invalid entry.png: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
