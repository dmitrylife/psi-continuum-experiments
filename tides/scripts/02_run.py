import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from tides.src.io_station_block import load_station_block_file

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
FIG = BASE / "figures"
FIG.mkdir(exist_ok=True)

path = RAW / "h293.dat.txt"
series = load_station_block_file(path)
df = series.df

if df.empty:
    raise ValueError("Parsed dataframe is empty. Check parser assumptions.")

t = df["time"]
h_obs_mm = df["sea_level_mm"].to_numpy()

# ---- Reference response h_eq(t): mean diurnal cycle (by hour-of-day)
hours = df["time"].dt.hour.to_numpy()
h_eq_hour = np.full(24, np.nan)
for h in range(24):
    mask = hours == h
    if np.any(mask):
        h_eq_hour[h] = np.nanmean(h_obs_mm[mask])

# fill any missing hours (unlikely) by interpolation
if np.any(np.isnan(h_eq_hour)):
    idx = np.arange(24)
    good = ~np.isnan(h_eq_hour)
    h_eq_hour = np.interp(idx, idx[good], h_eq_hour[good])

h_eq_mm = h_eq_hour[hours]

# normalize amplitude
amp = 0.5 * (np.nanmax(h_eq_hour) - np.nanmin(h_eq_hour))
A = amp if amp != 0 else 1.0

psi = (h_obs_mm - h_eq_mm) / A

# ---- Plot Ψ(t) (first 14 days to keep it readable)
N = min(len(df), 24 * 14)
plt.figure(figsize=(10, 4))
plt.plot(t.iloc[:N], psi[:N], lw=1)
plt.axhline(0, color="k", ls="--", alpha=0.5)
plt.xlabel("Time")
plt.ylabel("Ψ(t)")
plt.title(f"Ψ(t) — {series.source_file} ({series.cadence}), first 14 days")
plt.tight_layout()
out1 = FIG / "psi_tides.png"
plt.savefig(out1, dpi=150)
plt.close()

# ---- Plot mean diurnal cycle vs obs (sanity check)
plt.figure(figsize=(8, 4))
plt.plot(range(24), h_eq_hour, lw=2)
plt.xlabel("Hour of day")
plt.ylabel("Sea level (mm)")
plt.title("Reference response h_eq: mean diurnal cycle")
plt.tight_layout()
out2 = FIG / "heq_diurnal_cycle.png"
plt.savefig(out2, dpi=150)
plt.close()

print(f"Saved: {out1}")
print(f"Saved: {out2}")
