"""Loading and cleaning for the Titanic dataset."""

from dataclasses import dataclass

import pandas as pd

TARGET = "Survived"

FEATURE_COLUMNS = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

SEX_MAP = {"male": 0, "female": 1}
EMBARKED_MAP = {"S": 0, "C": 1, "Q": 2}


@dataclass
class Imputers:
    """Fill values learned from the training split and applied to every split."""

    age_median: float
    fare_median: float
    embarked_mode: str


def load_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def fit_imputers(train: pd.DataFrame) -> Imputers:
    return Imputers(
        age_median=train["Age"].median(),
        fare_median=train["Fare"].median(),
        embarked_mode=train["Embarked"].mode().iloc[0],
    )


def clean(df: pd.DataFrame, imputers: Imputers) -> pd.DataFrame:
    """Fill missing values with the given imputers, encode categoricals and
    keep only the model features and the target."""
    df = df.copy()
    df["Age"] = df["Age"].fillna(imputers.age_median)
    df["Fare"] = df["Fare"].fillna(imputers.fare_median)
    df["Embarked"] = df["Embarked"].fillna(imputers.embarked_mode)
    df["Sex"] = df["Sex"].map(SEX_MAP)
    df["Embarked"] = df["Embarked"].map(EMBARKED_MAP)
    return df[[*FEATURE_COLUMNS, TARGET]]


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return df[FEATURE_COLUMNS], df[TARGET]
