from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd
import numpy as np

from tides.src.diagnostics import compute_psi, robust_amplitude, summarize_metrics
from tides.src.io_station_block import load_station_block_file
from tides.src.plotting import (
    plot_reference_cycle,
    plot_reference_timeseries,
    plot_psi_timeseries,
    plot_state_space,
    plot_state_space_density,
    plot_psi_vs_phase,
    plot_psi_vs_phase_binned,
    plot_psi_vs_dheqdt,
    plot_psi_vs_dheqdt_binned,
)

from tides.src.reference import build_reference, harmonic_phase_4mode


def infer_station_id(input_path: Path) -> str:
    """
    Infer station id from file name.
    Example:
        h293.dat.txt -> h293
    """
    name = input_path.name
    return name.split(".")[0]


def load_and_filter(input_path: Path, start: str | None, end: str | None) -> tuple[pd.DataFrame, str]:
    series = load_station_block_file(input_path)
    df = series.df.rename(columns={"time": "t", "sea_level_mm": "h_mm"}).copy()

    if df.empty:
        raise ValueError(f"No data parsed from {input_path}")

    if start is not None:
        df = df[df["t"] >= pd.Timestamp(start)]
    if end is not None:
        df = df[df["t"] <= pd.Timestamp(end)]

    df = df.sort_values("t").reset_index(drop=True)

    if df.empty:
        raise ValueError(f"No data left after filtering {input_path} to [{start}, {end}]")

    return df, series.source_file


def window_id(start: str | None, end: str | None) -> str:
    s = start if start is not None else "full"
    e = end if end is not None else "full"
    return f"{s}_{e}"


def run_pipeline(
    input_path: str | Path,
    start: str | None = None,
    end: str | None = None,
    reference_method: str = "diurnal_mean",
    artifacts_root: str | Path = "tides/artifacts",
    aggregate_metrics_csv: str | Path = "tides/results/metrics.csv",
) -> dict:
    input_path = Path(input_path)
    artifacts_root = Path(artifacts_root)
    aggregate_metrics_csv = Path(aggregate_metrics_csv)

    station = infer_station_id(input_path)
    wid = window_id(start, end)

    df, source_file = load_and_filter(input_path, start, end)

    h_eq_mm, ref_info = build_reference(df, method=reference_method)
    A_mm = robust_amplitude(df["h_mm"].to_numpy())
    psi = compute_psi(df["h_mm"].to_numpy(), h_eq_mm, A_mm)
    # time derivative of the reference response
    t_hours = (df["t"] - df["t"].iloc[0]).dt.total_seconds().to_numpy(dtype=float) / 3600.0
    dheqdt = np.gradient(h_eq_mm, t_hours)

    phase = None
    if reference_method == "harmonic_4mode":
        phase = harmonic_phase_4mode(df)


    metrics = summarize_metrics(
        df=df,
        h_eq_mm=h_eq_mm,
        psi=psi,
        A_mm=A_mm,
        station=station,
        source_file=source_file,
        start=start or "full",
        end=end or "full",
        reference_method=reference_method,
    )

    run_dir = artifacts_root / station / wid
    fig_dir = run_dir / "figures"
    res_dir = run_dir / "results"
    fig_dir.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)

    if reference_method == "diurnal_mean":
        plot_reference_cycle(
            hourly_reference_mm=ref_info["hourly_reference_mm"],
            outpath=fig_dir / "heq_diurnal_cycle.png",
        )
    else:
        plot_reference_timeseries(
            df=df,
            h_eq_mm=h_eq_mm,
            outpath=fig_dir / "heq_timeseries.png",
            title=f"Reference fit — {station}, {start or 'full'} to {end or 'full'}",
        )

    plot_psi_timeseries(
        df=df,
        psi=psi,
        outpath=fig_dir / "psi_tides.png",
        title=f"Ψ(t) — {station}, {start or 'full'} to {end or 'full'}",
    )

    plot_state_space(
        h_eq_mm=h_eq_mm,
        psi=psi,
        outpath=fig_dir / "psi_state_space.png",
        title=f"State-space — {station}, {start or 'full'} to {end or 'full'}",
    )
    plot_state_space_density(
        h_eq_mm=h_eq_mm,
        psi=psi,
        outpath=fig_dir / "psi_state_space_density.png",
    )
    if phase is not None:
        plot_psi_vs_phase(
            phase=phase,
            psi=psi,
            outpath=fig_dir / "psi_vs_phase.png",
            title=f"Ψ vs tidal phase — {station}, {start or 'full'} to {end or 'full'}",
        )
    plot_psi_vs_phase_binned(
        phase=phase,
        psi=psi,
        outpath=fig_dir / "psi_vs_phase_binned.png",
    )
    plot_psi_vs_dheqdt(
        dheqdt=dheqdt,
        psi=psi,
        outpath=fig_dir / "psi_vs_dheqdt.png",
        title=f"Ψ vs dh_eq/dt — {station}, {start or 'full'} to {end or 'full'}",
    )

    plot_psi_vs_dheqdt_binned(
        dheqdt=dheqdt,
        psi=psi,
        outpath=fig_dir / "psi_vs_dheqdt_binned.png",
    )

    df_out = df.copy()
    df_out["h_eq_mm"] = h_eq_mm
    df_out["psi"] = psi
    df_out.to_csv(res_dir / "window.csv", index=False)

    with open(res_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    append_metrics_csv(aggregate_metrics_csv, metrics)

    return metrics


def append_metrics_csv(csv_path: Path, metrics: dict) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = csv_path.exists()
    fieldnames = list(metrics.keys())

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)

