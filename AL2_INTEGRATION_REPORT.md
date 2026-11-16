# AL2 Integration Report

**Project:** Ashura's Light 2
**Phase:** AL2-INTEGRATION-02
**Branch:** `integration/al2-release-candidate`
**Integrated source commit:** `b96b657f3220cc1526b08b48ca641aed006abe81`
**Base:** `origin/main` at `d50d9f484c48aee615fbcd7a862db89050a5a692`

## Integration and preservation

- The working tree was clean before integration. The current branch was `docs/submission-cleanup` at `b96b657`.
- A recoverable Git bundle and backup branch `backup/al2-pre-integration` were created at that source commit. The verified external kernel stack was copied to `/tmp/al2-integration-backup-20261116T0241/kernels`; its manifest is `/tmp/al2-integration-backup-20261116T0241/manifest.txt`.
- `dist/` did not exist before this task. A new local distribution was created after integration. The verified kernels were available under `/tmp/ashuras-light2-kernels`; the documented bootstrap command also populated the ignored project `kernels/` directory.
- `origin/main` is an ancestor of the integration source commit. There were no commits on `origin/main` missing from the source branch and no merge conflicts. The sole source commit ahead was `b96b657`.
- Its source changes were reviewed by path: README, app startup/API error guidance, user-visible labels, kernel/judge docs, deletion of obsolete planning/internal red-team docs, and a 30-day API regression test.
- `src/al2/geometry.py` and the scientific calculation implementation are unchanged from `origin/main`. The active sweep, presets, comparison, timeline, statistics, JSON export, and kernel integrity checks remain present.
- No push, merge to `main`, deployment, or submission was performed.

## Regression verification

Host environment, with verified kernels:

- `python -m pytest -q`: **21 passed**.
- `POST /api/compute`: **HTTP 200**.
- `POST /api/sweep` with `days=30`, `step_hours=1`: **HTTP 200**, 721 samples.
- For `(lon 0°, lat -89.9°, alt 0 km, 2026-11-15 00:00:00 UTC)`, sweep percentages were Sun above horizon **100.0%** and Earth above horizon **42.6%**. Both are finite and in `[0, 100]`.
- Missing and SHA-256-corrupted kernel directories caused startup kernel verification to fail closed (`KERNELS_OK=False`).

## Browser/UI verification

The actual Flask application was tested in Chromium at 1440 px desktop and 390 × 844 px mobile viewports using real API results.

- Preset selection updated the site coordinates and calculations returned successfully.
- Four single-epoch site evaluations appeared in the comparison table.
- The 30-day sweep returned 721 samples and finite, bounded statistics. At the selected Haworth approximate preset, the UI displayed Sun **69.8%**, Earth **59.2%**, and the elevation timeline.
- Timeline canvas rendered non-background series pixels.
- JSON export downloaded as `al2-result.json`; the file parsed and included Sun, Earth, and provenance data.
- No browser console errors, page errors, or failed requests occurred.
- Mobile document width was **390 px** at a 390 px viewport. The comparison region was **316 px** wide with **672 px** of internally scrollable table content; there was no page-wide horizontal overflow.

### Refreshed screenshots

Captured from the current UI after regression checks:

1. [Desktop landing/default UI](docs/screenshots/al2-test-03-desktop-final.png) — replaced.
2. [Desktop completed 30-day sweep](docs/screenshots/al2-sweep-desktop.png).
3. [Desktop sweep statistics and timeline](docs/screenshots/al2-sweep-stats-timeline-desktop.png).
4. [Desktop four-site comparison](docs/screenshots/al2-comparison-desktop.png).
5. [Mobile landing/default UI](docs/screenshots/al2-test-03-mobile-final.png) — replaced.
6. [Mobile sweep and internally scrollable comparison](docs/screenshots/al2-sweep-mobile.png).

The pre-refresh hashes for all previously tracked screenshots are recorded in the recovery manifest noted above.

## Docker judge package

- Build: `docker build -t ashura-light2:judge .` — **passed**.
- Image ID: `sha256:66d1edbb774275719fae165210dfad23ee6a9c5782e029c40c6571e064d328ef`.
- Archive: `dist/ashura-light2-judge.tar` (**99,616,768 bytes**).
- Archive SHA-256: `a2e8a2a83439deb78985597902823add1ca916e8563864a497568e9fd29d13ca`.
- `dist/SHA256SUMS` matches the archive.
- Clean-load: the image tag was removed, loaded from the archive, and restored with the same image ID.
- After clean-load, `docker run --rm --network none ashura-light2:judge python -m pytest -q`: **21 passed**.
- Offline image verification found all five manifest kernels and matched every SHA-256. A live Flask server in a `--network none` container returned home **HTTP 200**, `/api/compute` **HTTP 200**, and `/api/sweep` **HTTP 200** with 721 samples and the reference percentages above.

## README command verification

- On Linux, the documented default `python scripts/bootstrap_kernels.py` completed and verified all five files in `kernels/`.
- The documented Python tests passed with that verified stack.
- The README Docker image tag `ashuras-light2` was built and run at loopback port 5001 because the host app occupied 5000; its home page and both APIs returned HTTP 200, including the 721-sample sweep. The packaged `ashura-light2:judge` archive was separately clean-loaded and tested offline.
- PowerShell commands were reviewed but not executed in this Linux environment.

## Security review findings

The focused sweep-flow security review reported **no confirmed exploitable vulnerabilities**. Its scope was the 30-day sweep execution flow, inputs, data handling, and side effects; it was not a comprehensive security audit of the full product.

## Scientific baseline and limitations

The scientific baseline was not changed: DE421, frame `MOON_ME_DE421`, geometric correction `NONE`, and reference radius 1737.4 km. The outputs remain terrain-free centre-direction geometry. Horizon visibility does not establish usable power, operational communications, terrain-masked visibility, or landing safety. Preset coordinates marked approximate should be confirmed before use. Docker still uses Flask's development server and is intended for local demonstration, not production deployment.

## Current state

`integration/al2-release-candidate` is locally testable and ready for Project Owner acceptance. Screenshot files, this report, the local ignored Docker package, and verified kernel files are present locally. No changes were pushed or merged.
