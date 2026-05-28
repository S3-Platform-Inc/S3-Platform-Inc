#!/usr/bin/env python3
"""Print a PlantUML online-editor URL for each *.puml in the repo root.

Encoding follows https://plantuml.com/text-encoding (raw deflate + PlantUML's
custom base64 alphabet). The resulting URL pre-loads the diagram source in
the online editor, so it doubles as a "view this diagram" link in the README.

Run from anywhere; uses the repo root as the working set.
"""

from __future__ import annotations

import os
import sys
import zlib

ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
SERVER = "https://www.plantuml.com/plantuml/uml/"


def _encode_3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return ALPHA[c1] + ALPHA[c2] + ALPHA[c3] + ALPHA[c4]


def _encode64(data: bytes) -> str:
    out = []
    n = len(data)
    for i in range(0, n, 3):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < n else 0
        b3 = data[i + 2] if i + 2 < n else 0
        out.append(_encode_3bytes(b1, b2, b3))
    return "".join(out)


def plantuml_encode(text: str) -> str:
    raw = text.encode("utf-8")
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    compressed = compressor.compress(raw) + compressor.flush()
    return _encode64(compressed)


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(f for f in os.listdir(repo_root) if f.endswith(".puml"))
    if not files:
        print("No .puml files found.", file=sys.stderr)
        return 1
    for name in files:
        with open(os.path.join(repo_root, name), encoding="utf-8") as fh:
            url = SERVER + plantuml_encode(fh.read())
        print(f"{name}\t{url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
