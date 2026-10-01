import pandas as pd

from src.features import extract_title


def test_extracts_common_titles():
    names = pd.Series(
        [
            "Braund, Mr. Owen Harris",
            "Cumings, Mrs. John Bradley (Florence Briggs Thayer)",
            "Heikkinen, Miss. Laina",
            "Palsson, Master. Gosta Leonard",
        ]
    )

    assert list(extract_title(names)) == ["Mr", "Mrs", "Miss", "Master"]


def test_merges_french_and_short_forms():
    names = pd.Series(["Doe, Mlle. Jane", "Doe, Ms. Jane", "Doe, Mme. Jeanne"])

    assert list(extract_title(names)) == ["Miss", "Miss", "Mrs"]


def test_groups_other_titles_as_rare():
    names = pd.Series(["Smith, Dr. John", "Jones, Rev. Tom", "Lee, Countess. Ann"])

    assert list(extract_title(names)) == ["Rare", "Rare", "Rare"]


def test_name_without_title_is_unknown():
    names = pd.Series(["No title here", None])

    assert list(extract_title(names)) == ["Unknown", "Unknown"]


def test_keeps_index_and_length():
    names = pd.Series(["A, Mr. B", "C, Mrs. D"], index=[10, 20])

    result = extract_title(names)

    assert list(result.index) == [10, 20]
