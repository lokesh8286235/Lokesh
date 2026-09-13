def semantic_similarity(profile_text: str, role_text: str, model_name: str = "all-MiniLM-L6-v2") -> float:
    """Optional embedding similarity. Kept out of the core dependency set."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("Install the semantic extra first.") from exc

    model = SentenceTransformer(model_name)
    vectors = model.encode([profile_text, role_text], normalize_embeddings=True)
    return round(float(vectors[0] @ vectors[1]) * 100, 1)
