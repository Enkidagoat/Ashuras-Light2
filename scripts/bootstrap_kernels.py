#!/usr/bin/env python3
"""Download and verify the pinned DE421 kernel stack."""

import hashlib
import os
import sys
import urllib.request

BASE = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/"
FILES = [
    ("naif0012.tls", "lsk/naif0012.tls", "678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b"),
    ("pck00011.tpc", "pck/pck00011.tpc", "3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1"),
    ("moon_080317.tf", "fk/satellites/moon_080317.tf", "78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993"),
    ("moon_pa_de421_1900-2050.bpc", "pck/moon_pa_de421_1900-2050.bpc", "656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf"),
    ("de421.bsp", "spk/planets/a_old_versions/de421.bsp", "08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3"),
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    dest = os.environ.get("AL2_KERNEL_DIR", "kernels")
    os.makedirs(dest, exist_ok=True)
    for name, rel, expected in FILES:
        path = os.path.join(dest, name)
        url = BASE + rel
        print(f"Fetching {name} ...")
        urllib.request.urlretrieve(url, path)
        actual = sha256(path)
        if actual != expected:
            print(f"HASH MISMATCH for {name}: {actual}", file=sys.stderr)
            sys.exit(1)
        print(f"  verified {actual}")
    print(f"All kernels verified in {dest}")

if __name__ == "__main__":
    main()
