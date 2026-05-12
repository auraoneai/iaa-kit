from iaa_kit import krippendorff_alpha, cohen_kappa, weighted_kappa, fleiss_kappa, ac1, ac2, partial_credit, report

def test_krippendorff_tuple():
    value, low, high = krippendorff_alpha([[1,1,2],[2,2,2],[1,None,1]], scale="ordinal", n_boot=50)
    assert -1 <= value <= 1 and low <= high

def test_pairwise_metrics():
    assert cohen_kappa([1,1,0,0], [1,0,0,0]) <= 1
    assert weighted_kappa([1,2,3], [1,2,2], "quadratic") <= 1
    assert ac1(["a","a","b"], ["a","b","b"]) <= 1
    assert ac2([1,2,3], [1,2,2]) <= 1

def test_fleiss_partial_report():
    assert fleiss_kappa([[1,1,0],[1,1,1],[0,0,0]]) <= 1
    assert partial_credit([1,2,3], [1,3,3]) > 0
    assert "Agreement" in report({"kappa": 0.5})
