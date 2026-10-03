import pandas as pd

from src.checks.validate_data import (
    check_allowed_values,
    check_embarked_values,
    check_null_rate,
    check_numeric_range,
    check_passenger_id_unique,
    check_schema,
    validate,
)


def make_valid_df():
    return pd.DataFrame(
        {
            "PassengerId": [1, 2, 3],
            "Survived": [0, 1, 0],
            "Pclass": [3, 1, 2],
            "Name": ["A", "B", "C"],
            "Sex": ["male", "female", "male"],
            "Age": [22, 38, 26],
            "SibSp": [1, 1, 0],
            "Parch": [0, 0, 0],
            "Ticket": ["x", "y", "z"],
            "Fare": [7.25, 71.28, 7.92],
            "Cabin": [None, "C85", None],
            "Embarked": ["S", "C", "Q"],
        }
    )


def test_schema_passes_on_valid_df():
    assert check_schema(make_valid_df()) == []


def test_schema_flags_missing_column():
    df = make_valid_df().drop(columns=["Embarked"])
    errors = check_schema(df)
    assert len(errors) == 1
    assert "Embarked" in errors[0]


def test_passenger_id_unique_passes():
    assert check_passenger_id_unique(make_valid_df()) == []


def test_passenger_id_unique_flags_duplicates():
    df = make_valid_df()
    df.loc[2, "PassengerId"] = 1
    errors = check_passenger_id_unique(df)
    assert len(errors) == 1


def test_embarked_values_passes():
    assert check_embarked_values(make_valid_df()) == []


def test_embarked_values_flags_invalid():
    df = make_valid_df()
    df.loc[0, "Embarked"] = "X"
    errors = check_embarked_values(df)
    assert len(errors) == 1
    assert "X" in errors[0]


def test_allowed_values_flags_bad_class():
    df = make_valid_df()
    df.loc[0, "Pclass"] = 7
    errors = check_allowed_values(df, "Pclass", {1, 2, 3})
    assert len(errors) == 1
    assert "7" in errors[0]


def test_numeric_range_flags_negative_fare():
    df = make_valid_df()
    df.loc[1, "Fare"] = -5.0
    errors = check_numeric_range(df, "Fare", 0, 600)
    assert len(errors) == 1
    assert "Fare" in errors[0]


def test_numeric_range_ignores_missing_values():
    df = make_valid_df()
    df.loc[0, "Age"] = None
    assert check_numeric_range(df, "Age", 0, 120) == []


def test_null_rate_flags_too_many_missing():
    df = make_valid_df()
    df["Age"] = [None, None, 26]
    errors = check_null_rate(df, "Age", max_fraction=0.30)
    assert len(errors) == 1


def test_validate_passes_on_valid_df():
    assert validate(make_valid_df()) == []


def test_validate_reports_several_problems_at_once():
    df = make_valid_df()
    df.loc[0, "Survived"] = 5
    df.loc[1, "Fare"] = -1.0
    errors = validate(df)
    assert len(errors) == 3
