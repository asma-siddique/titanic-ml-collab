# Contributing

## Branching model

Work flows in one direction only: short-lived branches merge into `dev`, `dev` is promoted to
`staging`, and `staging` is promoted to `main`. Only `main` is production. Nobody pushes directly
to `dev`, `staging` or `main`: every change arrives through a reviewed pull request with passing
CI.

| Branch | Purpose | Created from | Merges into |
| --- | --- | --- | --- |
| `main` | Production: released, tagged models only | — | — |
| `staging` | Release candidate, reproduced and validated before release | `main` | `main` |
| `dev` | Integration of finished work | `main` | `staging` |
| `feat/<name>` | Production code: features, pipeline changes | `dev` | `dev` |
| `data/<name>` | Dataset updates tracked with DVC | `dev` | `dev` |
| `exp/<member>-<idea>` | Exploration; may never merge | `dev` | nothing directly: cherry-pick the winner into a `feat/` branch |
| `fix/<name>` | Urgent fix to production | `main` | `main`, then back into `dev` |

Delete `feat/`, `data/` and `fix/` branches after merging. Keep `exp/` branches short-lived and
rebase them on `dev` often.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add scaling step
data: remove duplicate rows
exp: try max_depth=8
fix: correct the split ratio
```

## Merge strategy

- Pull requests into `dev` are **squash-merged**: one commit per PR keeps `dev`'s history readable.
- Release PRs (`dev` → `staging`, `staging` → `main`) and merging `main` back into `dev` use a
  **merge commit**, so the three long-lived branches never diverge.

## Pre-commit hooks

Run `pre-commit install` once in every fresh clone. From then on, every `git commit` runs:

- **ruff**: lints (with safe auto-fixes) and formats Python code.
- **nbstripout**: strips outputs and execution counts from notebooks.
- **check-added-large-files**: blocks any file over 1 MB. Data and models belong in DVC.
- **detect-secrets**: blocks API keys, tokens and passwords.
- **check-merge-conflict** and **check-yaml**: catch leftover conflict markers and broken YAML.

If a hook modifies files (ruff or nbstripout), the commit stops: run `git add` on the changed files
and commit again. Never bypass the hooks with `--no-verify`. To check every file at once, run
`pre-commit run --all-files`.

## Notebooks

Every notebook is paired with a `.py` script (jupytext, percent format), so diffs and merges read
like code.

- Create the pair once: `jupytext --set-formats ipynb,py:percent notebooks/<name>.ipynb`.
- After editing either file, run `jupytext --sync notebooks/<name>.ipynb` and commit both.
- Restart the kernel and run all cells top to bottom before opening a PR. nbstripout removes
  outputs and execution counts on commit, so the PR diff stays clean.
- Move reusable logic into `src/` with a test in `tests/`, and import it back into the notebook.

## Reproducible runs

- Put every seed, split ratio and hyperparameter in `params.yaml`; never hardcode them.
- Fit scalers, encoders and imputers on the training split only.
- Commit your code **before** running `dvc repro` or `dvc exp run`, so the `git_sha` in
  `metrics.json` matches the code that produced the result. `git_dirty: true` means it did not.
- After `dvc repro`, commit `dvc.yaml`, `dvc.lock`, `params.yaml` and `metrics.json`, then run
  `dvc push` before `git push`.

## Continuous integration

`.github/workflows/ci.yml` runs on every PR into `dev`, `staging` and `main`. Four checks must pass
before a PR can merge:

| Check | What it runs |
| --- | --- |
| `lint` | `ruff check .` and `ruff format --check .` |
| `tests` | `pytest tests/` |
| `data-checks` | `python -m src.checks.validate_data tests/data/titanic_sample.csv`: schema, allowed values, value ranges and null counts |
| `smoke-train` | `prepare`, `train` and `evaluate` end to end on the 300-row sample |

A fifth job, `metrics-comment`, posts a before/after metrics table on the PR with CML. It is
informational and not required.

To run the same checks before you push:

```
ruff check .
ruff format --check .
pytest tests/
python -m src.checks.validate_data tests/data/titanic_sample.csv
```

CI never downloads the real dataset: it uses the committed sample in `tests/data/`, so no DVC
credentials are stored in GitHub. If a check is red, fix it on your branch and push again; do not
merge around it.

## Pull requests

- A teammate reviews and approves every PR before it merges.
- All CI checks must be green before merging.
- If data or models changed, run `dvc push` **before** `git push`.

## Lessons from the project

Rules we added after things went wrong (details in `REPORT.md`):

- **Always check the base branch.** Open PRs with `.../compare/dev...<branch>`. Two early PRs (#1, #3)
  went into `main` because GitHub defaults to the default branch. The default branch is now `dev`.
- **Use one Python version: 3.11.** Python 3.14 produced a different model file hash for the same
  metrics.
- **Keep generated files on Unix line endings.** Write them with `newline="\n"` (see
  `write_metrics`); a CRLF `metrics.json` made `dvc status` report a change on every checkout (#15).
- **Set every parameter in every `dvc exp run`** (`-S train.n_estimators=... -S train.max_depth=...`).
  A run that sets only one silently inherits the other from the previous run.
- **A data PR includes its pipeline results.** After changing data, run `dvc repro` and commit
  `dvc.lock` and `metrics.json` in the same PR, and keep the data diff minimal (#10 rewrote 852 cells
  to change 2 values; #11 and #13 fixed the stale lock).
- **Save text files as UTF-8 without a BOM.** A BOM broke the PR template's first heading (#19).
- **Secret scanner exclusions:** DVC pointers, `dvc.lock` and `metrics.json` hold hashes, not secrets.

## Roles

- **Data owner:** DVC, data checks, dataset updates.
- **Model owner:** training pipeline, configs, experiments.
- **Platform owner:** CI, pre-commit, environment, releases.

Everyone codes and reviews, whatever their role.
