# Generated disk images

Run:

```bash
python3 ../tools/rebuild_from_deramp.py /path/to/CPM22v1.0-FDC+3712-48K.dsk --repo-dir ..
```

from this directory (or invoke the script from anywhere without overriding `--repo-dir`) to recreate the exact two-drive and four-drive `.img` files here.

Expected SHA-256 checksums:

- `CPM22v1.0-FDC+3712-62K-PolyVTI-2Drive.img` — `f1ef9993d30408401b713759f6dc3774ade2d8c24a8f1b51ea38f97deb6b55f5`
- `CPM22v1.0-FDC+3712-62K-PolyVTI-4Drive.img` — `3a4f0363e11f49b496bb10b5f03a85cf14294b3aa1ca09a94842f50ce7914370`

The exact image contents are preserved in `../patches/`; these generated binaries can also be committed directly when working from a normal local Git checkout.
