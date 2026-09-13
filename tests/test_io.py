import pytest

from linkedin_optimizer.io import read_text


def test_read_text_uses_utf8(tmp_path):
    path = tmp_path / "job.md"
    path.write_text("Senior ML Engineer — Python", encoding="utf-8")

    assert read_text(path) == "Senior ML Engineer — Python"


def test_read_text_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_text(tmp_path / "missing.md")
