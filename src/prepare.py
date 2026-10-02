"""Stage 1: split the raw data, then clean it.

Imputation values are learned from the training split only and applied to
both splits, so no test information leaks into training.

Run from the repository root: python -m src.prepare
"""

from pathlib import Path

from sklearn.model_selection import train_test_split

from src.data import clean, fit_imputers, load_raw
from src.utils import load_params, set_seeds

RAW_PATH = "data/raw/titanic.csv"
OUT_DIR = Path("data/processed")


def main() -> None:
    params = load_params()
    set_seeds(params["seed"])

    raw = load_raw(RAW_PATH)
    train_raw, test_raw = train_test_split(
        raw,
        test_size=params["split"]["test_size"],
        random_state=params["seed"],
        shuffle=True,
    )

    imputers = fit_imputers(train_raw)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean(train_raw, imputers).to_csv(
        OUT_DIR / "train.csv", index=False, lineterminator="\n"
    )
    clean(test_raw, imputers).to_csv(
        OUT_DIR / "test.csv", index=False, lineterminator="\n"
    )


if __name__ == "__main__":
    main()
