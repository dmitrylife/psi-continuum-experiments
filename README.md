# psi-continuum-experiments

> **Companion demonstrations (ongoing)**

This repository contains a collection of **macroscopic experiments**
illustrating the **Psi-Continuum response framework**.

The goal is to demonstrate how acceleration-like or anomalous behavior
can emerge in real physical systems as a **global response**, driven by

- geometry
- phase shifts
- dissipation
- system memory

without introducing new forces or modifying microscopic dynamics.

Each experiment is implemented as a reproducible pipeline:

`raw data → reference response → diagnostic field Ψ → state-space diagnostics`

The repository complements the **Psi-Continuum cosmology framework**
and serves as a laboratory for testing response-based diagnostics on
well-understood macroscopic systems.

---

# Experiments

## Tidal dynamics (`tides/`)

The first experiment studies **ocean tidal response dynamics**
using tide-gauge observations.

Tides provide a clean macroscopic example of a system responding to
external forcing (Lunar and Solar tidal potential) through

- phase delay
- dissipation
- basin geometry
- nonlinear hydrodynamics

rather than purely local forces.

This makes tidal dynamics an ideal testbed for the **Ψ diagnostic
framework**.

---

# How to run

Clone the repository and install dependencies:

```bash
git clone https://github.com/dmitrylife/psi-continuum-experiments.git
cd psi-continuum-experiments

python3 -m venv sci_venv
source sci_venv/bin/activate

pip install -r requirements.txt
```

A minimal demonstrator can be executed with:

```
python -m tides.scripts.02_run
```

This script simply runs the pipeline for a predefined dataset and
produces example diagnostic figures.

## ⚠️ Note:
The full experiment pipeline, additional scripts, and detailed
instructions are documented in:

```
tides/README.md
```

---

# Outputs

Experiment outputs are written to:

```
tides/artifacts/
```

Typical diagnostics include:

- tidal response time series
- state-space trajectories
- phase diagnostics
- velocity diagnostics
- statistical summaries

---

# Results summary

A short overview of the current tidal experiment results is available in:

```
tides/results/summary.md
```

# Repository status

This repository is intended as a **growing collection of
response-diagnostic experiments**.

Future experiments may include:

- atmospheric oscillations
- hydrological systems
- laboratory oscillators
- additional observational datasets

Each experiment will be implemented as a reproducible pipeline following
the same **reference → response → state-space** methodology.

