# Kernel Manifest — Ashura's Light 2

The source repository does not include SPICE kernel binaries. Docker images built from this project download and include the five unmodified, manifest-verified NAIF kernels. For a local Python run, download them from the official NAIF archive with `python scripts/bootstrap_kernels.py`, or place matching unmodified files in `kernels/` yourself. Run the command from the project folder. It downloads into `kernels/` unless `AL2_KERNEL_DIR` names another destination.

## Required files (DE421 stack)
The application needs all five files below. The hashes were verified against downloads from the listed official NAIF archive paths on 2026-11-15.

| Filename | Official NAIF archive path | SHA-256 |
|---|---|---|
| naif0012.tls | `lsk/naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` |
| pck00011.tpc | `pck/pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` |
| moon_080317.tf | `fk/satellites/moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` |
| moon_pa_de421_1900-2050.bpc | `pck/moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` |
| de421.bsp | `spk/planets/a_old_versions/de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` |

## Download and verification
From the project folder, run:

```bash
python scripts/bootstrap_kernels.py
```

The script reads the filenames, archive paths, and hashes from this table. Each download is staged in a temporary file and verified before being moved into place. A failed or mismatched download does not replace an existing kernel.

The application reads this same table and checks that the kernel directory contains exactly these five regular files with matching hashes before loading any of them into SPICE. Missing, modified, symlinked, or extra entries prevent calculation. The default directory is `kernels/`; set `AL2_KERNEL_DIR` before starting the app to use another directory. Restart the app after downloading or changing kernels.

The Docker image downloads and verifies kernels during its build. No kernel download is needed while the container is running.

NAIF's [SPICE use rules](https://naif.jpl.nasa.gov/naif/rules.html) state that kernels on its server may be downloaded and used by anyone, and may be redistributed if unmodified. The application's MIT license does not apply to kernels. Files from other sources may have different terms.

## Frame
MOON_ME_DE421  
Correction: NONE (geometric)  
Reference radius: 1737.4 km
