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

## Pull requests

- A teammate reviews and approves every PR before it merges.
- If data or models changed, run `dvc push` **before** `git push`.

## Roles

- **Data owner:** DVC, data checks, dataset updates.
- **Model owner:** training pipeline, configs, experiments.
- **Platform owner:** CI, pre-commit, environment, releases.

Everyone codes and reviews, whatever their role.
