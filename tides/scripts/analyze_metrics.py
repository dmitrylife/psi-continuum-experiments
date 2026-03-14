from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


METRICS_PATH = Path("tides/results/metrics.csv")
OUTDIR = Path("tides/results/analysis")


def load_metrics():
    df = pd.read_csv(METRICS_PATH)

    # удалить дубликаты запусков, но сохранить разные reference_method
    df = df.drop_duplicates(
        subset=["station", "start", "end", "reference_method"],
        keep="last",
    )

    df["start"] = pd.to_datetime(df["start"])
    df = df.sort_values(["reference_method", "start"])

    return df


def plot_metric(df, column, ylabel):
    plt.figure(figsize=(8, 4))

    for method, sub in df.groupby("reference_method"):
        sub = sub.sort_values("start")
        plt.plot(sub["start"], sub[column], marker="o", label=method)

    plt.xlabel("Time window")
    plt.ylabel(ylabel)
    plt.title(f"{column} evolution")
    plt.legend()
    plt.tight_layout()

    out = OUTDIR / f"{column}.png"
    plt.savefig(out, dpi=150)
    plt.close()

    print("Saved:", out)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    df = load_metrics()
    print(df)

    plot_metric(df, "psi_rms", "Ψ RMS")
    plot_metric(df, "psi_skew", "Ψ skewness")
    plot_metric(df, "A_mm", "Amplitude A (mm)")


if __name__ == "__main__":
    main()
