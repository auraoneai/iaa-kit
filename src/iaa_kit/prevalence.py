def prevalence_index(a, b):
    pairs = [(x,y) for x,y in zip(a,b) if x is not None and y is not None]
    positive = sum(1 for x,y in pairs if x == y)
    negative = len(pairs) - positive
    return abs(positive - negative) / len(pairs)

def bias_index(a, b):
    pairs = [(x,y) for x,y in zip(a,b) if x is not None and y is not None]
    if not pairs:
        return 0.0
    labels = {x for pair in pairs for x in pair}
    first = {label: sum(x == label for x, _ in pairs) / len(pairs) for label in labels}
    second = {label: sum(y == label for _, y in pairs) / len(pairs) for label in labels}
    return sum(abs(first[label] - second[label]) for label in labels) / 2

def paradox_corrected(kappa_value: float, prevalence: float) -> float:
    return max(-1.0, min(1.0, kappa_value + (prevalence * (1 - abs(kappa_value)))))
