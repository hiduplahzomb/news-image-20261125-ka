#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 competition.

Copies the pre-rendered entry.png shipped in this repository to the
output directory (MAKEFUN_OUTPUT_DIR, or /output when unset), then
reads the copy back and verifies it is byte-identical to the original.
Exits non-zero on any mismatch. Standard library only; no network.
"""
import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.digest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if _sha256(src) != _sha256(dst):
        print("ERROR: copied entry.png differs from the original", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
