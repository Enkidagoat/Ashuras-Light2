# Product Brief — Ashura's Light 2

**Status:** Phase 1 — Owner-authorized product definition.

## Problem the product solves
Mission planners, educators, and public users need an intuitive way to compare candidate lunar south-pole landing sites and dates using Sun and Earth geometry relative to the local horizon.

## Intended users
- Mission planners
- Educators
- Public users

## Primary user workflow
Select a lunar site and date/time → view Sun and Earth azimuth/elevation relative to the local horizon → compare another site or date → inspect provenance and limitations.

## Data the product requires
- Lunar site coordinates
- Observation epoch
- Ephemeris data sufficient to compute Sun and Earth centre-direction geometry
**UNRESOLVED:** specific approved sources and versions.

## What the product must produce
- Solar azimuth and elevation (centre-direction, relative to local horizon)
- Earth azimuth and elevation (centre-direction, relative to local horizon)
- Side-by-side or sequential comparison of sites or dates
- Accompanying provenance and explicit limitations

## Claims that can be supported
Geometric centre-direction visibility of the Sun or Earth above the local horizon plane.

## Claims that must not be made
- Sun above horizon = guaranteed usable power
- Earth above horizon = guaranteed communications
- Geometric visibility = terrain-verified visibility
- Any visualization = validated scientific evidence

## Unknown or unverified
- Approved data sources and licenses
- Production calculation convention (geometric vs apparent)
- Terrain masking (explicitly out of MVP)
- Deployment domain

MVP candidates are listed for owner review in DECISIONS.md and are not yet final requirements.
