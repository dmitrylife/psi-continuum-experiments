from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_reference_cycle(hourly_reference_mm: list[float], outpath: Path) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 4))
    plt.plot(range(24), hourly_reference_mm, lw=2)
    plt.xlabel("Hour of day")
    plt.ylabel("Sea level (mm)")
    plt.title("Reference response h_eq: mean diurnal cycle")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_psi_timeseries(
    df: pd.DataFrame,
    psi: np.ndarray,
    outpath: Path,
    title: str,
    max_points: int = 24 * 14,
) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    n = min(len(df), max_points)
    t = df["t"].iloc[:n]

    plt.figure(figsize=(10, 4))
    plt.plot(t, psi[:n], lw=1)
    plt.axhline(0, color="k", ls="--", alpha=0.5)
    plt.xlabel("Time")
    plt.ylabel("Ψ(t)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_state_space(
    h_eq_mm: np.ndarray,
    psi: np.ndarray,
    outpath: Path,
    title: str = "State-space view: Ψ vs h_eq",
    max_points: int = 4000,
) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    if len(h_eq_mm) > max_points:
        idx = np.linspace(0, len(h_eq_mm) - 1, max_points).astype(int)
        x = h_eq_mm[idx]
        y = psi[idx]
    else:
        x = h_eq_mm
        y = psi

    plt.figure(figsize=(6, 5))
    plt.plot(x, y, lw=0.8)
    plt.xlabel("h_eq(t) [mm]")
    plt.ylabel("Ψ(t)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_state_space_density(
    h_eq_mm,
    psi,
    outpath,
):
    """
    Density view of state space: Ψ vs h_eq.
    """

    import matplotlib.pyplot as plt

    outpath.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(6,5))

    plt.hist2d(
        h_eq_mm,
        psi,
        bins=80,
        cmap="inferno"
    )

    plt.xlabel("h_eq(t) [mm]")
    plt.ylabel("Ψ(t)")
    plt.title("Conditional Ψ-distribution over reference states")

    plt.colorbar(label="Counts")

    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_reference_timeseries(
    df: pd.DataFrame,
    h_eq_mm: np.ndarray,
    outpath: Path,
    title: str,
    max_points: int = 24 * 14,
) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    n = min(len(df), max_points)
    t = df["t"].iloc[:n]

    plt.figure(figsize=(10, 4))
    plt.plot(t, df["h_mm"].iloc[:n], lw=1, label="h_obs")
    plt.plot(t, h_eq_mm[:n], lw=2, label="h_eq")
    plt.xlabel("Time")
    plt.ylabel("Sea level (mm)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_psi_vs_phase(
    phase: np.ndarray,
    psi: np.ndarray,
    outpath: Path,
    title: str = "Ψ vs tidal phase",
) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 5))
    plt.scatter(phase, psi, s=10, alpha=0.6)
    plt.xlabel("Tidal phase [rad]")
    plt.ylabel("Ψ(t)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_psi_vs_phase_binned(
    phase,
    psi,
    outpath,
    nbins=24,
):
    """
    Plot mean Ψ as a function of tidal phase.
    """

    import numpy as np
    import matplotlib.pyplot as plt

    outpath.parent.mkdir(parents=True, exist_ok=True)

    bins = np.linspace(-np.pi, np.pi, nbins + 1)
    centers = 0.5 * (bins[:-1] + bins[1:])

    mean = []
    std = []

    for i in range(nbins):
        m = (phase >= bins[i]) & (phase < bins[i + 1])
        if np.sum(m) > 2:
            mean.append(np.mean(psi[m]))
            std.append(np.std(psi[m]))
        else:
            mean.append(np.nan)
            std.append(np.nan)

    mean = np.array(mean)
    std = np.array(std)

    plt.figure(figsize=(7, 5))

    plt.plot(
        centers,
        mean,
        marker="o",
        lw=2,
        label="mean Ψ",
    )

    plt.fill_between(
        centers,
        mean - std,
        mean + std,
        alpha=0.3,
        label="±1σ",
    )

    plt.axhline(0, ls="--")

    plt.xlabel("Tidal phase [rad]")
    plt.ylabel("⟨Ψ⟩")
    plt.title("Mean Ψ vs tidal phase")

    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_psi_vs_dheqdt(
    dheqdt,
    psi,
    outpath,
    title="Ψ vs dh_eq/dt",
):
    """
    Scatter plot of Ψ against the time derivative of the reference response.
    """

    import matplotlib.pyplot as plt

    outpath.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 5))
    plt.scatter(dheqdt, psi, s=10, alpha=0.6)

    plt.xlabel("dh_eq/dt [mm/hour]")
    plt.ylabel("Ψ(t)")
    plt.title(title)

    plt.axhline(0, ls="--", alpha=0.6)
    plt.axvline(0, ls="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_psi_vs_dheqdt_binned(
    dheqdt,
    psi,
    outpath,
    nbins=24,
):
    """
    Mean Ψ as a function of dh_eq/dt.
    """

    import numpy as np
    import matplotlib.pyplot as plt

    outpath.parent.mkdir(parents=True, exist_ok=True)

    bins = np.linspace(np.min(dheqdt), np.max(dheqdt), nbins + 1)
    centers = 0.5 * (bins[:-1] + bins[1:])

    mean = []
    std = []

    for i in range(nbins):
        m = (dheqdt >= bins[i]) & (dheqdt < bins[i + 1])
        if np.sum(m) > 2:
            mean.append(np.mean(psi[m]))
            std.append(np.std(psi[m]))
        else:
            mean.append(np.nan)
            std.append(np.nan)

    mean = np.array(mean)
    std = np.array(std)

    plt.figure(figsize=(7, 5))

    plt.plot(
        centers,
        mean,
        marker="o",
        lw=2,
        label="mean Ψ",
    )

    plt.fill_between(
        centers,
        mean - std,
        mean + std,
        alpha=0.3,
        label="±1σ",
    )

    plt.axhline(0, ls="--", alpha=0.6)
    plt.axvline(0, ls="--", alpha=0.6)

    plt.xlabel("dh_eq/dt [mm/hour]")
    plt.ylabel("⟨Ψ⟩")
    plt.title("Mean Ψ vs dh_eq/dt")

    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
