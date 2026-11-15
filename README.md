# Ashura's Light 2

Clean-room lunar south-pole site geometry navigator for exploratory geometry and education.

## Purpose
Allow users to compare candidate lunar south-pole sites and dates by viewing terrain-free centre-direction Sun and Earth azimuth/elevation relative to the local radial horizon.

## Features
- Site input (east longitude, latitude, altitude above 1737.4 km sphere)
- UTC date-time
- Geometric centre-direction Sun and Earth AZ/EL
- Simple labeled horizon view (N/E/S/W)
- Side-by-side comparison of up to four saved evaluations
- JSON export with inputs, outputs, frame, correction mode, and provenance
- Explicit limitations on every result

## Limitations
- Terrain-free only. Does not establish usable electrical power, operational communication availability, terrain-masked visibility, or landing safety.
- No mission-grade accuracy claimed.
- Kernels are not bundled.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Kernel acquisition
See `docs/KERNEL_MANIFEST.md`. Download the DE421 stack from official NAIF archives, verify SHA-256, and place in `kernels/`.

```bash
export AL2_KERNEL_DIR=kernels
python app.py
```

Open http://127.0.0.1:5000

## Scientific methodology
- Frame: MOON_ME_DE421
- Correction: NONE (geometric)
- Reference radius: 1737.4 km
- Local basis: radial up, east, north
- Azimuth: clockwise from north
- Elevation: relative to local horizontal plane

## Tests
```bash
pytest tests/
```
Tests require kernels present; otherwise they are skipped.

## License
MIT. Original project code only. Kernels remain subject to NAIF redistribution terms.
