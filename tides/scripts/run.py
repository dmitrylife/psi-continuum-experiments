from __future__ import annotations

import argparse
from pathlib import Path

from tides.src.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a single tidal response experiment window."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to raw tide-gauge input file, e.g. tides/data/raw/h293.dat.txt",
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Start date (inclusive), format YYYY-MM-DD",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="End date (inclusive), format YYYY-MM-DD",
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

    metrics = run_pipeline(
        input_path=args.input,
        start=args.start,
        end=args.end,
        reference_method=args.reference,
        artifacts_root=args.artifacts_root,
        aggregate_metrics_csv=args.aggregate_metrics,
    )

    print("Run completed.")
    for k, v in metrics.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
