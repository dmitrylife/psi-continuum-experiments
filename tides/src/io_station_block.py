from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd


@dataclass
class TideSeries:
    df: pd.DataFrame          # columns: time, sea_level_mm
    cadence: str              # "1hour"
    source_file: str


DATESEG_RE = re.compile(r"^(\d{8})(\d)$")  # YYYYMMDD + segment (1/2)


def load_station_block_file(path: str | Path) -> TideSeries:
    """
    Parse format like:

    293LERWICK 1959  LAT=... LONG=... TIMEZONE=GMT
    293LERWICK 195901011 v1 v2 ... v12
    293LERWICK 195901012 v1 v2 ... v12
    ...

    Interpretation:
    - token[0] = station name/code (ignored for parsing)
    - token[1] = YYYYMMDD + segment (1 or 2)
        segment 1 -> hours 00..11
        segment 2 -> hours 12..23
    - next 12 tokens = sea level in mm (integers); missing may appear as 9999
    """

    path = Path(path)
    lines = path.read_text(errors="ignore").splitlines()

    records: List[Tuple[pd.Timestamp, float]] = []

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue

        # Skip header/meta line
        if "LAT=" in ln or "LONG=" in ln or "TIMEZONE" in ln:
            continue

        parts = ln.split()
        if len(parts) < 2 + 6:  # need at least station + dateseg + some data
            continue

        dateseg = parts[1]
        m = DATESEG_RE.match(dateseg)
        if not m:
            continue

        yyyymmdd = m.group(1)
        segment = int(m.group(2))

        year = int(yyyymmdd[0:4])
        month = int(yyyymmdd[4:6])
        day = int(yyyymmdd[6:8])

        start_hour = 0 if segment == 1 else 12

        # parse the remaining tokens as mm values
        vals: List[Optional[float]] = []
        for v in parts[2:]:
            try:
                iv = int(v)
            except ValueError:
                continue
            if iv == 9999:
                vals.append(None)
            else:
                vals.append(float(iv))

        # Typically exactly 12 values per segment
        for i, v in enumerate(vals):
            if v is None:
                continue
            hour = start_hour + i  # 1-hour cadence
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour)
            records.append((ts, v))

    df = pd.DataFrame(records, columns=["time", "sea_level_mm"]).dropna().sort_values("time")
    return TideSeries(df=df, cadence="1hour", source_file=path.name)
