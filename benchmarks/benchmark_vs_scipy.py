from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from iaa_kit import ac1, cohen_kappa, fleiss_kappa, weighted_kappa


def assert_close(name: str, actual: float, expected: float, tolerance: float = 1e-6) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{name}: expected {expected}, got {actual}")
    print(f"{name}: {actual:.6f}")


def main() -> int:
    # Reference values are calculated from the closed-form Cohen/Fleiss/Gwet
    # equations used by scipy/sklearn/nltk-style agreement examples.
    assert_close("cohen_kappa", cohen_kappa([1, 1, 0, 0], [1, 0, 0, 0]), 0.5)
    assert_close("weighted_kappa_linear", weighted_kappa([1, 2, 3], [1, 2, 2], "linear"), 0.5714285714)
    assert_close("weighted_kappa_quadratic", weighted_kappa([1, 2, 3], [1, 2, 2], "quadratic"), 0.6666666667)
    assert_close("fleiss_kappa", fleiss_kappa([[1, 1, 0], [1, 1, 1], [0, 0, 0]]), 0.55)
    assert_close("gwet_ac1", ac1(["a", "a", "b"], ["a", "b", "b"]), 0.3333333333)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
