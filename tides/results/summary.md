# Ψ-response diagnostics in tidal state space

## Preliminary experiment summary

### 1. Dataset

- **Station**: h293  
- **Source file**: h293.dat.txt  

**Time windows analyzed:**

| Period             | Points |
|--------------------|--------|
| 1959-01-01 → 1959-01-31 | 721    |
| 1959-02-01 → 1959-02-28 | 649    |
| 1959-03-01 → 1959-03-31 | 721    |

Sampling is regular and contains **no missing values**.

### 2. Reference models

Two reference constructions were tested.

#### 2.1 Diurnal mean reference
Reference level defined by mean tidal cycle.  
Residual amplitude:

**Ψ_rms ≈ 0.58–0.60**

→ Diurnal averaging removes only the slow background and leaves most tidal variability in the residual.

#### 2.2 Harmonic reference (4 modes)
Harmonic model including dominant constituents:

- M₂  
- S₂  
- K₁  
- O₁  

**Residual statistics for January:**

- A_mm        = 777.0 mm  
- ψ_mean      ≈ 0  
- ψ_rms       = 0.188  
- ψ_max_abs   = 0.599  
- ψ_skew      = 0.185  

**RMS reduction:**

ψ_rms : 0.60 → 0.19

→ Dominant tidal signal is well captured by the harmonic model.

### 3. State-space diagnostics

The experiment analyzes tidal dynamics in state-space representation:

**(h_eq(t), Ψ(t))**

where

**Ψ(t) = (h_obs(t) − h_eq(t)) / A**

(A — observed tidal amplitude)

**Observed features:**

State-space trajectories form a dense but bounded cloud:

- **Ψ** ∈ [−0.6, 0.6]  
- **h_eq** ∈ [1100, 1600] mm  

The structure appears stable across time windows.

### 4. Phase diagnostics

**Scatter plot:** Ψ vs tidal phase

**Results:**

- Distribution is nearly uniform across phase  
- No sinusoidal dependence is visible  
- Binned mean: ⟨Ψ⟩(phase) ≈ 0 (within statistical uncertainty)

**Interpretation:**  
Residual response is **not phase-locked** to the tidal cycle once the main harmonic constituents are removed.

### 5. Velocity diagnostics

Computed derivative of the harmonic reference:

**v_eq(t) = dh_eq/dt**

**Diagnostics performed:**

- Ψ vs dh_eq/dt  
- Mean Ψ vs dh_eq/dt  

**Observations:**

- No strong linear relation  
- Weak nonlinear trend in binned averages  
- Magnitude small compared to scatter  

**Typical values:**

- |⟨Ψ⟩| ≤ 0.1  
- σ ≈ 0.2  

**Interpretation:**  
Residual Ψ does **not** follow a simple velocity-proportional response law  
**Ψ ∝ dh_eq/dt**  

Instead, it reflects a more complex macroscopic response.

### 6. Key results

1. Harmonic reference removes the dominant tidal signal.  
2. Residual Ψ field remains bounded and stable.  
3. Residual response is **not phase-locked** to the tidal cycle.  
4. Residual response is **not linearly velocity-locked** either.  
5. Weak nonlinear structure may remain, suggesting additional physical processes.

### 7. Interpretation

The residual field **Ψ** can be interpreted as a **macroscopic response field** describing deviations of the observed system from the leading harmonic tidal model.

Possible contributing factors:

- hydrodynamic nonlinearities  
- basin geometry  
- friction and dissipation  
- meteorological forcing  
- unresolved tidal constituents  

The Ψ-representation provides a compact diagnostic coordinate for studying such effects.

### 8. Next steps

Planned extensions of the experiment:

1. Repeat diagnostics for additional months and stations  
2. Compute cross-correlations:  
   - Ψ vs dh_eq/dt  
   - Ψ vs h_eq  
   - Ψ vs phase  
3. Analyze persistence and autocorrelation of Ψ  
4. Compare with extended harmonic models (more constituents)  
5. Test whether Ψ exhibits universal statistical properties across locations

### 9. Conclusion

The experiment demonstrates that the **Ψ-state-space representation** provides a useful diagnostic framework for tidal systems.

After removal of the dominant harmonic structure, the residual field **Ψ** captures remaining macroscopic dynamics that are **not trivially reducible** to tidal phase or velocity alone.

Further analysis across datasets will clarify whether these residual structures contain systematic physical information

