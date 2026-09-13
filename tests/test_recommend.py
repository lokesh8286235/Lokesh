from linkedin_optimizer.recommend import recommend_bullet


def test_recommendation_does_not_invent_missing_evidence() -> None:
    result = recommend_bullet("Worked on an internal Python service.")
    assert result.original == "Worked on an internal Python service."
    assert "quantified outcome" in result.missing_evidence
    assert "scale/scope" in result.missing_evidence
    assert "10K" not in result.rewritten


def test_recommendation_improves_passive_opening_without_adding_facts() -> None:
    result = recommend_bullet("Worked on a Python service that reduced latency by 30%.")
    assert result.rewritten.startswith("Built ")
    assert "30%" in result.rewritten
