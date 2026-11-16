# Third-party kernel notice

The Docker image built from this repository contains the five unmodified NAIF SPICE kernels listed in [KERNEL_MANIFEST.md](KERNEL_MANIFEST.md). The image build downloads and verifies them. Their source archive paths and SHA-256 values are recorded in the manifest.

NAIF's [SPICE use rules](https://naif.jpl.nasa.gov/naif/rules.html), under “Kernels Redistribution,” permit redistribution of NAIF-distributed SPICE kernels provided they have not been modified. The image includes the files unmodified. NAIF encourages acknowledgement of SPICE and the teams that provided kernel data.

The project [MIT License](../LICENSE) applies to Ashura's Light 2 project code; it does not relicense these kernels. Kernels obtained from sources other than NAIF may have different terms. See the linked NAIF rules for full terms and disclaimers.
