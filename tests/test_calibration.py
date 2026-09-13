import json
from pathlib import Path

from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role

CASES = json.loads((Path(__file__).parents[1] / "eval" / "v2_cases.json").read_text(encoding="utf-8"))


def _report(name: str):
    case = next(case for case in CASES if case["name"] == name)
    return analyze_v2(Profile.model_validate(case["profile"]), Role.model_validate(case["role"]))


def _score(report, name: str) -> float:
    return next(signal.score for signal in report.signals if signal.name == name)


def test_strong_evidence_beats_keyword_stuffing() -> None:
    strong = _report("strong evidence")
    stuffed = _report("keyword stuffed")
    assert strong.overall_score > stuffed.overall_score
    assert _score(strong, "business_impact") > _score(stuffed, "business_impact")


def test_technical_depth_without_impact_is_not_treated_as_strong_impact() -> None:
    report = _report("technical but weak impact")
    assert _score(report, "technical_depth") >= 50
    assert _score(report, "business_impact") < 50


def test_generic_profile_scores_below_evidence_rich_profile() -> None:
    assert _report("generic").overall_score < _report("strong evidence").overall_score
