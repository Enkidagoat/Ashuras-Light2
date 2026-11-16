# AL2 Red Team Audit — Submission Readiness

**Date:** 2026-11-15  
**Branch:** feature/local-horizon-3d  
**Scope:** End-to-end review of geometry engine, Flask API, UI, kernel handling, and new viability features.

## Summary

The geometric core is sound and correctly limited. The new 30-day sweep, preset sites, and problem-oriented framing are implemented. Several submission-blocking issues were present and are addressed by the accompanying regression tests and this audit.

## Critical Findings (fixed in this pass)

1. **Import breakage** — `app.py` imported `sweep` while `geometry.py` did not define it. The endpoint would raise `ImportError` on startup. **Fixed** by completing the `sweep()` implementation.
2. **Missing UI** — Preset dropdown, sweep button, stats, and timeline canvas were not present in the committed template. **Fixed**.
3. **No regression coverage for new features** — Added `tests/test_sweep.py` and `tests/test_api.py`.

## Medium Findings

| ID | Area | Finding | Severity | Recommendation |
|----|------|---------|----------|----------------|
| RT-01 | API | No input length / range limits on `days` or `step_hours`. A client can request `days=10000`, causing long CPU-bound SPICE loops. | Medium | Cap `days` ≤ 90 and `step_hours` ≥ 0.25 in the API. |
| RT-02 | API | Broad `except Exception` returns raw exception text. Could leak internal paths or SPICE messages. | Low | Return generic 400 message; log details server-side. |
| RT-03 | Kernel loading | Startup fails hard if any kernel is missing (good), but the error is only stored and shown as a banner. No structured health endpoint. | Low | Add `/health` that reports kernel status without computation. |
| RT-04 | UI | Preset coordinates for Artemis III regions are approximate. Users may treat them as official. | Low | Label them clearly as approximate and link to NASA source. |
| RT-05 | Claims | Banner correctly frames power/comms as proxies. Limitations text is present. Risk remains that screenshots could be taken out of context. | Info | Keep the explicit limitation sentence on every result card. |

## Low / Informational

- Geometric-only computation is correctly documented and cannot be mistaken for terrain-masked or operational availability when the limitations text is read.
- No authentication is required (appropriate for a local/demo tool).
- JSON export contains full provenance; no secrets.
- Docker build downloads kernels at build time and verifies SHA-256 (good). Runtime has no network dependency.
- Near-pole guard correctly raises on exact ±90°.

## Regression Tests Added

- `tests/test_sweep.py`: shape, single-epoch consistency, parameter validation, finite percentages.
- `tests/test_api.py`: Flask test client coverage for `/api/compute` and `/api/sweep` success and error paths.
- Existing `tests/test_geometry.py` still covers site vector, basic compute, and pole rejection.

Run with kernels present:
```bash
export AL2_KERNEL_DIR=kernels
pytest tests/ -q
```

## Submission Recommendation

Ready for owner review after the input-bounds hardening (RT-01) is applied. All scientific boundaries (DE421, geometric correction, 1737.4 km radius, terrain-free disclaimer) remain intact.
