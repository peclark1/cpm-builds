# CP/M 2.2 — FDC+ 3712 / Poly VTI / 62K

## Target hardware

- North Star ZPB-A2 Z80 CPU
- Altair FDC+ firmware 1.8
- FDC+ Drive Type 8 / iCOM-Pertec FD3712 emulation at ports 08H/09H
- Shugart SA-800-class IBM 3740 8-inch SSSD drives
- 63K ordinary RAM from 0000H-FBFFH
- CP/M 2.2 sized to 62K
- Polymorphic VTI framebuffer FC00H-FFFFH, keyboard port FCH
- VTI keyboard interrupt: JMP2 -> S-100 VI2 -> ZPB RST 2 -> page-zero 0010H
- No monitor ROM, PIC-8, or CF/IDE required by this profile

## CP/M memory layout

- CCP: DE00H
- BDOS: E600H
- BIOS: F400H-F77FH (896-byte standard BIOS reservation)
- BIOS runtime workspace: F780H-FBFFH
- VTI: FC00H-FFFFH

The system has 63K of RAM, but CP/M is deliberately generated as a 62K system so the F780H-FBFFH region can be used for BIOS runtime storage without increasing the on-disk BIOS reservation.

## Preserved images

Two exact image builds are preserved here. Because the ChatGPT GitHub connector used to create this repository cannot directly transfer binary files, the repository stores each image as a very small compressed XOR delta against the original DeRamp 48K image. `tools/rebuild_from_deramp.py` recreates the exact 256,256-byte `.img` files and verifies their SHA-256 checksums.

Required upstream base image:

`CPM22v1.0-FDC+3712-48K.dsk`

SHA-256: `2c8f2054475d0ef00eb913a887709a3942053d2231b3405547d8ffafdff60164`

Rebuild both preserved images with:

```bash
python3 tools/rebuild_from_deramp.py /path/to/CPM22v1.0-FDC+3712-48K.dsk
```

The generated images are written under `images/`.

### `CPM22v1.0-FDC+3712-62K-PolyVTI-2Drive.img`

Known-good build recovered from the working floppy-image library. Supports A: and B:. This is the image originally called `CPM22v1.0-FDC+3712-62K-PolyVTI-dev.img` during development.

SHA-256: `f1ef9993d30408401b713759f6dc3774ade2d8c24a8f1b51ea38f97deb6b55f5`

### `CPM22v1.0-FDC+3712-62K-PolyVTI-4Drive.img`

Four-drive revision supporting A:, B:, C:, and D:. It preserves the proven 62K CP/M, FDC+, and VTI layout. The low-level FDC+ code already encoded drive numbers 0-3; this revision extends `SELDSK`, adds DPH2/DPH3, and allocates separate CSV/ALV workspace for drives C: and D:.

SHA-256: `3a4f0363e11f49b496bb10b5f03a85cf14294b3aa1ca09a94842f50ce7914370`

**Status:** generated and statically verified; physical A:-D: hardware testing still required.

## Four-drive BIOS additions

The existing two-drive BIOS ends at approximately F710H, leaving unused space inside the reserved BIOS area through F77FH. The four-drive revision uses that space without moving CCP, BDOS, BIOS, VTI, or the system tracks.

- DPH2: F710H
- DPH3: F720H
- DPH pointer table: F730H
- extended four-drive `SELDSK`: F738H
- CSV2: F880H
- ALV2: F890H
- CSV3: F8B0H
- ALV3: F8C0H

The original `SELDSK` entry at F5C1H is changed to jump to the extended selector. The original low-level `SELSEC` routine already does `CURDRV & 03H` and rotates the drive number into the FD3712 drive-select bits, so no low-level FDC command changes are required.

## Source and tools

- `source/FDCPLUS_VTI_BIOS_2DRIVE.ASM` — preserved source for the known-good two-drive BIOS.
- `source/FDCPLUS_VTI_BIOS_4DRIVE.ASM` — source documenting the four-drive revision while preserving the proven BIOS addresses.
- `tools/make_4drive.py` — creates the four-drive image directly from the known-good two-drive image and verifies the result.
- `tools/rebuild_from_deramp.py` — reconstructs both exact images from the DeRamp 48K base image and the repository's compressed XOR deltas.
- `patches/` — lossless deltas for the two exact disk images.

## Provenance

The build originated from Mike Douglas / DeRamp's `CPM22v1.0-FDC+3712-48K` CP/M 2.2 distribution. The custom BIOS adds the native FDC+ Drive Type 8 disk interface and Polymorphic VTI console/keyboard support, and changes the CP/M size to 62K.
