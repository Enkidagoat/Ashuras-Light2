# AL2 Integration Report

- **Project:** Ashura's Light 2
- **Phase:** AL2-INTEGRATION-01
- **Branch:** `integration/al2-release-candidate`
- **Status:** Local integration and offline verification complete; awaiting Project Owner testing.

## Integration history

| Commit | Purpose |
|---|---|
| `a9f0d76d05b3e5871be3c60381084ac59f308861` | Merge local AL2 kernel integrity checkpoints; parents: `366fb1339bb8fec32a88ff7f3d4fefb4b55c275f` and `f71e4fd0c8a8e9f97ae3ba0636e709042b9f5161`. |
| `ed304416699f51027ef425936e13e3788635d55d` | `Prepare offline judge-ready release package`. |
| `a0565ae52987b1e68cba1a1694711cd8964fa8d5` | Exclude internal reconciliation, preservation, and release reports from the Docker build context. |
| `61611221b00c800dc5268f641e722019b19318d3` | Update readiness evidence with the final image and archive verification. |

Preserved checkpoint ancestry:

- `60e42a2624514a21154df450c1c07a45c7fc1f09`: ancestor of integration `HEAD`.
- `f71e4fd0c8a8e9f97ae3ba0636e709042b9f5161`: ancestor of integration `HEAD`.
- `820f45b83a17313da166dc37b65056beb709e34f`: ancestor of integration `HEAD`, through `origin/main`.
- `366fb1339bb8fec32a88ff7f3d4fefb4b55c275f`: ancestor of integration `HEAD`.

The remote feature commit was not merged again; `origin/main` already contained it. The pre-integration worktree stash remains intact: `0b17039bcba0233a7b09b5f3b3e0c35e2c146f9a`.

## Conflict resolution

`templates/index.html` was reconciled against the latest fetched `origin/main` template. The warm lunar palette and other remote template content were retained, with the responsive, keyboard-focusable comparison-table wrapper restored from the stashed worktree. The resulting template diff against `origin/main` is the table wrapper only.

## Integrated release file inventory

The release implementation and evidence commits add or modify these 20 paths relative to `origin/main`:

**Added**

- `.dockerignore`
- `.gitignore`
- `AL2_JUDGE_READINESS_REPORT.md`
- `AL2_KERNEL_INTEGRITY_REPORT.md`
- `AL2_TEST_REPORT.md`
- `docs/JUDGE_QUICKSTART.md`
- `docs/KERNEL_NOTICES.md`
- `docs/screenshots/al2-test-01-mobile-comparison.png`
- `docs/screenshots/al2-test-01-mobile-provenance.png`
- `docs/screenshots/al2-test-01-mobile-results.png`
- `docs/screenshots/al2-test-03-desktop-final.png`
- `docs/screenshots/al2-test-03-mobile-final.png`
- `src/al2/kernel_manifest.py`
- `tests/test_kernel_integrity.py`

**Modified**

- `README.md`
- `app.py`
- `docs/KERNEL_MANIFEST.md`
- `scripts/bootstrap_kernels.py`
- `src/al2/geometry.py`
- `templates/index.html`

`AL2_INTEGRATION_REPORT.md` itself is tracked separately in an internal evidence commit; it is not part of the 20-path release inventory or the judge package commit.

The judge package commit staged only the nine requested judge-facing files. The reconciliation, preservation, release-review, and integration reports are not part of that package commit. The reconciliation, preservation, release-review, readiness, and integration reports are excluded from the Docker build context. `dist/ashura-light2-judge.tar` and `dist/SHA256SUMS` remain ignored and are not in Git history.

## Scientific boundary and kernel verification

`src/al2/geometry.py` is unchanged relative to the preserved `f71e4fd` integrity checkpoint. The integration does not alter calculation formulas, coordinate conventions, or scientific constants:

- Ephemeris: DE421
- Frame: `MOON_ME_DE421`
- Correction: `NONE`
- Reference radius: 1737.4 km

The five image kernels were verified against `docs/KERNEL_MANIFEST.md` during the final image build and again after clean-loading the archive:

| Kernel | Expected and actual SHA-256 | Result |
|---|---|---|
| `naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | Pass |
| `pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | Pass |
| `moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | Pass |
| `moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | Pass |
| `de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | Pass |

## Regression results

- **Automated suite in final clean-loaded image:** 12 passed, 0 failed, 0 skipped.
- Host `.venv` run without local kernels: 9 passed, 3 skipped. These skips were not counted as passes; the full in-image suite ran with the verified kernel stack.
- Corrupted `de421.bsp`: calculation API returned **HTTP 503** with a SHA-256 mismatch; no result was produced.
- Network-disabled live Flask server: `/` returned **HTTP 200**; three `/api/compute` requests returned **HTTP 200**.
- Reference case, `(lon 0°, lat -89.9°, alt 0 km, 2026-11-15 00:00 UTC)`:
  - Sun: `114.4394201° / +1.5149980°` AZ/EL.
  - Earth: `357.3803908° / -3.4529761°` AZ/EL.
- Signed coordinate cases `(-30°, -89.9°)` and `(+30°, +89.9°)` were preserved and returned finite results. Invalid longitude returned **HTTP 400**.
- Browser UI: four evaluations appeared in the comparison table, including negative elevations and signed coordinates. The JSON export produced `al2-result.json`; its content parsed as JSON and included provenance.
- At a 390 × 844 viewport, document client and scroll widths were both 375 px (vertical scrollbar included). The comparison region was 302 px wide with 672 px scrollable content and keyboard focusability; no page-wide horizontal overflow occurred.

## Docker distribution

- Image: `ashura-light2:judge`
- Image ID: `sha256:6a4b2f9bb25da3fe96a92b90dc0509295889800cd978a234772f138cce16691a`
- Archive: `dist/ashura-light2-judge.tar`
- Archive size: **97,968,128 bytes**
- SHA-256: `9e02a93579d0980c42dd3aa0f9e82cd66d4baf1c17ceaa762192e0ec44f3d215`
- `dist/SHA256SUMS` contains the matching archive digest.
- Clean-load check removed the judge image tag and loaded the archive; Docker restored the same image ID. The full test suite, kernel/hash checks, and offline API checks then passed against the restored image.

The app and calculations work with `--network none`. This Docker host cannot publish a browser port from `--network none`; local browser testing therefore used a loopback-published bridge port. No runtime kernel download is required.

## Current state and limitations

- Integration branch is local; no push, merge to `main`, deployment, publication, or submission occurred.
- The integration/readiness reports remain local and unpushed.
- The pre-integration stash remains available and was not dropped.
- No production WSGI server is configured; the Docker image starts Flask's development server for this local judge demonstration.
- Judges requiring strict container network isolation and simultaneous host-browser access will need an owner-approved networking alternative.

**Ready for Project Owner testing and demo recording.**
