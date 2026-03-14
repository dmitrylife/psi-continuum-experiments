from __future__ import annotations

import numpy as np
import pandas as pd


TIDAL_PERIODS_HOURS = {
    "M2": 12.4206,
    "S2": 12.0000,
    "K1": 23.9345,
    "O1": 25.8193,
}


def _time_hours(df: pd.DataFrame) -> np.ndarray:
    t0 = df["t"].iloc[0]
    return ((df["t"] - t0).dt.total_seconds() / 3600.0).to_numpy(dtype=float)


def build_reference(
    df: pd.DataFrame,
    method: str = "diurnal_mean",
) -> tuple[np.ndarray, dict]:
    """
    Build reference response h_eq(t) for a tide-gauge time series.

    Supported methods
    -----------------
    diurnal_mean
        Mean sea level by hour of day (24 discrete reference states).
    harmonic_4mode
        Continuous harmonic reference using M2, S2, K1, O1 constituents.
    """
    if df.empty:
        raise ValueError("Input dataframe is empty.")

    if method == "diurnal_mean":
        return _build_diurnal_mean(df)

    if method == "harmonic_4mode":
        return _build_harmonic_4mode(df)

    raise ValueError(f"Unsupported reference method: {method}")


def _build_diurnal_mean(df: pd.DataFrame) -> tuple[np.ndarray, dict]:
    hours = df["t"].dt.hour.to_numpy()
    h_obs = df["h_mm"].to_numpy()

    h_eq_hour = np.full(24, np.nan, dtype=float)

    for h in range(24):
        mask = hours == h
        if np.any(mask):
            h_eq_hour[h] = np.nanmean(h_obs[mask])

    if np.any(np.isnan(h_eq_hour)):
        idx = np.arange(24)
        good = ~np.isnan(h_eq_hour)
        if np.sum(good) < 2:
            raise ValueError("Not enough valid hourly bins to build diurnal reference.")
        h_eq_hour = np.interp(idx, idx[good], h_eq_hour[good])

    h_eq_mm = h_eq_hour[hours]

    info = {
        "method": "diurnal_mean",
        "hourly_reference_mm": h_eq_hour.tolist(),
    }
    return h_eq_mm, info


def _build_harmonic_4mode(df: pd.DataFrame) -> tuple[np.ndarray, dict]:
    t_hours = _time_hours(df)
    h_obs = df["h_mm"].to_numpy(dtype=float)

    # Design matrix: constant + cos/sin pairs
    cols = [np.ones_like(t_hours)]
    labels = ["const"]

    for name, period in TIDAL_PERIODS_HOURS.items():
        omega = 2.0 * np.pi / period
        cols.append(np.cos(omega * t_hours))
        cols.append(np.sin(omega * t_hours))
        labels.append(f"{name}_cos")
        labels.append(f"{name}_sin")

    X = np.column_stack(cols)

    # Least-squares fit
    beta, *_ = np.linalg.lstsq(X, h_obs, rcond=None)
    h_eq_mm = X @ beta

    coeffs = {label: float(val) for label, val in zip(labels, beta)}

    info = {
        "method": "harmonic_4mode",
        "constituents_hours": TIDAL_PERIODS_HOURS,
        "coefficients": coeffs,
    }
    return h_eq_mm, info


def harmonic_phase_4mode(df: pd.DataFrame) -> np.ndarray:
    """
    Simple tidal phase proxy based on the dominant M2 constituent.

    Returns phase in radians in [-pi, pi].
    """
    t_hours = _time_hours(df)
    period = TIDAL_PERIODS_HOURS["M2"]
    omega = 2.0 * np.pi / period
    phase = (omega * t_hours + np.pi) % (2.0 * np.pi) - np.pi
    return phase
