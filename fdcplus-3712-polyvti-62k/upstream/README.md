# Upstream DeRamp FDC+3712 package

The source package used while reconstructing/documenting this build was supplied as `FDC+3712.zip` from the DeRamp FDC+ software collection.

Uploaded package SHA-256:

`df353d6e621509fff043361adb7961ad32360fd732f84dc81f812572df8dfe93`

Important base disk image inside that package:

`CPM22v1.0-FDC+3712-48K.dsk`

SHA-256:

`2c8f2054475d0ef00eb913a887709a3942053d2231b3405547d8ffafdff60164`

Package contents observed during this build:

- `ReadMe.txt`
- `PROM.ASM`
- `COPY.ASM`
- `CPM22v1.0-FDC+3712-48K.dsk`
- `SYSGEN.COM`
- `BIOS.ASM`
- `MOVCPM.COM`
- `3X12DIAG.DOC`
- `BOOT.ASM`
- `FORMAT.ASM`
- `BASICGAMES3-8IN-SSSD.DSK`
- `3712DIAG.ASM`
- `SYSGEN.ASM`

The original DeRamp BIOS defines `NUMDISK equ 4`; the initial custom Poly VTI BIOS reduced CP/M drive selection to A:/B:, and the four-drive revision in this repository restores A:/B:/C:/D: support while retaining the custom FDC+ and VTI implementation.
