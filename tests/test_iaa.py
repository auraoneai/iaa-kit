import json
from pathlib import Path

import pytest

from iaa_kit import (
    ac1,
    ac2,
    bias_index,
    cohen_kappa,
    fleiss_kappa,
    krippendorff_alpha,
    paradox_corrected,
    partial_credit,
    prevalence_index,
    report,
    weighted_kappa,
)

ROOT = Path(__file__).resolve().parents[1]

def test_krippendorff_tuple():
    value, low, high = krippendorff_alpha([[1,1,2],[2,2,2],[1,None,1]], scale="ordinal", n_boot=50)
    assert -1 <= value <= 1 and low <= high

def test_pairwise_metrics():
    assert cohen_kappa([1,1,0,0], [1,0,0,0]) == pytest.approx(0.5)
    assert weighted_kappa([1,2,3], [1,2,2], "linear") == pytest.approx(0.5714285714)
    assert weighted_kappa([1,2,3], [1,2,2], "quadratic") == pytest.approx(0.6666666667)
    assert ac1(["a","a","b"], ["a","b","b"]) == pytest.approx(0.3333333333)
    assert ac2([1,2,3], [1,2,2]) == pytest.approx(0.5714285714)

def test_fleiss_partial_report():
    assert fleiss_kappa([[1,1,0],[1,1,1],[0,0,0]]) == pytest.approx(0.55)
    assert partial_credit([1,2,3], [1,3,3]) == pytest.approx(0.6666666667)
    assert "Agreement" in report({"kappa": 0.5})

def test_prevalence_bias_and_correction():
    a = ["yes", "yes", "yes", "no"]
    b = ["yes", "no", "yes", "no"]
    assert prevalence_index(a, b) == pytest.approx(0.5)
    assert bias_index(a, b) == pytest.approx(0.25)
    assert paradox_corrected(0.5, 0.2) == pytest.approx(0.6)

def test_notebook_tutorials_execute():
    env = {"krippendorff_alpha": krippendorff_alpha, "cohen_kappa": cohen_kappa, "weighted_kappa": weighted_kappa}
    for notebook_path in sorted((ROOT / "examples").glob("*.ipynb")):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
        assert code_cells, f"{notebook_path.name} should include executable tutorial code"
        for cell in code_cells:
            exec("".join(cell["source"]), env)
