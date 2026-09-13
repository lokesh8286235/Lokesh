import re

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9+#.-]*")
_ALIASES = {
    "ml": "machine-learning", "ai": "artificial-intelligence", "llm": "large-language-model",
    "k8s": "kubernetes", "postgres": "postgresql", "js": "javascript", "ts": "typescript",
    "rest": "rest-api", "rag": "retrieval-augmented-generation", "genai": "generative-ai",
}


def normalize_terms(text: str) -> set[str]:
    terms = {x.lower() for x in _TOKEN.findall(text) if len(x) > 2}
    return {_ALIASES.get(x, x) for x in terms}


def role_similarity(profile_text: str, role_text: str) -> float:
    """Transparent lexical similarity with common technical aliases normalized."""
    left, right = normalize_terms(profile_text), normalize_terms(role_text)
    if not right:
        return 100.0
    return round(100 * len(left & right) / len(right), 1)
