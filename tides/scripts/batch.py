from __future__ import annotations

import argparse
import csv
from pathlib import Path

from tides.src.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a batch of tidal experiments from a CSV target list."
    )
    parser.add_argument(
        "targets_csv",
        help="CSV with columns: station,input,start,end",
    )
    parser.add_argument(
        "--reference",
        default="diurnal_mean",
        choices=["diurnal_mean", "harmonic_4mode"],
        help="Reference response method",
    )
    parser.add_argument(
        "--artifacts-root",
        default="tides/artifacts",
        help="Directory where run artifacts will be saved",
    )
    parser.add_argument(
        "--aggregate-metrics",
        default="tides/results/metrics.csv",
        help="Path to aggregate metrics CSV",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    with open(args.targets_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"No targets found in {args.targets_csv}")

    for row in rows:
        input_path = row["input"]
        start = row.get("start") or None
        end = row.get("end") or None

        print(f"Running: input={input_path}, start={start}, end={end}")

        metrics = run_pipeline(
            input_path=input_path,
            start=start,
            end=end,
            reference_method=args.reference,
            artifacts_root=args.artifacts_root,
            aggregate_metrics_csv=args.aggregate_metrics,
        )

        print(f"Done: station={metrics['station']} psi_rms={metrics['psi_rms']:.4f}")


if __name__ == "__main__":
    main()

