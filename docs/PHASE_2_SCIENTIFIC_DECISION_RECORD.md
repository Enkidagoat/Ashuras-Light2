# PHASE 2 SCIENTIFIC DECISION RECORD
## Ashura's Light 2 — Lunar South-Pole Landing Site Navigator
**Date:** 2026-11-15  
**Status:** Research reconciliation complete. No owner decisions pre-approved.  
**Current baseline commit:** 45734d43261b12c75d744cfbac0c559f9df979d1  

## Executive Decision
A bounded geometric centre-direction calculation for Sun and Earth azimuth/elevation is technically feasible and supported by the reconciled research. Terrain-aware visibility, power prediction, communications availability, and landing safety remain excluded from any MVP. No calculation convention is approved for production until the owner explicitly accepts the provisional recommendations below.

## Evidence Reviewed
- Phase 1 documents (PRODUCT_BRIEF, USER_WORKFLOW, TECHNICAL_ARCHITECTURE, DATA_PROVENANCE, ACCEPTANCE_CRITERIA, DECISIONS, README)
- SCIENTIFIC_METHODS_REVIEW.md
- COORDINATE_SYSTEMS_AND_TIME.md
- EPHEMERIS_AND_DATA_SOURCE_AUDIT.md
- LUNAR_TERRAIN_DATA_REVIEW.md
- POWER_AND_COMMUNICATIONS_LIMITATIONS.md
- VERIFICATION_PLAN.md
- MVP_FEASIBILITY_AND_RECOMMENDATIONS.md

## Confirmed Findings
- Geometric centre-direction AZ/EL relative to a named local horizontal frame is a well-defined mathematical operation (NAIF SPICE / Horizons).
- Horizons quantity 4 returns apparent AZ/EL; SPICE NONE is geometric; LT and LT+S are distinct.
- ME and PA frames are not interchangeable; DE421 ME/PA rotation is approximately 0.0288°.
- Smooth-body geometric horizon ≠ terrain-aware visibility ≠ operational visibility.
- Geometric solar elevation ≠ usable electrical power.
- Geometric Earth visibility ≠ operational communication availability.
- A DE421/MOON_ME_DE421 vs Horizons DE441/MEAN_ME comparison is a cross-check, not a fully controlled matched validation.

## Provisional Findings
- Planetocentric latitude, east-positive longitude, and a 1,737.4 km reference sphere are defensible interoperability defaults (USGS/LRO literature).
- Local SPICE with pinned kernels is preferable for reproducibility; Horizons is a useful independent check but shares JPL ephemeris heritage.
- DE440 FK/PCK filename discrepancy remains unresolved (moon_de440_200625.tf named in PCK comment vs moon_de440_250416.tf observed in directory).

## Unresolved Questions
- Exact compatible DE440 (or other) kernel stack.
- Production geometric vs apparent mode.
- Longitude serialization domain (0–360 vs −180–+180).
- Exact-pole tangent basis.
- Approved data-source licenses.
- Owner-defined numeric tolerance.

## Recommended Defaults (all OWNER DECISION REQUIRED)
| Decision | Proposed Recommendation | Status |
|---|---|---|
| Intended product use | Exploratory geometry and education | OWNER DECISION REQUIRED |
| Coordinate convention | Planetocentric, positive-east | OWNER DECISION REQUIRED |
| Reference frame | Explicitly pinned ME realization | OWNER DECISION REQUIRED |
| Reference radius | 1,737.4 km, provisional | OWNER DECISION REQUIRED |
| Height handling | Explicitly declared; no silent assumptions | OWNER DECISION REQUIRED |
| Exact-pole handling | Require explicit tangent basis | OWNER DECISION REQUIRED |
| Time input | UTC, converted with pinned LSK | OWNER DECISION REQUIRED |
| Calculation mode | Geometric centre-direction baseline | OWNER DECISION REQUIRED |
| Terrain visibility | Excluded from MVP | OWNER DECISION REQUIRED |
| Power prediction | Excluded from MVP | OWNER DECISION REQUIRED |
| Communications availability | Excluded from MVP | OWNER DECISION REQUIRED |
| Landing safety | Excluded from MVP | OWNER DECISION REQUIRED |

## Risks and Consequences
- Approving geometric mode without documenting the difference from Horizons apparent will produce small but real residuals.
- Leaving the DE440 stack unresolved blocks pinning a current-century kernel set.
- Treating the DM2 comparison as controlled validation overstates the evidence.

## Explicit Owner Approval Fields
No decision above is approved. Owner must explicitly accept or amend each item before architecture is authorized.
