#!/usr/bin/env python3
"""Create the four-drive CP/M image from the proven two-drive image.

This is intentionally a surgical BIOS patch. It preserves the exact working
62K CP/M / FDC+ / Poly VTI image and uses only previously-unused bytes in the
standard F400H-F77FH BIOS reservation.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXPECTED_INPUT_SHA256 = "f1ef9993d30408401b713759f6dc3774ade2d8c24a8f1b51ea38f97deb6b55f5"
EXPECTED_OUTPUT_SHA256 = "3a4f0363e11f49b496bb10b5f03a85cf14294b3aa1ca09a94842f50ce7914370"

BIOS_FILE_OFFSET = 0x1680   # Track 1, physical sector 20 in the 26x128 image
BIOS_ADDRESS = 0xF400


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch_at(memory_address: int, payload: bytes, image: bytearray) -> None:
    offset = BIOS_FILE_OFFSET + (memory_address - BIOS_ADDRESS)
    image[offset : offset + len(payload)] = payload


def build(input_path: Path, output_path: Path) -> None:
    original = input_path.read_bytes()
    digest = sha256(original)
    if digest != EXPECTED_INPUT_SHA256:
        raise SystemExit(
            f"Refusing to patch unexpected input image.\n"
            f"Expected: {EXPECTED_INPUT_SHA256}\n"
            f"Actual:   {digest}"
        )

    image = bytearray(original)

    # Original SELDSK begins at F5C1H. Replace its first three bytes
    # (MOV A,C / CPI 02H) with a same-size jump to the extended selector.
    patch_at(0xF5C1, bytes.fromhex("C3 38 F7"), image)  # JMP F738H

    # DPH2 at F710H: XLT, 3 scratch words, DIRBUF, DPB, CSV2, ALV2.
    patch_at(
        0xF710,
        bytes.fromhex("C7 F6 00 00 00 00 00 00 80 F7 01 F7 80 F8 90 F8"),
        image,
    )

    # DPH3 at F720H.
    patch_at(
        0xF720,
        bytes.fromhex("C7 F6 00 00 00 00 00 00 80 F7 01 F7 B0 F8 C0 F8"),
        image,
    )

    # DPH pointer table at F730H: DPH0, DPH1, DPH2, DPH3.
    patch_at(0xF730, bytes.fromhex("E1 F6 F1 F6 10 F7 20 F7"), image)

    # Extended SELDSK at F738H.
    #
    #   MOV A,C
    #   CPI 04H
    #   JNC SEL4BAD
    #   STA CURDRV
    #   MVI A,0FFH
    #   STA DRVTRK
    #   MOV L,C
    #   MVI H,00H
    #   DAD H
    #   LXI D,DPHTAB
    #   DAD D
    #   MOV E,M
    #   INX H
    #   MOV D,M
    #   XCHG
    #   RET
    # SEL4BAD:
    #   LXI H,0000H
    #   RET
    selector = bytes.fromhex(
        "79 FE 04 D2 53 F7 "
        "32 74 F8 3E FF 32 79 F8 "
        "69 26 00 29 11 30 F7 19 5E 23 56 EB C9 "
        "21 00 00 C9"
    )
    patch_at(0xF738, selector, image)

    output = bytes(image)
    out_digest = sha256(output)
    if out_digest != EXPECTED_OUTPUT_SHA256:
        raise SystemExit(
            f"Internal build verification failed.\n"
            f"Expected: {EXPECTED_OUTPUT_SHA256}\n"
            f"Actual:   {out_digest}"
        )

    output_path.write_bytes(output)
    print(f"Wrote {output_path}")
    print(f"SHA-256 {out_digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="known-good two-drive .img")
    parser.add_argument("output", type=Path, help="four-drive output .img")
    args = parser.parse_args()
    build(args.input, args.output)


if __name__ == "__main__":
    main()
