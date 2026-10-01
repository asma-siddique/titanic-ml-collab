# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 - Titanic exploratory data analysis
#
# Goal: understand the raw passenger data before changing the training pipeline.
# We check the shape and types, missing values, the target balance, and how
# survival relates to the main passenger attributes.
#
# This notebook is paired with `01-eda.py` (jupytext, percent format). Edit either
# file, then run `jupytext --sync notebooks/01-eda.ipynb`. Outputs are stripped on
# commit, so run it top to bottom to see results.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Find the repo root from wherever the kernel starts, so any working directory works.
ROOT = next(
    p for p in [Path.cwd(), *Path.cwd().parents] if (p / "requirements.txt").exists()
)
sys.path.insert(0, str(ROOT))

from src.features import extract_title

df = pd.read_csv(ROOT / "data" / "raw" / "titanic.csv")

# %% [markdown]
# ## Overview

# %%
print(df.shape)
df.head()

# %%
df.dtypes

# %%
df.describe()

# %% [markdown]
# ## Missing values

# %%
missing = df.isna().sum()
missing = missing[missing > 0]
pd.DataFrame({"missing": missing, "percent": (missing / len(df) * 100).round(1)})

# %% [markdown]
# `Cabin` is missing for 77% of passengers, so it is a poor feature. `Age` is
# missing for 20% and will need imputing. `Embarked` is missing for only 2 rows.
# Any imputation values must be learned from the training split only.

# %% [markdown]
# ## Target balance

# %%
df["Survived"].value_counts(normalize=True).round(3)

# %% [markdown]
# 38% of passengers survived, so the classes are imbalanced but not extreme.
# Accuracy is a usable first metric; F1 shows how well the minority class is found.

# %% [markdown]
# ## Survival by sex and class

# %%
df.groupby("Sex")["Survived"].mean().round(3)

# %%
survival_by_class_sex = df.pivot_table(index="Pclass", columns="Sex", values="Survived")
survival_by_class_sex.round(2)

# %% [markdown]
# Sex is the strongest signal: 74% of women survived against 19% of men. Class
# matters too, and the two interact: nearly all first and second class women
# survived, while third class women had a coin-flip chance.

# %% [markdown]
# ## Age and fare

# %%
fig, ax = plt.subplots(figsize=(7, 4))
for survived, group in df.groupby("Survived"):
    ax.hist(group["Age"].dropna(), bins=20, alpha=0.6, label=f"Survived={survived}")
ax.set_xlabel("Age")
ax.set_ylabel("Passengers")
ax.legend()
plt.show()

# %%
known_age = df["Age"].notna()
pd.Series(
    {
        "under 12": df.loc[known_age & (df["Age"] < 12), "Survived"].mean(),
        "12 and over": df.loc[known_age & (df["Age"] >= 12), "Survived"].mean(),
    }
).round(3)

# %%
fig, ax = plt.subplots(figsize=(7, 4))
df.boxplot(column="Fare", by="Pclass", ax=ax)
ax.set_ylabel("Fare")
plt.suptitle("")
plt.show()

# %% [markdown]
# Children under 12 survived more often (57%) than older passengers (39%).
# Fare is heavily skewed and follows class: the median first class fare is
# 60.3 against 8.0 in third class, so the two features overlap.

# %% [markdown]
# ## Title from the passenger name
#
# `extract_title` lives in `src/features.py` (unit tested) so the training
# pipeline can reuse it.

# %%
df["Title"] = extract_title(df["Name"])
df.groupby("Title")["Survived"].agg(["count", "mean"]).round(2)

# %% [markdown]
# Titles separate groups that sex and age alone blur: `Master` (boys) survived
# at 57% while `Mr` survived at only 16%. `Rare` titles are a small, mixed group.

# %% [markdown]
# ## Takeaways
#
# - Sex, class and age are the main drivers of survival; fare mostly repeats class.
# - Drop `Cabin`, and impute `Age` and `Embarked` using training data only.
# - `Title` is a cheap feature worth trying as a later experiment.
