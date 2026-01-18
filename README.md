# psi-continuum-experiments

This repository collects macroscopic experiments illustrating the
Psi-Continuum response framework.

The goal is to demonstrate how apparent acceleration-like or anomalous
behavior can emerge in real physical systems as a global response,
driven by geometry, phase shifts, dissipation, and system memory —
without introducing new forces or microscopic dynamics.

Each experiment is based on real observational data and is designed as
a reproducible, minimal pipeline:
raw data → reference response → diagnostic field Ψ → state-space analysis.

The repository is complementary to the Psi-Continuum cosmology releases
and serves as a laboratory for testing the universality of the response
and state-space description across different macroscopic systems.

The first experiment focuses on tidal dynamics as a clean and physically
transparent proof of concept.

## Experiments

This repository includes a set of macroscopic, data-driven experiments
demonstrating the Psi-Continuum response framework on real physical systems.

### Tidal dynamics (`tides/`)

The `tides/` directory contains a complete, reproducible tidal response
experiment based on tide-gauge observations.

**What it contains**
- Raw hourly tide-gauge data (`tides/data/raw/h293.dat.txt`)
- A reference response constructed as a mean diurnal tidal cycle
- A diagnostic response field Ψ(t) capturing phase shifts and dissipation
- Reproducible figures illustrating the response structure

**How to run**
From the repository root:

```bash
python -m tides.scripts.02_run
```

## Outputs

After execution, the following figures are generated in:

```
tides/figures/
```

- heq_diurnal_cycle.png — empirical reference response h_eq​(t)
- psi_tides.png — diagnostic response field Ψ(t)

These results demonstrate how acceleration-like behavior can emerge as a
global response mode of a macroscopic dissipative system, without invoking
additional forces.
