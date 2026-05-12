def partial_credit(labels, truth, max_distance: float | None = None):
    pairs = [(float(x), float(y)) for x, y in zip(labels, truth) if x is not None and y is not None]
    if not pairs: raise ValueError("no labels")
    maxd = max_distance if max_distance is not None else max(abs(x-y) for x,y in pairs) or 1.0
    return sum(max(0.0, 1.0 - abs(x-y)/maxd) for x,y in pairs) / len(pairs)
