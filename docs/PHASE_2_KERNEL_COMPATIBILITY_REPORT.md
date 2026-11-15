# PHASE 2 KERNEL COMPATIBILITY REPORT
## Ashura's Light 2
**Date:** 2026-11-15  
**Status:** Compatibility of a current DE440 stack is UNRESOLVED.

## Observed Discrepancy
The binary lunar PCK `moon_pa_de440_200625.bpc` comment names the frame kernel `moon_de440_200625.tf`.  
The current NAIF generic FK directory listed `moon_de440_250416.tf` at research time.  

This is a filename/source discrepancy, not proof of incompatibility. Compatibility was not demonstrated.

## DE421 Stack (executed in research)
The following combination was loaded and executed successfully for the DM2 cross-check:
- de421.bsp
- moon_pa_de421_1900-2050.bpc
- moon_080317.tf
- pck00011.tpc
- naif0012.tls
- Frame: MOON_ME_DE421

SHA-256 values were recorded in VERIFICATION_PLAN.md. Coverage for lunar orientation: 1900–2051.

## Frame Identifiers
- MOON_ME_DE421 and MOON_PA_DE421 are distinct (rotation ~0.0288°).
- Horizons MEAN_ME (high precision) with DE441 is not identical to MOON_ME_DE421.
- IAU_MOON is a different realization.

These frames must not be treated as interchangeable.

## Compatibility Conclusion
- DE421 stack: CONFIRMED compatible for the executed test.
- DE440 stack: UNRESOLVED. The named FK was not inspected against the directory file. No replacement stack is selected by assumption.

## Required Before Any DE440 Adoption
1. Inspect the actual frame-kernel comment, frame IDs, aliases, and PCK references.
2. Confirm coverage pairing with the binary PCK.
3. Record SHA-256 and retrieval date.
4. Demonstrate a successful load and a known-site calculation.

Until these steps are completed, the project cannot pin a DE440 kernel stack.
