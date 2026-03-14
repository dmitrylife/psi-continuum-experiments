# Tidal Dynamics Experiment

This experiment uses tidal sea-level observations as a clean macroscopic system  
for illustrating the **Ψ-Continuum response framework**.

Tides provide a physically transparent example of a global system response.  
The ocean reacts to external gravitational forcing (Lunar and Solar tidal potential)  
through a combination of:

- phase delay  
- dissipation  
- basin geometry  
- nonlinear hydrodynamic effects  

rather than through purely local forces.

This makes tidal dynamics a useful macroscopic testbed for studying  
how response fields emerge in real physical systems.

## Data

The experiment uses tide-gauge time series (hourly resolution or finer)  
obtained from established observational networks such as:

- PSMSL  
- NOAA  
- national oceanographic services  

Only **raw sea-level measurements** are used.  
No long-term sea-level trend removal or climate corrections are applied,  
because the analysis focuses on **dynamical response modes** rather than secular evolution.

**Example dataset** used in the current experiment:

```
tides/data/raw/h293.dat.txt
```

## Reference Response

The analysis requires a reference equilibrium response **h_eq(t)**  
representing the leading tidal behavior.

Two reference constructions are implemented:

### 1. Mean diurnal cycle
An empirical reference obtained by averaging sea level by hour of day:

```
h_eq(t) = mean sea level at hour(t)
```


This removes slow background variability but leaves most tidal oscillations in the residual.

### 2. Harmonic reference
A minimal harmonic tidal model including the dominant constituents:

- M₂  
- S₂  
- K₁  
- O₁  

This model captures the primary tidal dynamics and substantially reduces the residual variance.

## Diagnostic Field Ψ

The diagnostic response field **Ψ(t)** is defined as:

$$
\Psi(t) = \frac{h_{\mathrm{obs}}(t) - h_{\mathrm{eq}}(t)}{A}
$$

where:

- $h_{\mathrm{obs}}(t)$ — observed sea level  
- $h_{\mathrm{eq}}(t)$ — reference response  
- $A$ — characteristic tidal amplitude  

The field **Ψ(t)** represents the normalized deviation of the system from its reference response.  
It compactly captures effects such as:

- phase shifts  
- dissipation  
- nonlinear hydrodynamic response  
- unresolved forcing  

in a coordinate-independent form.

## Analysis Pipeline

The experiment is implemented as a reproducible data pipeline. Steps:

1. Load raw tide-gauge observations  
2. Construct reference response **h_eq(t)**  
3. Compute diagnostic field **Ψ(t)**  
4. Analyze trajectories in time and state space  
5. Compute diagnostic metrics  
6. Generate reproducible figures  

Implementation:

- Main pipeline logic: `tides/src/pipeline.py`  
- Execution scripts: `tides/scripts/`

## Running the Experiment

```bash
# Clone repository
git clone https://github.com/dmitrylife/psi-continuum-experiments.git
cd psi-continuum-experiments

# Create and activate virtual environment
python3 -m venv sci_venv
source sci_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the tidal experiment
python -m tides.scripts.02_run
```

## Outputs

Results are written to:

```
tides/artifacts/
```

For each station and each time window, the pipeline creates:

```
tides/artifacts/<station>/<window>/
```

containing:

- `figures/`
- `results/`

### Figures

#### Reference response
- `heq_diurnal_cycle.png`
- `heq_timeseries.png`

#### Diagnostic field
- `psi_tides.png`

#### State-space diagnostics
- `psi_state_space.png`
- `psi_state_space_density.png`

#### Phase diagnostics
- `psi_vs_phase.png`
- `psi_vs_phase_binned.png`

#### Velocity diagnostics
- `psi_vs_dheqdt.png`
- `psi_vs_dheqdt_binned.png`

These plots illustrate the structure of the residual response field  
relative to tidal phase and reference velocity.

## Results Summary

A concise summary of the current experiment results is available in:

```
tides/results/summary.md
```

This document reports:

- residual statistics  
- diagnostic plots  
- interpretation of the **Ψ** response field

## Purpose of the Experiment

The tidal system serves as a macroscopic **proof-of-concept** for the **Ψ-Continuum framework**.

The goal is to demonstrate how a suitably chosen diagnostic field can cleanly separate:

**reference behavior**  
vs  
**system response**

in real observational data.

In this sense, tidal dynamics provide a controlled example of how acceleration-like behavior can emerge from:

- response geometry  
- phase structure  
- dissipation  

without introducing additional forces or microscopic modifications to the governing dynamics.

