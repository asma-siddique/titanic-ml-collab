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

## Pull requests

- A teammate reviews and approves every PR before it merges.
- If data or models changed, run `dvc push` **before** `git push`.

## Roles

- **Data owner:** DVC, data checks, dataset updates.
- **Model owner:** training pipeline, configs, experiments.
- **Platform owner:** CI, pre-commit, environment, releases.

Everyone codes and reviews, whatever their role.
