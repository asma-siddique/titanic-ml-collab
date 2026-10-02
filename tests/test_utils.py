import random

import numpy as np

from src.utils import git_info, load_params, set_seeds


def test_load_params_reads_yaml(tmp_path):
    path = tmp_path / "params.yaml"
    path.write_text("seed: 7\ntrain:\n  max_depth: 3\n")

    assert load_params(str(path)) == {"seed": 7, "train": {"max_depth": 3}}


def test_set_seeds_makes_random_draws_repeatable():
    set_seeds(123)
    first = (random.random(), np.random.rand())
    set_seeds(123)
    second = (random.random(), np.random.rand())

    assert first == second


def test_git_info_has_sha_and_dirty_flag():
    info = git_info()

    assert set(info) == {"git_sha", "git_dirty"}
    assert isinstance(info["git_sha"], str) and info["git_sha"]
