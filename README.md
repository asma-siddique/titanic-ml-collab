# titanic-ml-collab

Survival prediction (binary classification) on the Kaggle
[Titanic](https://www.kaggle.com/c/titanic/data) dataset, run as a team project with Git, DVC and
CI.

## Team

| Name | GitHub | Role |
| --- | --- | --- |
| Asma Siddique | `asma-siddique` | Data owner; Platform owner (pre-commit, environment) |
| Rameesha Shakeel | `Rameesha1234` | Model owner; Platform owner (CI) |

The full write-up, with reproducibility details and the experiment results, is in
[REPORT.md](REPORT.md).

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

## Pipeline

The pipeline is defined in `dvc.yaml` and has three stages. Every seed, split ratio and
hyperparameter lives in `params.yaml`.

| Stage | Command | What it does |
| --- | --- | --- |
| `prepare` | `python -m src.prepare` | Splits the raw data, fits the imputers on the training split only, writes `data/processed/` |
| `train` | `python -m src.train` | Trains the random forest and writes `models/model.joblib` |
| `evaluate` | `python -m src.evaluate` | Scores the test split and writes `metrics.json` |

From the repository root:

```bash
dvc pull      # fetch the raw data
dvc repro     # run the stages whose inputs changed
dvc metrics show
```

`metrics.json` holds the accuracy and F1 score, plus the commit SHA the run was made from
(`git_sha`) and whether `src/` or `dvc.yaml` had uncommitted changes (`git_dirty`). Commit your code
before running the pipeline, so the SHA matches the code that produced the numbers.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch naming rules, commit convention and merge
strategy.
