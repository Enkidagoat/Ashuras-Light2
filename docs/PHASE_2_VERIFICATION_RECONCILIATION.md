# PHASE 2 VERIFICATION RECONCILIATION
## Ashura's Light 2
**Date:** 2026-11-15  
**Status:** Existing DM2 comparison correctly bounded as a cross-check, not a controlled matched validation.

## What the DM2 Comparison Actually Was
- Site: literature point DM2 (84°12′5.61″ S, 60°41′59.61″ E), interpreted provisionally as planetocentric, east-positive, zero height on 1,737.4 km sphere, MOON_ME_DE421.
- Local path: CSPICE N0067 azlcpo, ELLIPSOID, LT+S, MOON_ME_DE421, DE421 kernels.
- Horizons path: quantity 4 apparent AZ/EL, airless, MEAN_ME (high precision), DE441.
- Maximum absolute residual: 8.6031×10⁻⁶ degrees.

## Why It Is Not Fully Controlled
1. Different ephemeris realizations (DE421 vs DE441).
2. Different frame realizations (MOON_ME_DE421 vs Horizons MEAN_ME).
3. Source coordinate metadata (latitude type, frame, height) was missing from the literature point and supplied as a test assumption.
4. Correction mode was matched to apparent (LT+S) but the frames were not identical.
5. No owner-approved tolerance existed.

The small residual demonstrates computational-path consistency under related but non-identical models. It does not validate the underlying ephemeris, the source coordinate, or any operational claim.

## Matched Comparison Feasibility
A genuinely matched comparison (identical kernels, identical frame, identical correction mode, identical site definition) is feasible with free tools if:
- The same SPK/PCK/FK/LSK set is used on both sides, or
- Horizons is configured to a known matching model and the response header is archived confirming the match.

This was not performed in the existing research. The current comparison must not be substituted for a controlled matched validation.

## Required for a Controlled Validation
- Identical kernel set (or explicitly documented and accepted difference).
- Identical frame realization.
- Identical site vector and height datum.
- Identical correction mode.
- Archived full Horizons response header.
- Pre-declared tolerance.

Until these exist, verification status for production remains PARTIAL.
