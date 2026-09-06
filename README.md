# CP/M Builds

Reproducible CP/M system images and the source/build artifacts used to create them for the IMSAI 8080 master-system project and related S-100 configurations.

Unlike ordinary working-disk images, the images in this repository are intentionally versioned so a tested CP/M system build can always be recovered together with the BIOS source, build notes, checksums, and any scripts used to produce it.

## Builds

- `fdcplus-3712-polyvti-62k/` — CP/M 2.2 for the Altair FDC+ in Drive Type 8 / iCOM FD3712 mode, 62K CP/M in a 63K RAM system, Polymorphic VTI at FC00H-FFFFH, North Star ZPB-A2 interrupt path. Includes the known-good original two-drive build and the four-drive A:-D: revision.

Each build directory should contain enough information to identify the target hardware and reproduce or verify the image.
