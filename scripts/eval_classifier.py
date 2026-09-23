from __future__ import annotations

import argparse
import json
from pathlib import Path

from percentile.evaluation import evaluate
from percentile.models import Classification, LabelProbability


def load_gold(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        result[row["id"]] = row["true_label"]
    return result


def load_predictions(path: Path) -> dict[str, Classification]:
    result: dict[str, Classification] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        probabilities = tuple(
            LabelProbability(label=k, probability=float(v))
            for k, v in row.get("probabilities", {}).items()
        )
        result[row["id"]] = Classification(
            task=row["task"],
            predicted_label=row["predicted_label"],
            probabilities=probabilities,
            classifier=row["classifier"],
            classifier_version=row["classifier_version"],
            review_required=bool(row.get("review_required", False)),
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gold", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--confidence-threshold", type=float, default=0.0)
    args = parser.parse_args()

    result = evaluate(
        load_gold(args.gold),
        load_predictions(args.predictions),
        confidence_threshold=args.confidence_threshold,
    )
    print(json.dumps(result.__dict__, indent=2))


if __name__ == "__main__":
    main()
