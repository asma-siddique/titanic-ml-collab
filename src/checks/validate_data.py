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


def main():
    df = pd.read_csv(ROOT / "data" / "raw" / "titanic.csv")

    all_errors = []
    all_errors += check_schema(df)
    all_errors += check_passenger_id_unique(df)
    all_errors += check_embarked_values(df)
    all_errors += check_null_rate(df, "Age", max_fraction=0.30)

    if all_errors:
        print("Data validation FAILED:")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Data validation passed. {len(df)} rows checked.")


if __name__ == "__main__":
    main()
