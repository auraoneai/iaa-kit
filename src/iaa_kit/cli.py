from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .cohen import cohen_kappa, weighted_kappa
from .fleiss import fleiss_kappa
from .krippendorff import alpha_bootstrap


def load_ratings(path: str | Path) -> list[list[Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        rows = payload.get("ratings") or payload.get("matrix")
    else:
        rows = payload
    if not isinstance(rows, list) or not all(isinstance(row, list) for row in rows):
        raise ValueError("ratings input must be a JSON array of rating rows or an object with ratings/matrix")
    return rows


def analyze(
    ratings: Sequence[Sequence[Any]],
    *,
    scale: str = "nominal",
    bootstrap_samples: int = 200,
    seed: int = 0,
) -> dict[str, Any]:
    rows = [list(row) for row in ratings]
    if not rows:
        raise ValueError("at least one rating row is required")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("all rating rows must have the same number of raters")

    alpha, alpha_low, alpha_high = alpha_bootstrap(rows, scale=scale, n_boot=bootstrap_samples, seed=seed)
    result: dict[str, Any] = {
        "ok": True,
        "item_count": len(rows),
        "rater_count": width,
        "scale": scale,
        "metrics": {
            "krippendorff_alpha": {
                "value": round(alpha, 10),
                "ci95_low": round(alpha_low, 10),
                "ci95_high": round(alpha_high, 10),
                "bootstrap_samples": bootstrap_samples,
                "seed": seed,
            }
        },
    }
    if width == 2:
        first = [row[0] for row in rows]
        second = [row[1] for row in rows]
        result["metrics"]["cohen_kappa"] = {"value": round(cohen_kappa(first, second), 10)}
        result["metrics"]["weighted_kappa_linear"] = {"value": round(weighted_kappa(first, second, "linear"), 10)}
        result["metrics"]["weighted_kappa_quadratic"] = {
            "value": round(weighted_kappa(first, second, "quadratic"), 10)
        }
    if width >= 2:
        result["metrics"]["fleiss_kappa"] = {"value": round(fleiss_kappa(rows), 10)}
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iaa-kit")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze_parser = sub.add_parser("analyze", help="Compute agreement metrics from a JSON rating matrix.")
    analyze_parser.add_argument("--input", required=True, type=Path, help="JSON file with ratings or matrix rows.")
    analyze_parser.add_argument("--scale", default="nominal", choices=["nominal", "ordinal", "interval", "ratio"])
    analyze_parser.add_argument("--bootstrap-samples", type=int, default=200)
    analyze_parser.add_argument("--seed", type=int, default=0)
    analyze_parser.add_argument("--out", type=Path, help="Write JSON output to this path instead of stdout.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = analyze(
            load_ratings(args.input),
            scale=args.scale,
            bootstrap_samples=args.bootstrap_samples,
            seed=args.seed,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = {"ok": False, "error": str(exc)}
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 1
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
