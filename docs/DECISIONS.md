# Decisions — Ashura's Light 2

## Established by Project Owner
- Product identity: clean-room build of the Lunar Landing Site Navigator (NASA Space Apps Challenge).
- Not a continuation or migration of any previous implementation.
- Intended users: mission planners, educators, public users.
- Purpose: compare candidate lunar south-pole sites and dates using Sun and Earth geometry relative to the local horizon.
- Required distinctions: geometric visibility ≠ usable power, ≠ operational communications, ≠ terrain-verified visibility.
- Repository: holeyfield33-art/ashuras-light2

## Proposed MVP candidates (for owner review — not yet final)
- Lunar site selection by coordinates
- Date/time selection
- Sun azimuth and elevation
- Earth azimuth and elevation
- Site/date comparison
- Clear horizon-relative presentation
- Provenance and limitations accompanying results

## Explicit non-goals
- Terrain-masked illumination
- Guaranteed power or communications claims
- Decorative 3D
- Code or data migration from previous repositories

## Unresolved
- Approved data sources and licenses
- Production calculation convention (geometric vs apparent)
- Exact comparison UI
- Deployment domain
- Final numeric tolerance

Phase 1 must be explicitly accepted by the Project Owner before architecture or implementation is authorized.
