import re
from collections import Counter

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9+#.-]*")

# Small deterministic synonym groups improve matching without requiring an external model.
_SYNONYMS = {
    "ml": "machine-learning",
    "machine-learning": "ml",
    "ai": "artificial-intelligence",
    "artificial-intelligence": "ai",
    "javascript": "js",
    "js": "javascript",
    "typescript": "ts",
    "ts": "typescript",
    "postgres": "postgresql",
    "postgresql": "postgres",
}


def normalize_terms(text: str) -> list[str]:
    return [token.lower() for token in _WORD.findall(text)]


def role_alignment(profile_text: str, role_text: str) -> tuple[list[str], list[str], float]:
    """Return matched terms, missing terms, and a deterministic weighted coverage score."""
    profile = set(normalize_terms(profile_text))
    counts = Counter(normalize_terms(role_text))
    targets = {term for term, count in counts.items() if len(term) > 2 and count >= 1}

    matched: set[str] = set()
    for term in targets:
        if term in profile or _SYNONYMS.get(term) in profile:
            matched.add(term)

    missing = sorted(targets - matched)
    matched_sorted = sorted(matched)
    score = round(100.0 * len(matched_sorted) / len(targets), 1) if targets else 100.0
    return matched_sorted, missing, score
