from __future__ import annotations
import numpy as np
from typing import Iterable, Sequence

def _clean(data):
    return [[x for x in row if x is not None and not (isinstance(x, float) and np.isnan(x))] for row in data]

def _distance(a, b, scale: str) -> float:
    if scale == "nominal": return 0.0 if a == b else 1.0
    if scale == "ordinal": return float((float(a) - float(b)) ** 2)
    if scale == "interval": return float((float(a) - float(b)) ** 2)
    if scale == "ratio": return float(((float(a) - float(b)) / (float(a) + float(b))) ** 2) if float(a) + float(b) else 0.0
    raise ValueError("scale must be nominal, ordinal, interval, or ratio")

def alpha_value(data: Sequence[Sequence[object]], scale: str = "nominal") -> float:
    rows = _clean(data); observed = []
    for row in rows:
        for i, a in enumerate(row):
            for b in row[i+1:]: observed.append(_distance(a, b, scale))
    if not observed: raise ValueError("at least one overlapping item is required")
    values = [v for row in rows for v in row]
    expected = [_distance(a, b, scale) for i, a in enumerate(values) for b in values[i+1:]]
    de = float(np.mean(expected)) if expected else 0.0
    return 1.0 if de == 0 else 1.0 - float(np.mean(observed)) / de

def alpha_bootstrap(data: Sequence[Sequence[object]], scale: str = "nominal", n_boot: int = 1000, seed: int | None = 0) -> tuple[float, float, float]:
    value = alpha_value(data, scale)
    rng = np.random.default_rng(seed); rows = list(data); stats = []
    for _ in range(n_boot):
        sample = [rows[int(i)] for i in rng.integers(0, len(rows), len(rows))]
        try: stats.append(alpha_value(sample, scale))
        except ValueError: pass
    if not stats: return (value, value, value)
    return (value, float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5)))
