from linkedin_optimizer.models import OptimizationReport, Signal
from linkedin_optimizer.quality_report import bullet_recommendations, improvement_plan


def test_improvement_plan_and_bullet_recommendations_are_exposed() -> None:
    report = OptimizationReport(
        overall_score=50,
        signals=[
            Signal(category="impact", name="business_impact", score=20, evidence="weak", recommendation="add proof"),
            Signal(category="technical_depth", name="technical_depth", score=80, evidence="strong", recommendation="keep"),
        ],
        matched_keywords=[],
        missing_keywords=[],
    )
    assert improvement_plan(report)[0].signal == "business_impact"
    assert bullet_recommendations(["Worked on a service."])[0].missing_evidence
