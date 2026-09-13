from linkedin_optimizer import bullet_recommendations, improvement_plan


def test_quality_helpers_are_public_exports() -> None:
    assert callable(bullet_recommendations)
    assert callable(improvement_plan)
