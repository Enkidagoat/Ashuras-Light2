# Kernel Manifest — Ashura's Light 2

Kernels are **not bundled**.

## Required files (DE421 stack)
Place these unmodified files in a `kernels/` directory (or set `AL2_KERNEL_DIR`). The hashes below were verified against downloads from the listed official NAIF archive paths on 2026-11-15.

| Filename | Official NAIF archive path | SHA-256 |
|---|---|---|
| naif0012.tls | `lsk/naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` |
| pck00011.tpc | `pck/pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` |
| moon_080317.tf | `fk/satellites/moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` |
| moon_pa_de421_1900-2050.bpc | `pck/moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` |
| de421.bsp | `spk/planets/a_old_versions/de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` |

## Acquisition
Use the [official NAIF generic kernels archive](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/) and the relative paths above. Verify every file's SHA-256 before use. For example, in PowerShell, run `Get-FileHash .\kernels\* -Algorithm SHA256` and compare the results with this manifest. `load_kernels` loads files in the required order.

NAIF's [SPICE use rules](https://naif.jpl.nasa.gov/naif/rules.html) state that kernels on its server may be downloaded and used by anyone, and may be redistributed if unmodified. The application's MIT license does not apply to kernels. Files from other sources may have different terms.

No automatic downloader is implemented; users provide local kernel files.

## Frame
MOON_ME_DE421  
Correction: NONE (geometric)  
Reference radius: 1737.4 km
