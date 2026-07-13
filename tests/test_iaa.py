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
from iaa_kit.cli import analyze, load_ratings, main as cli_main
from iaa_kit.krippendorff import alpha_value

ROOT = Path(__file__).resolve().parents[1]

def test_krippendorff_tuple():
    value, low, high = krippendorff_alpha([[1,1,2],[2,2,2],[1,None,1]], scale="ordinal", n_boot=50)
    assert -1 <= value <= 1 and low <= high

def test_krippendorff_scales_and_invalid_inputs():
    data = [[1, 1, 2], [2, 2, 2]]
    assert alpha_value(data, scale="interval") == pytest.approx(0.375)
    assert alpha_value(data, scale="ratio") == pytest.approx(0.375)
    assert krippendorff_alpha([[1, 1], [2]], n_boot=50, seed=0) == (1.0, 1.0, 1.0)
    with pytest.raises(ValueError, match="scale must be"):
        alpha_value(data, scale="unsupported")

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
    assert bias_index([], []) == 0.0
    assert paradox_corrected(0.5, 0.2) == pytest.approx(0.6)

def test_notebook_tutorials_execute():
    env = {"krippendorff_alpha": krippendorff_alpha, "cohen_kappa": cohen_kappa, "weighted_kappa": weighted_kappa}
    for notebook_path in sorted((ROOT / "examples").glob("*.ipynb")):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
        assert code_cells, f"{notebook_path.name} should include executable tutorial code"
        for cell in code_cells:
            exec("".join(cell["source"]), env)

def test_cli_json_contract(tmp_path):
    output = tmp_path / "agreement.json"
    assert cli_main([
        "analyze",
        "--input",
        str(ROOT / "examples" / "ratings_matrix.json"),
        "--bootstrap-samples",
        "10",
        "--out",
        str(output),
    ]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["ok"] is True
    assert payload["item_count"] == 4
    assert "krippendorff_alpha" in payload["metrics"]

def test_cli_stdout_and_input_shapes(tmp_path, capsys):
    ratings = [[1, 1], [2, 2], [1, 2]]
    list_input = tmp_path / "ratings-list.json"
    list_input.write_text(json.dumps(ratings), encoding="utf-8")
    assert load_ratings(list_input) == ratings

    matrix_input = tmp_path / "ratings-matrix.json"
    matrix_input.write_text(json.dumps({"matrix": ratings}), encoding="utf-8")
    assert load_ratings(matrix_input) == ratings

    assert cli_main([
        "analyze",
        "--input",
        str(matrix_input),
        "--bootstrap-samples",
        "10",
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["rater_count"] == 2
    assert "cohen_kappa" in payload["metrics"]
    assert "weighted_kappa_linear" in payload["metrics"]
    assert "fleiss_kappa" in payload["metrics"]

def test_cli_validation_errors(tmp_path, capsys):
    invalid_input = tmp_path / "invalid.json"
    invalid_input.write_text(json.dumps({"ratings": "not-a-matrix"}), encoding="utf-8")
    assert cli_main(["analyze", "--input", str(invalid_input)]) == 1
    assert json.loads(capsys.readouterr().out)["ok"] is False

    uneven_input = tmp_path / "uneven.json"
    uneven_input.write_text(json.dumps([[1, 2], [1]]), encoding="utf-8")
    error_output = tmp_path / "errors" / "result.json"
    assert cli_main([
        "analyze",
        "--input",
        str(uneven_input),
        "--out",
        str(error_output),
    ]) == 1
    assert "same number of raters" in json.loads(error_output.read_text(encoding="utf-8"))["error"]

    with pytest.raises(ValueError, match="at least one rating row"):
        analyze([])
