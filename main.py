"""food-picture-01 round 2 entry: copy the bundled food picture to the output dir.

The entry image lives in this repository as entry.png (JPEG bytes under that
name, which the competition accepts: the format is told apart by the file's
first bytes, not its extension). This program does nothing creative at run
time -- it ships the picture that was chosen beforehand, checks it is a
well-formed JPEG inside the size limit, and places an exact copy where the
grader expects it.

Run:  MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
"""

import hashlib
import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB, the competition's file-size ceiling
JPEG_OPEN = b"\xff\xd8\xff"
JPEG_CLOSE = b"\xff\xd9"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def jpeg_dimensions(data: bytes) -> tuple:
    """Read width/height from the first JPEG SOF marker (stdlib only)."""
    i = 2  # skip the SOI marker
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2: length, precision, h, w
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return (width, height)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        i += 2 + seg_len
    raise fail("no JPEG SOF marker found in entry.png")


def fail(message: str) -> "SystemExit":
    print(f"main.py: error: {message}", file=sys.stderr)
    return SystemExit(1)


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise fail("entry.png is missing from the repository")

    data = source.read_bytes()

    if len(data) > MAX_BYTES:
        raise fail(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit")
    if not data.startswith(JPEG_OPEN):
        raise fail("entry.png does not start with the JPEG magic bytes FF D8 FF")
    if not data.endswith(JPEG_CLOSE):
        raise fail("entry.png does not end with the JPEG end marker FF D9")

    width, height = jpeg_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise fail(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png"))
    # MAKEFUN_OUTPUT_DIR names the directory; tolerate a full file path too.
    target = out_dir if out_dir.suffix == ".png" else out_dir / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

    written = target.read_bytes()
    if written != data:
        raise fail("output differs from entry.png after copying")

    digest = hashlib.sha256(data).hexdigest()
    print(f"main.py: wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
