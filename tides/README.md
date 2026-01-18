# Tidal dynamics experiment

This experiment uses tidal sea-level data as an illustrative macroscopic
system for the Psi-Continuum framework.

Tides provide a physically transparent example of a global system
response: the ocean reacts to an external gravitational driver
(Lunar/Solar tidal potential) with phase delay, dissipation, and
geometry-dependent amplification, rather than through local forces.

## Data

The experiment is based on tide-gauge time series (hourly or finer),
obtained from established observational networks such as PSMSL, NOAA,
or equivalent national services.

Only raw sea-level measurements are used.
No long-term sea-level trend or climate correction is required, as the
focus is on dynamical response modes rather than secular evolution.

## Reference response

A reference equilibrium or harmonic tidal response `h_eq(t)` is
constructed using a minimal set of dominant tidal components or a
smoothed mean cycle.

In the current implementation, the reference response is defined
empirically as a **mean diurnal cycle**, obtained by averaging the
observed sea level by hour of day.

This reference plays the role of an idealized, instantaneous response
to the external tidal potential.

## Diagnostic field Ψ

The diagnostic field Ψ(t) is defined as the deviation of the observed
sea level from the reference response, normalized by a characteristic
tidal amplitude:

$$
\Psi(t) = \frac{h_{\mathrm{obs}}(t) - h_{\mathrm{eq}}(t)}{A}
$$

This field captures phase shifts, dissipation, and regime changes in a
coordinate-independent way.

## Pipeline

1. Load raw tide-gauge data
2. Construct reference response `h_eq(t)`
3. Compute diagnostic field `Ψ(t)`
4. Analyze trajectories in time and state space
5. Produce reproducible figures and summary metrics

## How to run

From the repository root, execute:

```bash
git clone https://github.com/dmitrylife/psi-continuum-experiments.git
cd psi-continuum-experiments
python3 -m venv sci_venv
source sci_venv/bin/activate
pip install -r requirements.txt
```

```bash
python -m tides.scripts.02_run
```

The script reads raw data from:

```text
tides/data/raw/h293.dat.txt
```

which follows a standard hourly tide-gauge format with intra-day phase segmentation.

## Outputs

After execution, the following figures are generated in:

```
tides/figures/
```

## Reference response

```
heq_diurnal_cycle.png
```

This figure shows the empirically reconstructed mean diurnal tidal
cycle, serving as the reference response h_eq(t).

## Diagnostic field

```
psi_tides.png
```

This figure shows the diagnostic field `Ψ(t)` for the first days of the
time series. The resulting trajectories exhibit coherent oscillatory
structure and amplitude modulation, demonstrating that
acceleration-like behavior can arise as a **global response mode** of a
macroscopic dissipative system, without invoking additional forces.

## Purpose

The tidal experiment serves as a proof of concept for the
Psi-Continuum framework, illustrating how a suitable state-space
diagnostic separates reference behavior from response-induced structure
in real observational data.

In this sense, the tidal system provides a controlled macroscopic example
of how acceleration-like effects can emerge from response geometry and
phase structure rather than from additional dynamical components.
