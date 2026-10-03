"""Data validation checks for the raw Titanic dataset.

Run as part of CI and locally before training: catches schema drift,
duplicate IDs, and invalid categorical values before they reach the
pipeline silently.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = next(
    p for p in [Path.cwd(), *Path.cwd().parents] if (p / "requirements.txt").exists()
)

EXPECTED_COLUMNS = {
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
}

VALID_EMBARKED = {"S", "C", "Q"}


def check_schema(df: pd.DataFrame) -> list[str]:
    errors = []
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        errors.append(f"Missing expected columns: {missing}")
    return errors


def check_passenger_id_unique(df: pd.DataFrame) -> list[str]:
    errors = []
    if df["PassengerId"].duplicated().any():
        dupes = df.loc[df["PassengerId"].duplicated(), "PassengerId"].tolist()
        errors.append(f"Duplicate PassengerId values found: {dupes}")
    return errors


def check_embarked_values(df: pd.DataFrame) -> list[str]:
    errors = []
    actual = set(df["Embarked"].dropna().unique())
    invalid = actual - VALID_EMBARKED
    if invalid:
        errors.append(f"Invalid Embarked values found: {invalid}")
    return errors


def check_null_rate(df: pd.DataFrame, column: str, max_fraction: float) -> list[str]:
    errors = []
    null_fraction = df[column].isna().mean()
    if null_fraction > max_fraction:
        errors.append(
            f"{column} is {null_fraction:.1%} null, exceeds allowed {max_fraction:.0%}"
        )
    return errors


ALLOWED_VALUES = {
    "Survived": {0, 1},
    "Pclass": {1, 2, 3},
    "Sex": {"male", "female"},
}

NUMERIC_RANGES = {
    "Age": (0, 120),
    "Fare": (0, 600),
    "SibSp": (0, 10),
    "Parch": (0, 10),
}

MAX_NULL_FRACTION = {
    "Survived": 0.0,
    "Pclass": 0.0,
    "Sex": 0.0,
    "Fare": 0.0,
    "Age": 0.30,
    "Embarked": 0.01,
}


def check_allowed_values(df: pd.DataFrame, column: str, allowed: set) -> list[str]:
    invalid = set(df[column].dropna().unique()) - allowed
    if invalid:
        return [f"Invalid {column} values found: {sorted(map(str, invalid))}"]
    return []


def check_numeric_range(
    df: pd.DataFrame, column: str, low: float, high: float
) -> list[str]:
    values = df[column].dropna()
    out_of_range = values[(values < low) | (values > high)]
    if len(out_of_range):
        message = (
            f"{column} has {len(out_of_range)} value(s) outside [{low}, {high}], "
            f"for example {out_of_range.iloc[0]}"
        )
        return [message]
    return []


def validate(df: pd.DataFrame) -> list[str]:
    errors = check_schema(df)
    if errors:
        return errors
    errors += check_passenger_id_unique(df)
    errors += check_embarked_values(df)
    for column, allowed in ALLOWED_VALUES.items():
        errors += check_allowed_values(df, column, allowed)
    for column, (low, high) in NUMERIC_RANGES.items():
        errors += check_numeric_range(df, column, low, high)
    for column, max_fraction in MAX_NULL_FRACTION.items():
        errors += check_null_rate(df, column, max_fraction)
    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/raw/titanic.csv"
    df = pd.read_csv(path)

    all_errors = validate(df)

    if all_errors:
        print("Data validation FAILED:")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Data validation passed. {len(df)} rows checked.")


if __name__ == "__main__":
    main()
