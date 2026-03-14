from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


def robust_amplitude(h_mm: np.ndarray) -> float:
    """
    Robust amplitude scale:
        A = 0.5 * (p95 - p5)
    """
    p5 = np.nanpercentile(h_mm, 5)
    p95 = np.nanpercentile(h_mm, 95)
    A = 0.5 * (p95 - p5)
    return float(A if A > 0 else 1.0)


def compute_psi(h_obs_mm: np.ndarray, h_eq_mm: np.ndarray, A: float) -> np.ndarray:
    """
    Compute diagnostic field:
        Psi(t) = (h_obs - h_eq) / A
    """
    if A <= 0:
        raise ValueError("Amplitude scale A must be positive.")
    return (h_obs_mm - h_eq_mm) / A


def skewness(x: np.ndarray) -> float:
    """
    Simple skewness estimator without scipy.
    """
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 3:
        return float("nan")
    mu = np.mean(x)
    sigma = np.std(x)
    if sigma == 0:
        return 0.0
    return float(np.mean(((x - mu) / sigma) ** 3))


def summarize_metrics(
    df: pd.DataFrame,
    h_eq_mm: np.ndarray,
    psi: np.ndarray,
    A_mm: float,
    station: str,
    source_file: str,
    start: str,
    end: str,
    reference_method: str,
) -> dict[str, Any]:
    """
    Collect run-level metrics.
    """
    n_points = int(len(df))
    total_hours = np.nan
    missing_frac = np.nan

    if n_points >= 2:
        dt_seconds = df["t"].diff().dropna().dt.total_seconds().median()
        if pd.notna(dt_seconds) and dt_seconds > 0:
            total_hours = (df["t"].iloc[-1] - df["t"].iloc[0]).total_seconds() / 3600.0
            expected_n = int(round(total_hours / (dt_seconds / 3600.0))) + 1
            if expected_n > 0:
                missing_frac = max(0.0, 1.0 - n_points / expected_n)

    metrics = {
        "station": station,
        "source_file": source_file,
        "start": start,
        "end": end,
        "reference_method": reference_method,
        "n_points": n_points,
        "missing_frac": None if np.isnan(missing_frac) else float(missing_frac),
        "A_mm": float(A_mm),
        "h_obs_mean_mm": float(np.nanmean(df["h_mm"].to_numpy())),
        "h_eq_mean_mm": float(np.nanmean(h_eq_mm)),
        "psi_mean": float(np.nanmean(psi)),
        "psi_rms": float(np.sqrt(np.nanmean(psi**2))),
        "psi_max_abs": float(np.nanmax(np.abs(psi))),
        "psi_skew": skewness(psi),
    }
    return metrics

