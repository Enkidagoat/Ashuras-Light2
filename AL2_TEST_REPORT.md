# AL2-TEST-01 Verification Report

**Project:** Ashura's Light 2  
**Mode:** Verification only  
**Date:** 2026-11-15  
**Branch:** `feature/local-horizon-3d`  
**Tested commit:** `868d66ade56e6192a328662b87098724974c998a`

No source files or scientific calculations were modified.

## Synchronization

- Fetched `origin`, checked out `feature/local-horizon-3d`, and fast-forward pulled.
- HEAD: `868d66ade56e6192a328662b87098724974c998a`
- Worktree was clean before verification. This report and its three screenshots are the requested test deliverables.
- `main` was not changed.

## Kernel verification

Ran `python scripts/bootstrap_kernels.py` with `AL2_KERNEL_DIR` set to the repository's `kernels/` directory. Each downloaded file's SHA-256 matched both the bootstrap expectation and `docs/KERNEL_MANIFEST.md`.

| Kernel | Actual SHA-256 | Expected SHA-256 | Result |
| --- | --- | --- | --- |
| `naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | Match |
| `pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | Match |
| `moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | Match |
| `moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | Match |
| `de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | Match |

## Automated tests

Ran `python -m pytest -q` with the verified local kernels.

- **Passed:** 3
- **Failed:** 0
- **Skipped:** 0

## Negative-elevation check

Input site: longitude `0°`, latitude `-89.9°`, altitude `0 km`; UTC `2026-11-15 00:00:00 UTC`.

| Body | AZ / EL from API | README example | Rounded comparison |
| --- | --- | --- | --- |
| Sun | `114.43942006997335° / +1.514998039323311°` | `114.4394° / +1.5150°` | Match |
| Earth | `357.38039076018777° / -3.452976085892258°` | `357.3804° / -3.4530°` | Match |

The browser plot placed the Earth marker center at pixel row `124`; the zero-degree line was at row `121`. Thus the negative-elevation Earth marker appeared below the horizon line.

## Signed-coordinate checks

Both API responses preserved the submitted coordinates exactly (JSON numeric values may be represented as floats) and returned finite Sun/Earth AZ/EL values.

| Input latitude, longitude | API latitude, longitude | Sun AZ / EL | Earth AZ / EL | Result |
| --- | --- | --- | --- | --- |
| `-89.9°, -30°` | `-89.9°, -30.0°` | `144.4385178379821° / +1.4750207676433889°` | `27.37750883432273° / -3.4640701520845227°` | Preserved; finite |
| `+89.9°, +30°` | `+89.9°, +30.0°` | `107.74580152514312° / -1.5260655836177517°` | `213.98027757740633° / +1.9001327167095652°` | Preserved; finite |

## Mobile verification

Set the browser viewport to approximately `390 × 844`. Inputs and result cards were visible. The horizon canvas backing width matched its CSS width at `302 px`; the page document width was `375 px`, below the `390 px` viewport, so there was no page-wide horizontal overflow. The three-entry comparison retained signed site coordinates and UTC values. The provenance disclosure opened and exposed provenance, limitations, and JSON export.

Screenshots captured from the running app:

- [Mobile inputs, results, and negative Earth elevation](docs/screenshots/al2-test-01-mobile-results.png)
- [Mobile three-evaluation comparison](docs/screenshots/al2-test-01-mobile-comparison.png)
- [Mobile expanded provenance and limitations](docs/screenshots/al2-test-01-mobile-provenance.png)

The browser automation tool's full-page screenshot capture reported a shorter `630 px` viewport height on subsequent evaluations; viewport width remained `390 px`.

## Docker verification

- Built with `docker build -t ashura-light2:feature .`: **success**.
- Ran the image with `--network none`; inspected network mode as `none`.
- Confirmed all five `/app/kernels/` files existed and matched their expected SHA-256 values inside the container.
- Flask served the home page with HTTP `200` and logged listening on `0.0.0.0:5000`.
- The calculation API returned HTTP `200` and the same Sun/Earth results and DE421 provenance as the local run, without container network access.
- Ran the test suite inside the network-disabled container: **3 passed, 0 failed, 0 skipped**.

## Failures and unresolved items

- **Automated tests:** none failed or skipped.
- Docker build and network-disabled runtime checks passed.
- Browser automation's pointer click on “Calculate & Save” timed out waiting for the control to become stable. The page's native form `requestSubmit()` path successfully invoked the same submit handler, produced the results, and populated the comparison. A manual pointer click was not independently verified in this run.
- No source changes, merge, or deployment were made.
