"""Stage 2: train the model on the prepared training split.

Run from the repository root: python -m src.train
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.data import split_features_target
from src.utils import load_params, set_seeds

TRAIN_PATH = "data/processed/train.csv"
MODEL_PATH = Path("models/model.joblib")


def build_model(train_params: dict, seed: int) -> RandomForestClassifier:
    if train_params["model"] != "random_forest":
        raise ValueError(f"Unknown model: {train_params['model']!r}")
    return RandomForestClassifier(
        n_estimators=train_params["n_estimators"],
        max_depth=train_params["max_depth"],
        random_state=seed,
    )


def main() -> None:
    params = load_params()
    set_seeds(params["seed"])

    X_train, y_train = split_features_target(pd.read_csv(TRAIN_PATH))
    model = build_model(params["train"], params["seed"])
    model.fit(X_train, y_train)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    main()
