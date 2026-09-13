from linkedin_optimizer.matcher import normalize_terms, role_similarity


def test_common_aliases_normalize():
    terms = normalize_terms("ML engineer with K8s, Postgres and RAG")
    assert {"machine-learning", "kubernetes", "postgresql", "retrieval-augmented-generation"} <= terms


def test_role_similarity_is_transparent():
    assert role_similarity("Python FastAPI Kubernetes", "Python K8s FastAPI") == 100.0
