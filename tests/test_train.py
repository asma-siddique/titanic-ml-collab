import pytest

from src.train import build_model

PARAMS = {"model": "random_forest", "n_estimators": 7, "max_depth": 3}


def test_build_model_uses_params_and_seed():
    model = build_model(PARAMS, seed=11)

    assert model.n_estimators == 7
    assert model.max_depth == 3
    assert model.random_state == 11


def test_build_model_rejects_unknown_model():
    with pytest.raises(ValueError, match="Unknown model"):
        build_model({**PARAMS, "model": "svm"}, seed=1)
