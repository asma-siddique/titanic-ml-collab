"""Reusable feature helpers for the Titanic data."""

import pandas as pd

TITLE_ALIASES = {"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
COMMON_TITLES = {"Mr", "Mrs", "Miss", "Master"}


def extract_title(names: pd.Series) -> pd.Series:
    """Return the honorific from names like "Braund, Mr. Owen Harris".

    Mlle/Ms become Miss and Mme becomes Mrs. Any title other than Mr, Mrs, Miss
    or Master becomes "Rare", and names without a title become "Unknown".
    """
    titles = names.str.extract(r",\s*([^.]+)\.", expand=False).str.strip()
    titles = titles.replace(TITLE_ALIASES)
    titles = titles.where(titles.isin(COMMON_TITLES) | titles.isna(), "Rare")
    return titles.fillna("Unknown")
