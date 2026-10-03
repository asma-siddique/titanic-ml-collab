"""Helpers shared by the pipeline stages."""

import random
import subprocess
from pathlib import Path

import numpy as np
import yaml


def load_params(path: str = "params.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())


def set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def git_info() -> dict:
    """Commit SHA of HEAD, and whether the code has uncommitted changes.

    params.yaml is left out of the dirty check on purpose: `dvc exp run
    --set-param` changes it without committing.
    """
    try:
        sha = _git("rev-parse", "HEAD")
        dirty = bool(_git("status", "--porcelain", "--", "src", "dvc.yaml"))
    except (OSError, subprocess.CalledProcessError):
        return {"git_sha": "unknown", "git_dirty": None}
    return {"git_sha": sha, "git_dirty": dirty}
