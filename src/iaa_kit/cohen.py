from __future__ import annotations
from collections import Counter
from typing import Any, Sequence

Label = Any

def kappa(a: Sequence[Label], b: Sequence[Label], weights: str | None = None) -> float:
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pairs: raise ValueError("no overlapping labels")
    labels = sorted({x for p in pairs for x in p}, key=repr)
    index = {label: i for i, label in enumerate(labels)}; n = len(labels)
    def w(x: Label, y: Label) -> float:
        if x == y: return 0.0
        if weights is None: return 1.0
        d = abs(index[x]-index[y]) / max(n-1,1)
        return d if weights == "linear" else d*d if weights == "quadratic" else 1.0
    observed = sum(w(x,y) for x,y in pairs) / len(pairs)
    ca, cb = Counter(x for x,_ in pairs), Counter(y for _,y in pairs)
    expected = sum(w(x,y) * ca[x]/len(pairs) * cb[y]/len(pairs) for x in labels for y in labels)
    return 1.0 if expected == 0 else 1.0 - observed / expected

def cohen_kappa(a: Sequence[Label], b: Sequence[Label]) -> float: return kappa(a, b)
def weighted_kappa(a: Sequence[Label], b: Sequence[Label], weight: str = "linear") -> float: return kappa(a, b, weight)
