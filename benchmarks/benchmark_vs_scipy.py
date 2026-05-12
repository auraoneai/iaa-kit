from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from iaa_kit import ac1, cohen_kappa, fleiss_kappa, weighted_kappa


def nltk_kappa(a: list[object], b: list[object]) -> float | None:
    try:
        from nltk.metrics.agreement import AnnotationTask
    except Exception:
        return None
    task = AnnotationTask(data=[("a", i, x) for i, x in enumerate(a)] + [("b", i, y) for i, y in enumerate(b)])
    return float(task.kappa())


def sklearn_kappa(a: list[object], b: list[object], weights: str | None = None) -> float | None:
    try:
        from sklearn.metrics import cohen_kappa_score
    except Exception:
        return None
    return float(cohen_kappa_score(a, b, weights=weights))


def assert_close(name: str, actual: float, expected: float, tolerance: float = 1e-6) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{name}: expected {expected}, got {actual}")
    print(f"{name}: {actual:.6f}")


def main() -> int:
    # Optional external-library checks run when the comparison libraries are
    # installed; otherwise the same closed-form reference values are used.
    pair_a, pair_b = [1, 1, 0, 0], [1, 0, 0, 0]
    ordinal_a, ordinal_b = [1, 2, 3], [1, 2, 2]
    assert_close("cohen_kappa_vs_nltk", cohen_kappa(pair_a, pair_b), nltk_kappa(pair_a, pair_b) or 0.5)
    assert_close(
        "weighted_kappa_linear_vs_sklearn",
        weighted_kappa(ordinal_a, ordinal_b, "linear"),
        sklearn_kappa(ordinal_a, ordinal_b, "linear") or 0.5714285714,
    )
    assert_close(
        "weighted_kappa_quadratic_vs_sklearn",
        weighted_kappa(ordinal_a, ordinal_b, "quadratic"),
        sklearn_kappa(ordinal_a, ordinal_b, "quadratic") or 0.6666666667,
    )
    assert_close("fleiss_kappa", fleiss_kappa([[1, 1, 0], [1, 1, 1], [0, 0, 0]]), 0.55)
    assert_close("gwet_ac1", ac1(["a", "a", "b"], ["a", "b", "b"]), 0.3333333333)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
