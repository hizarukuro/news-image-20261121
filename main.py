#!/usr/bin/env python3
"""news-image-20261121 — "Sum up 21 November's world news in one image".

Grader program (program/v1). The front page is rendered ahead of time and
shipped in this repository as entry.png; this program simply installs it
as the entry image:

    source:  $MAKEFUN_BOT_DIR/entry.png      (default: this script's folder)
    target:  $MAKEFUN_OUTPUT_DIR/entry.png   (default: /output/entry.png)

The copy is a plain byte copy, so repeated runs produce byte-identical
output. Python 3.13 standard library only.
"""

import os
import shutil
import sys

ENTRY_NAME = "entry.png"


def source_path() -> str:
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        return os.path.join(bot_dir, ENTRY_NAME)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ENTRY_NAME)


def target_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, ENTRY_NAME)
    return os.path.join("/output", ENTRY_NAME)


def main() -> int:
    src = source_path()
    dst = target_path()
    if not os.path.isfile(src):
        print(f"error: entry image not found at {src}", file=sys.stderr)
        return 1
    out_dir = os.path.dirname(dst)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
