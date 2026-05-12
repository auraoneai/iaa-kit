from __future__ import annotations
from collections import Counter
from typing import Any, Sequence

Label = Any

def fleiss_kappa(matrix: Sequence[Sequence[Label]]) -> float:
    rows = [list(row) for row in matrix if len(row) >= 2]
    if not rows: raise ValueError("at least one row with two raters required")
    n = len(rows[0])
    if any(len(row) != n for row in rows): raise ValueError("all rows must have same number of ratings")
    labels = sorted({x for row in rows for x in row}, key=repr); totals: Counter[Label] = Counter()
    p_i = []
    for row in rows:
        c = Counter(row); totals.update(c); p_i.append((sum(v*v for v in c.values()) - n) / (n * (n - 1)))
    pbar = sum(p_i) / len(p_i); total = len(rows) * n
    pe = sum((totals[l] / total) ** 2 for l in labels)
    return 1.0 if pe == 1 else (pbar - pe) / (1 - pe)
