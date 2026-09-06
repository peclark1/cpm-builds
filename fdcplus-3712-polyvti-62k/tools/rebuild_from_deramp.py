#!/usr/bin/env python3
"""Rebuild the preserved 62K PolyVTI images from the DeRamp 48K base image.

The repository stores tiny compressed XOR deltas as hex text so the exact disk
images are preserved even when a GitHub connector cannot transfer binary files.
"""

from __future__ import annotations

import argparse
import hashlib
import lzma
from pathlib import Path

BASE_SHA256 = "2c8f2054475d0ef00eb913a887709a3942053d2231b3405547d8ffafdff60164"
OUTPUTS = {
    "2drive": (
        "patches/CPM22v1.0-FDC+3712-62K-PolyVTI-2Drive.xor.xz.hex",
        "images/CPM22v1.0-FDC+3712-62K-PolyVTI-2Drive.img",
        "f1ef9993d30408401b713759f6dc3774ade2d8c24a8f1b51ea38f97deb6b55f5",
    ),
    "4drive": (
        "patches/CPM22v1.0-FDC+3712-62K-PolyVTI-4Drive.xor.xz.hex",
        "images/CPM22v1.0-FDC+3712-62K-PolyVTI-4Drive.img",
        "3a4f0363e11f49b496bb10b5f03a85cf14294b3aa1ca09a94842f50ce7914370",
    ),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path, help="DeRamp CPM22v1.0-FDC+3712-48K.dsk")
    parser.add_argument(
        "--repo-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="build directory containing patches/ and images/",
    )
    args = parser.parse_args()

    base = args.base.read_bytes()
    actual = digest(base)
    if actual != BASE_SHA256:
        raise SystemExit(
            "Wrong DeRamp base image.\n"
            f"Expected SHA-256: {BASE_SHA256}\n"
            f"Actual SHA-256:   {actual}"
        )

    for name, (patch_rel, output_rel, expected_sha) in OUTPUTS.items():
        patch_hex = (args.repo_dir / patch_rel).read_text(encoding="ascii")
        compressed_xor = bytes.fromhex("".join(patch_hex.split()))
        xor_mask = lzma.decompress(compressed_xor)
        if len(xor_mask) != len(base):
            raise SystemExit(f"{name}: XOR mask size mismatch")

        output = bytes(a ^ b for a, b in zip(base, xor_mask))
        actual_out = digest(output)
        if actual_out != expected_sha:
            raise SystemExit(
                f"{name}: output checksum mismatch\n"
                f"Expected: {expected_sha}\nActual:   {actual_out}"
            )

        output_path = args.repo_dir / output_rel
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(output)
        print(f"{name}: wrote {output_path}")
        print(f"{name}: SHA-256 {actual_out}")


if __name__ == "__main__":
    main()
