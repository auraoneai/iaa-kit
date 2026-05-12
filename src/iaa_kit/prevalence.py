def prevalence_index(a, b):
    pairs = [(x,y) for x,y in zip(a,b) if x is not None and y is not None]
    positive = sum(1 for x,y in pairs if x == y)
    negative = len(pairs) - positive
    return abs(positive - negative) / len(pairs)

def bias_index(a, b):
    pairs = [(x,y) for x,y in zip(a,b) if x is not None and y is not None]
    return abs(sum(x != y for x,y in pairs) - sum(y != x for x,y in pairs)) / len(pairs) if pairs else 0.0

def paradox_corrected(kappa_value: float, prevalence: float) -> float:
    return max(-1.0, min(1.0, kappa_value + (prevalence * (1 - abs(kappa_value)))))
