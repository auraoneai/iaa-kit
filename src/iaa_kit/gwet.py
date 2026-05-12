from __future__ import annotations
from .cohen import kappa

def ac1(a, b) -> float:
    pairs = [(x,y) for x,y in zip(a,b) if x is not None and y is not None]
    po = sum(x == y for x,y in pairs) / len(pairs)
    labels = {x for p in pairs for x in p}; probs = []
    for label in labels:
        probs.append((sum(x == label for x,_ in pairs) + sum(y == label for _,y in pairs)) / (2 * len(pairs)))
    pe = sum(p * (1-p) for p in probs) / max(len(labels) - 1, 1)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)

def ac2(a, b, weight: str = "linear") -> float:
    return kappa(a, b, weights=weight)
