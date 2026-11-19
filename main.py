#!/usr/bin/env python3
"""make.fun entry — copies entry.png to /output/entry.png or $MAKEFUN_OUTPUT_DIR/entry.png."""

import os
import shutil
import sys


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write(f"missing {src}\n")
        sys.exit(1)

    out_path = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, out_path)


if __name__ == "__main__":
    main()
