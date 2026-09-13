from pathlib import Path


def read_text(path: str | Path) -> str:
    """Read a UTF-8 text file with an explicit, predictable encoding."""
    return Path(path).read_text(encoding="utf-8")
