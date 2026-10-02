import pandas as pd

from src.data import (
    FEATURE_COLUMNS,
    TARGET,
    clean,
    fit_imputers,
    split_features_target,
)


def make_frame(ages, fares, embarked):
    n = len(ages)
    return pd.DataFrame(
        {
            "Survived": [0, 1] * (n // 2) + [0] * (n % 2),
            "Pclass": [3] * n,
            "Sex": ["male", "female"] * (n // 2) + ["male"] * (n % 2),
            "Age": ages,
            "SibSp": [0] * n,
            "Parch": [0] * n,
            "Fare": fares,
            "Embarked": embarked,
            "Name": ["x"] * n,
        }
    )


def test_imputers_come_from_the_training_frame_only():
    train = make_frame([20.0, 30.0, 40.0], [10.0, 20.0, 30.0], ["S", "S", "C"])
    test = make_frame([None, 90.0], [None, 500.0], [None, "Q"])

    imputers = fit_imputers(train)
    cleaned = clean(test, imputers)

    assert imputers.age_median == 30.0
    assert cleaned.loc[0, "Age"] == 30.0
    assert cleaned.loc[0, "Fare"] == 20.0
    assert cleaned.loc[0, "Embarked"] == 0


def test_clean_encodes_categoricals_and_keeps_only_model_columns():
    df = make_frame([22.0, 38.0], [7.25, 71.28], ["S", "C"])
    cleaned = clean(df, fit_imputers(df))

    assert list(cleaned.columns) == [*FEATURE_COLUMNS, TARGET]
    assert list(cleaned["Sex"]) == [0, 1]
    assert list(cleaned["Embarked"]) == [0, 1]
    assert cleaned.isna().sum().sum() == 0


def test_split_features_target():
    df = make_frame([22.0, 38.0], [7.25, 71.28], ["S", "C"])
    X, y = split_features_target(clean(df, fit_imputers(df)))

    assert TARGET not in X.columns
    assert list(y) == [0, 1]
