import json

from src.evaluate import write_metrics


def test_write_metrics_uses_lf_line_endings(tmp_path):
    path = tmp_path / "metrics.json"

    write_metrics({"accuracy": 0.5, "f1": 0.25}, path)

    raw = path.read_bytes()
    assert b"\r" not in raw
    assert raw.endswith(b"\n")
    assert json.loads(raw) == {"accuracy": 0.5, "f1": 0.25}
