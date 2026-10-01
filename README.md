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

The dataset is the [Kaggle Titanic](https://www.kaggle.com/c/titanic/data) training set (891
passengers). Datasets are never committed to Git: `data/raw/titanic.csv.dvc` is a small pointer to
the file, which is stored in a DVC remote on [DagsHub](https://dagshub.com).

To fetch the data, add your DagsHub username and access token to your local, git-ignored DVC
config (get the token under DagsHub → Your Settings → Tokens), then pull:

```bash
dvc remote modify --local storage auth basic
dvc remote modify --local storage user <your DagsHub username>
dvc remote modify --local storage password <your DagsHub token>
dvc pull
```

Never commit the token. `--local` writes it to `.dvc/config.local`, which Git ignores.

## Train

From the repository root:

```bash
python src/train.py
```

This prints the accuracy on a held-out 20% split and saves the model to `models/model.joblib`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch naming rules, commit convention and merge
strategy.
