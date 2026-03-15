# psi-continuum-experiments

## Overview

This repository contains small macroscopic experiments designed to test
the Ψ-Continuum response framework using real observational data.

> **Companion demonstrations (ongoing)**

This repository collects macroscopic experiments illustrating the
**Psi-Continuum response framework**.

The goal is to demonstrate how apparent acceleration-like or anomalous
behavior may emerge in real physical systems as a **global response**,
driven by geometry, phase shifts, dissipation, and system memory —
without introducing new forces or modifying microscopic dynamics.

Each experiment is based on real observational data and is implemented
as a reproducible analysis pipeline:

raw data → reference response → diagnostic field Ψ → state-space analysis.

The repository complements the Psi-Continuum cosmology releases and
serves as a laboratory for testing the universality of the response
description across different macroscopic systems.

---

# Repository status

This repository is intended as a **growing collection of diagnostic
experiments**.

New macroscopic systems and datasets will be added as the framework is
extended and tested.

Current experiment:

- tidal dynamics (ocean tide gauge response)

Future candidates may include:

- atmospheric oscillations  
- hydrological systems  
- mechanical oscillators  
- laboratory response experiments  

---

# Experiments

## Tidal dynamics (`tides/`)

The `tides/` module contains a complete reproducible experiment
analyzing **tidal response dynamics** using tide-gauge observations.

Tides provide a clean macroscopic example of a system responding to
external forcing (Lunar and Solar tidal potential) through

- phase delay
- dissipation
- basin geometry
- nonlinear hydrodynamic effects

rather than purely local forces.

### What the experiment includes

- Raw tide-gauge data  
- Construction of reference tidal response `h_eq(t)` 
- Diagnostic response field **Ψ(t)**  
- State-space diagnostics of the residual dynamics  
- Reproducible figures and statistical summaries  

### Running the experiment

From the repository root:

```bash
python -m tides.scripts.02_run
```
## Outputs

Results are written to:

```
tides/artifacts/
```

For each station and time window, the pipeline generates:

```
tides/artifacts/<station>/<window>/
```

containing:

- `figures/`
- `results/`

### Typical diagnostic plots

- `psi_tides.png` — diagnostic field **Ψ(t)** (time series)  
- `psi_state_space.png` — state-space trajectory  
- `psi_state_space_density.png` — state-space density / heatmap  
- `psi_vs_phase.png` — **Ψ** vs tidal phase (scatter)  
- `psi_vs_phase_binned.png` — mean **⟨Ψ⟩** vs phase (binned)  
- `psi_vs_dheqdt.png` — **Ψ** vs reference velocity **dh_eq/dt**  
- `psi_vs_dheqdt_binned.png` — mean **⟨Ψ⟩** vs velocity (binned)  

These diagnostics illustrate how the residual response field Ψ
depends on tidal phase and reference dynamics.

## Results Summary

A short overview of the current tidal experiment results is available in:

```
tides/results/summary.md
```

This document summarizes:

- residual statistics  
- diagnostic plots  
- interpretation of the **Ψ** response field

## Purpose

The goal of this repository is to demonstrate how  
**response-based state-space diagnostics** can reveal hidden structure  
in macroscopic systems that would otherwise appear as anomalous  
or acceleration-like behavior.

The tidal experiment serves as a controlled **proof-of-concept**  
for the **Ψ-Continuum framework** using real observational data.

