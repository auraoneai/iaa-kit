# iaa-kit

Compute inter-annotator agreement for labeling, review, and rubric-calibration workflows.

`iaa-kit` is for annotation leads, evaluation engineers, and data scientists who need inspectable agreement metrics without a statistics service. It combines a pure-NumPy implementation of Krippendorff alpha, Cohen and weighted kappa, Fleiss kappa, Gwet AC1/AC2, prevalence and bias diagnostics, partial credit, missing-data handling, and deterministic bootstrap confidence intervals.

## Inspectable Output

The Python API returns the Krippendorff alpha estimate and seeded bootstrap interval as a tuple. The installed `iaa-kit analyze` CLI writes JSON with item and rater counts, scale type, Krippendorff alpha with a seeded 95% interval, Fleiss kappa, and two-rater Cohen/weighted kappa values when applicable. The Python API also exposes the Gwet, prevalence, bias, and partial-credit functions.

## Runtime Boundary

Metrics run entirely in the local Python process over caller-provided arrays or a local JSON rating matrix. NumPy is the only runtime dependency. There are no network requests, model calls, telemetry hooks, or uploaded annotations.

## Install

Python library and CLI:

```bash
python -m pip install iaa-kit==0.1.2
```

## Python API Quickstart

```bash
python - <<'PY'
from iaa_kit import krippendorff_alpha

alpha, low, high = krippendorff_alpha(
    [[1, 1, 2], [2, 2, 2]],
    scale="ordinal",
    n_boot=200,
    seed=7,
)
print({"alpha": alpha, "ci95": [low, high]})
PY
```

## CLI Quickstart

```bash
iaa-kit analyze \
  --input examples/ratings_matrix.json \
  --scale nominal \
  --bootstrap-samples 200 \
  --seed 7 \
  --out agreement.json
```

## Documentation

- Metric selection: [`docs/when-to-use-which-metric.md`](docs/when-to-use-which-metric.md)
- Ordinal versus nominal labels: [`docs/ordinal-vs-nominal.md`](docs/ordinal-vs-nominal.md)
- Bootstrap CI tutorial: [`docs/bootstrap-ci-tutorial.md`](docs/bootstrap-ci-tutorial.md)

## Release Status

Registry and artifact status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The wheel includes the Python API and the `iaa-kit analyze` entry point. The project is alpha software. No annotation-volume, adoption, or benchmark claim is made.

## Limits

Agreement statistics do not establish label validity or reviewer correctness. The package does not recruit reviewers, host annotation data, or include real annotation datasets; bundled inputs are synthetic.

## Next Action

Run the Python API or JSON CLI on a representative rating matrix with the correct scale, then document the metric and threshold rationale before using the result as a gate.
