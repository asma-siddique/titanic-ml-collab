# titanic-ml-collab

Survival prediction (binary classification) on the Kaggle
[Titanic](https://www.kaggle.com/c/titanic/data) dataset, run as a team project with Git, DVC and
CI.

## Team

| Name | Role |
| --- | --- |
| TBD | Data owner |
| TBD | Model owner |
| TBD | Platform owner |

## Setup

Requires Python 3.11.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pre-commit install             # once per clone: runs the checks on every commit
```

## Data

Download `train.csv` from the [Kaggle Titanic competition](https://www.kaggle.com/c/titanic/data)
and save it as `data/raw/titanic.csv`. Datasets are never committed to Git.

## Train

From the repository root:

```bash
python src/train.py
```

This prints the accuracy on a held-out 20% split and saves the model to `models/model.joblib`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch naming rules, commit convention and merge
strategy.
