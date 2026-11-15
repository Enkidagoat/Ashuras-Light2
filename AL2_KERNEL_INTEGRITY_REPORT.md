# AL2-TEST-02 Kernel Integrity Report

## Scope and revision

- Branch: `feature/local-horizon-3d`
- Implementation was tested in the worktree based on `60e42a2624514a21154df450c1c07a45c7fc1f09`.
- No merge, deployment, or release was performed.
- DE421, `MOON_ME_DE421`, correction `NONE`, reference radius 1737.4 km, coordinate conventions, and geometry equations were not changed.

## Manifest and kernel hashes

`docs/KERNEL_MANIFEST.md` is read by both the bootstrap script and runtime loader. The official files were downloaded and all actual SHA-256 values matched the manifest:

| Kernel | Expected SHA-256 | Actual SHA-256 | Result |
|---|---|---|---|
| `naif0012.tls` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | `678e32bdb5a744117a467cd9601cd6b373f0e9bc9bbde1371d5eee39600a039b` | Pass |
| `pck00011.tpc` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | `3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1` | Pass |
| `moon_080317.tf` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | `78732477b96f9863e7b0d65bcee3c22b8707ca5ed0db56d1173319cb2e8c7993` | Pass |
| `moon_pa_de421_1900-2050.bpc` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | `656f90616403d75a75f0cd6c8830fc5b44f8cb4facb5ccb8915e752b397520cf` | Pass |
| `de421.bsp` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | `08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3` | Pass |

The bootstrap downloads to a same-directory temporary file, verifies its digest, and only then atomically replaces the destination. A failed/mismatched download preserved the existing destination and left no temporary file in the test.

## Automated tests

Final command: `python -m pytest -q` with `AL2_KERNEL_DIR` pointing to the verified temporary kernel stack.

- Passed: 12
- Failed: 0
- Skipped: 0

The 12 tests include all three existing kernel-backed geometry tests and nine new integrity/acquisition tests. Integrity failures covered missing and modified kernels, an incorrect manifest hash, an incomplete manifest, an unexpected directory entry, a simulated SPICE loading failure, and a mismatched download. The failed preflight cases made no `spice.furnsh()` calls. The simulated SPICE failure cleared the partial pool. Positive cases verified full-stack loading and hash-before-atomic-replacement.

## Reference calculation and API

For longitude `0`, latitude `-89.9`, altitude `0 km`, UTC `2026-11-15 00:00:00 UTC`:

| Target | Actual azimuth | Actual elevation | README reference |
|---|---:|---:|---|
| Sun | 114.4394° | +1.5150° | 114.4394° / +1.5150° |
| Earth | 357.3804° | -3.4530° | 357.3804° / -3.4530° |

The Earth elevation is negative, below the zero-degree horizon. The local Flask API returned HTTP 200 and preserved the supplied site coordinates in the result.

## Docker verification

- Built image: `ashura-light2:al2-test-02` — build passed; build-time bootstrap verified all five files.
- Ran the image with `--network none` — container started successfully.
- In-container manifest verification: all five actual hashes matched the expected values above.
- In-container API request to loopback succeeded and returned the reference Sun/Earth values above.
- No runtime network access was needed.

## Failures and remaining limitations

- No implementation or regression failures remain.
- Local test runs require the five separately acquired kernels; kernels are not added to the repository.
- Kernel acquisition and Docker image build require network access to the official NAIF archive. Runtime verification and calculation work without network access.
- The application verifies the complete kernel directory at startup; changing kernels or the manifest requires restarting the application.
- No deployment or release was attempted. Owner review/authorization remains required.
