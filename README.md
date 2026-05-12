# iaa-kit

`iaa-kit` is a pure-NumPy inter-annotator agreement library with Krippendorff alpha, Cohen kappa, weighted kappa, Fleiss kappa, Gwet AC1/AC2, bootstrap confidence intervals, missing-data handling, and synthetic-report generation.

## Quickstart

```bash
python -m venv .venv
. .venv/bin/activate
pip install iaa-kit
python -c "from iaa_kit import krippendorff_alpha; print(krippendorff_alpha([[1,1,2],[2,2,2]], scale='ordinal'))"
```

## What This Is Not

This is not a human-label vendor, benchmark, or source of real annotations. Examples are synthetic.
