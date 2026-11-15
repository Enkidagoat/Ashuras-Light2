# Ashura's Light 2

Ashura's Light 2 is a lunar south-pole geometry navigator. Given a site and UTC time, it calculates terrain-free centre-direction azimuth and elevation for the Sun and Earth using the pinned DE421 SPICE kernel stack.

## Features
- Site input (signed latitude and longitude)
- UTC date-time
- Geometric centre-direction Sun and Earth AZ/EL
- Labeled horizon plot (markers below the line are below the horizon)
- Comparison of up to four saved evaluations
- JSON export with provenance
- Explicit limitations

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Kernel acquisition
```bash
python scripts/bootstrap_kernels.py
```
This downloads the five pinned NAIF files into `kernels/` and verifies every SHA-256 against `docs/KERNEL_MANIFEST.md`. It exits non-zero on any mismatch.

```bash
export AL2_KERNEL_DIR=kernels
python app.py
```
Open http://127.0.0.1:5000

On Windows PowerShell:
```powershell
$env:AL2_KERNEL_DIR = (Resolve-Path .\kernels).Path
python app.py
```

## Docker
```bash
docker build -t al2 .
docker run -p 5000:5000 al2
```
The image downloads and verifies kernels at build time. The application listens on `0.0.0.0:5000`.

## Scientific methodology
- Frame: MOON_ME_DE421
- Correction: NONE (geometric)
- Reference radius: 1737.4 km
- Azimuth: clockwise from north
- Elevation: relative to local horizontal plane

## Limitations
Terrain-free centre-direction geometry only. Does not establish usable electrical power, operational communication availability, terrain-masked visibility, or landing safety.

## Tests
```bash
pytest tests/
```

## License
MIT. Kernels are separate and subject to NAIF redistribution terms.
