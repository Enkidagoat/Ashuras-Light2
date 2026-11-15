# Ashura's Light 2

Clean-room lunar south-pole site geometry navigator.

## What it does
- Enter a lunar site (east longitude, latitude, altitude).
- Enter a UTC date-time.
- Compute terrain-free centre-direction Sun and Earth azimuth/elevation relative to the local radial horizon.
- Display provenance and explicit limitations.
- Export results as JSON.

## What it does not do
- Terrain-masked visibility
- Usable electrical power prediction
- Operational communication availability
- Landing safety assessment

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Download the DE421 kernel stack into `kernels/` (see `docs/KERNEL_MANIFEST.md`). Verify SHA-256.

```bash
export AL2_KERNEL_DIR=kernels
python app.py
```

Open http://127.0.0.1:5000

## Tests
```bash
pytest tests/
```

## License
MIT. Kernels are not bundled; see KERNEL_MANIFEST.md.
