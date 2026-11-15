# PHASE 2 CALCULATION CONTRACT
## Ashura's Light 2
**Date:** 2026-11-15  
**Status:** Proposed. All items OWNER DECISION REQUIRED unless marked CONFIRMED.

## Proposed Contract (Provisional)

| Element | Proposed Value | Status |
|---|---|---|
| Latitude type | Planetocentric | OWNER DECISION REQUIRED |
| Longitude sign | Positive east | OWNER DECISION REQUIRED |
| Longitude domain | Preserve source; normalize explicitly for output | OWNER DECISION REQUIRED |
| Reference frame | Explicitly pinned ME realization | OWNER DECISION REQUIRED |
| Site height | Explicitly declared; default 0 km above 1,737.4 km sphere only if labelled provisional | OWNER DECISION REQUIRED |
| Reference surface | Sphere, radius 1,737.4 km | OWNER DECISION REQUIRED |
| Exact-pole behavior | Azimuth undefined until explicit tangent basis supplied | OWNER DECISION REQUIRED |
| Time input | UTC string preserved; convert via pinned LSK to ET/TDB | CONFIRMED (method) |
| Correction mode | Geometric (SPICE NONE) as baseline; apparent only if explicitly selected and labelled | OWNER DECISION REQUIRED |
| Target semantics | Centre direction only | OWNER DECISION REQUIRED |
| Azimuth | Clockwise from local north | OWNER DECISION REQUIRED |
| Elevation | Relative to plane perpendicular to local radial up | OWNER DECISION REQUIRED |
| Output units | Degrees, full precision retained internally | OWNER DECISION REQUIRED |
| Provenance | Source, version, frame, LSK, correction mode, limitations attached to every result | CONFIRMED (requirement) |

## Evidence-Backed Recommendations
- Preserve source-native coordinates and label any provisional interpretation.
- Do not use Moon-centre direction as a site-relative direction (omit lunar-radius parallax).
- Record both UTC and ET/TDB.
- Never equate geometric and apparent results.

## Decisions Requiring Owner Approval
All rows marked OWNER DECISION REQUIRED above. No item is approved.
