# AL2 Judge Readiness Report

## Result

The local offline distribution, kernel integrity checks, application API, and UI verification passed. The one Docker limitation is that this environment does not publish ports in `--network none` mode, so a browser-accessible local launch uses Docker's bridge mode with a loopback-only host binding. The application itself has no runtime network dependency.

## Tested source and distribution

- Branch: `integration/al2-release-candidate`
- Integration merge commit: `a9f0d76d05b3e5871be3c60381084ac59f308861`
- Judge package commit: `ed304416699f51027ef425936e13e3788635d55d`
- Image-context hardening commit: `a0565ae52987b1e68cba1a1694711cd8964fa8d5`
- Source base commit: `f71e4fd0c8a8e9f97ae3ba0636e709042b9f5161`
- Existing checkpoints `60e42a2624514a21154df450c1c07a45c7fc1f09` and `f71e4fd0c8a8e9f97ae3ba0636e709042b9f5161` are preserved.
- Judge-facing AL2-TEST-03 changes are committed on the integration branch. Internal reports remain uncommitted; no changes were made to `main`.
- Docker image: `ashura-light2:judge`
- Docker image ID: `sha256:6a4b2f9bb25da3fe96a92b90dc0509295889800cd978a234772f138cce16691a`
- Archive: `dist/ashura-light2-judge.tar`
- Archive size: **97,968,128 bytes**
- Archive SHA-256: `9e02a93579d0980c42dd3aa0f9e82cd66d4baf1c17ceaa762192e0ec44f3d215`
- Checksum manifest: `dist/SHA256SUMS`
- The `dist/SHA256SUMS` entry matches the archive SHA-256 above.
- Clean-state verification: removed the `ashura-light2:judge` tag, loaded `.\dist\ashura-light2-judge.tar`, and confirmed Docker restored image ID `sha256:6a4b2f9bb25da3fe96a92b90dc0509295889800cd978a234772f138cce16691a`.

The image includes the Flask application, Python dependencies, MIT license, kernel manifest, separate kernel notice, current checksum-verifying judge quick start, updated screenshots, warm lunar color palette, and all five verified kernels. Kernels were downloaded and verified during image build; no downloader runs at application startup.

## Kernel integrity

The image build bootstrap and runtime directory verification matched every manifest hash:

| Kernel | Expected SHA-256 | Actual SHA-256 | Result |
|---|---|---|---|
| `naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | Pass |
| `pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | Pass |
| `moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | Pass |
| `moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | Pass |
| `de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | Pass |

A disposable container with a modified `de421.bsp` rejected startup integrity and returned **HTTP 503** from the calculation API with a SHA-256 mismatch. It did not produce a calculation.

## Automated and scientific regression

- Re-run after clean-state archive load: full packaged test suite **12 passed, 0 failed, 0 skipped**. The host Python 3.14 environment, without kernels, reported 9 passed and 3 skipped; the complete Docker run with verified kernels passed all 12.
- The restored image ran with Docker `--network none`; Flask returned **HTTP 200** for `/` and for all three API cases.
- Reference case at longitude 0°, latitude -89.9°, altitude 0 km, UTC `2026-11-15 00:00:00`:
  - Sun: azimuth `114.4394201°`, elevation `+1.5149980°` (rounded: `114.4394° / +1.5150°`).
  - Earth: azimuth `357.3803908°`, elevation `-3.4529761°` (rounded: `357.3804° / -3.4530°`).
- API checks at longitude/latitude `(-30°, -89.9°)` and `(+30°, +89.9°)` preserved both signed coordinates and returned finite Sun and Earth azimuth/elevation values.
- Invalid longitude input returned **HTTP 400**. A modified `de421.bsp` returned **HTTP 503** and no calculation.
- The kernel-loading changes in `src/al2/geometry.py` match the preserved `f71e4fd` integrity checkpoint; this integration adds no geometry changes. DE421, `MOON_ME_DE421`, correction `NONE`, reference radius `1737.4 km`, coordinate conventions, and calculation formulas remain unchanged.

## User-interface verification

The running application was exercised with mouse clicks and keyboard Enter submission. Four evaluations were saved and displayed with site coordinates and UTC times; negative elevations were visible; JSON export produced the result and provenance. The four-entry comparison showed:

| Latitude | Longitude | UTC | Sun AZ / EL | Earth AZ / EL |
|---:|---:|---|---:|---:|
| +89.9° | -30° | 2026-11-18 00:00 UTC | 72.087 / -1.583 | 156.235 / -0.846 |
| -89.9° | -30° | 2026-11-16 00:00 UTC | 132.259 / +1.488 | 26.020 / -2.221 |
| +89.9° | +30° | 2026-11-17 00:00 UTC | 119.919 / -1.505 | 215.216 / +0.550 |
| -89.9° | 0° | 2026-11-15 00:00 UTC | 114.439 / +1.515 | 357.380 / -3.453 |

The visual refresh uses a warm near-black background, warm charcoal panels, amber Sun accents, and copper Earth accents. At a 390 × 844 mobile viewport, inputs, result cards, plot, comparison, and provenance remained accessible. The layout viewport measured 375 px due to the vertical scrollbar and document scroll width also measured 375 px, so there was no page-wide horizontal overflow. The keyboard-focusable comparison region measured 302 px with 672 px of scrollable table content.

Screenshots captured from the running application:

- Desktop: [docs/screenshots/al2-test-03-desktop-final.png](docs/screenshots/al2-test-03-desktop-final.png)
- Mobile: [docs/screenshots/al2-test-03-mobile-final.png](docs/screenshots/al2-test-03-mobile-final.png)

## Launch and limitation

The packaged checksum-verifying instructions and loopback-only launch were tested from the repository root after clean-state archive loading; the application returned **HTTP 200**:

```powershell
$expected = (Get-Content .\dist\SHA256SUMS).Trim().Split(' ')[0]
$actual = (Get-FileHash -Algorithm SHA256 .\dist\ashura-light2-judge.tar).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Archive SHA-256 mismatch" }
docker load -i .\dist\ashura-light2-judge.tar
docker run --rm -p 127.0.0.1:5000:5000 ashura-light2:judge
```

Open <http://127.0.0.1:5000/>. The project is distributed with all required kernels; its startup and calculations work with networking disabled. However, Docker's `--network none` mode does not publish a host port in this environment, so `--network none -p 5000:5000` cannot provide the browser UI. The network-disabled container was verified through in-container HTTP requests. See [docs/JUDGE_QUICKSTART.md](docs/JUDGE_QUICKSTART.md) and [docs/KERNEL_NOTICES.md](docs/KERNEL_NOTICES.md).

## Outstanding items

- The archive and commits remain local; they have not been pushed or submitted.
- No merge, deployment, publication, or repository visibility change was performed.
- For a judge who requires strict container network isolation and browser access simultaneously, the Docker port-publishing limitation needs an owner-approved alternative.
