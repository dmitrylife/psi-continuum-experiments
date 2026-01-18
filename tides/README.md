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

This reference plays the role of an idealized, instantaneous response
to the external tidal potential.

## Diagnostic field Ψ

The diagnostic field Ψ(t) is defined as the deviation of the observed
sea level from the reference response, normalized by a characteristic
tidal amplitude:

Ψ(t) = (h_obs(t) − h_eq(t)) / A

This field captures phase shifts, dissipation, and regime changes in a
coordinate-independent way.

## Pipeline

1. Load raw tide-gauge data
2. Construct reference response h_eq(t)
3. Compute diagnostic field Ψ(t)
4. Analyze trajectories in time and state space
5. Produce reproducible figures and summary metrics

The tidal experiment serves as a proof of concept for interpreting
acceleration-like effects as response phenomena rather than new forces.
