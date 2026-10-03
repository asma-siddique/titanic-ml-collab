"""Stage 3: score the model on the test split and write metrics.json.

metrics.json also records the commit SHA the run was made from, and whether
src/ or dvc.yaml had uncommitted changes, so a result can be traced to code.

Run from the repository root: python -m src.evaluate
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from src.data import split_features_target
from src.utils import git_info

TEST_PATH = "data/processed/test.csv"
MODEL_PATH = "models/model.joblib"
METRICS_PATH = Path("metrics.json")


def write_metrics(metrics: dict, path: Path = METRICS_PATH) -> None:
    # newline="\n" keeps the bytes the same on Windows, where write_text would
    # use \r\n and DVC would record a hash that Git's checkout never reproduces.
    path.write_text(json.dumps(metrics, indent=2) + "\n", newline="\n")


def main() -> None:
    model = joblib.load(MODEL_PATH)
    X_test, y_test = split_features_target(pd.read_csv(TEST_PATH))
    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        **git_info(),
    }
    write_metrics(metrics)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
