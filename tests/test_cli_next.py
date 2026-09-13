from linkedin_optimizer.cli_next import render_comparison, render_report
from linkedin_optimizer.models import ComparisonReport, OptimizationReport, Signal


def test_render_report_contains_core_sections():
    report = OptimizationReport(
        overall_score=87.4,
        signals=[
            Signal(
                category="profile",
                name="Evidence quality",
                score=92,
                evidence="Metrics present",
                recommendation="Keep measurable outcomes visible.",
            )
        ],
        matched_keywords=["Python", "FastAPI"],
        missing_keywords=["Kubernetes"],
    )

    output = render_report(report)

    assert "87.4 / 100" in output
    assert "MATCHED" in output
    assert "✓ Python" in output
    assert "GAPS" in output
    assert "! Kubernetes" in output
    assert "RECOMMENDATIONS" in output
    assert "Keep measurable outcomes visible." in output


def test_render_report_handles_empty_keyword_sets():
    report = OptimizationReport(
        overall_score=50,
        signals=[],
        matched_keywords=[],
        missing_keywords=[],
    )

    output = render_report(report)

    assert "— None detected" in output
    assert "✓ No keyword gaps detected" in output


def test_render_comparison_shows_delta_and_keyword_changes():
    report = ComparisonReport(
        before_score=71.0,
        after_score=84.5,
        score_delta=13.5,
        newly_matched_keywords=["RAG"],
        resolved_missing_keywords=["AWS"],
        remaining_missing_keywords=["Kubernetes"],
    )

    output = render_comparison(report)

    assert "71.0 / 100" in output
    assert "84.5 / 100" in output
    assert "↑ 13.5 points" in output
    assert "✓ RAG" in output
    assert "✓ AWS" in output
    assert "! Kubernetes" in output
