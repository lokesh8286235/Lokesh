"""Rank profile improvements by expected score leverage and evidence gaps."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Improvement:
    priority: int
    signal: str
    action: str
    rationale: str


def prioritize(signals: list[dict]) -> list[Improvement]:
    """Return deterministic, actionable priorities; lower scores come first."""
    actions = {
        "business_impact": ("Add a truthful quantified outcome", "Impact is weak and usually has high recruiter signal."),
        "ownership": ("Make personal ownership explicit", "The work is harder to evaluate when contribution is ambiguous."),
        "technical_depth": ("Name the concrete system and engineering decisions", "Specific technical depth differentiates generic claims."),
        "evidence_quality": ("Strengthen proof with scope, action, and outcome", "Evidence quality is the foundation for credible claims."),
        "keyword_coverage": ("Add only missing role terms supported by experience", "Improve role fit without keyword stuffing."),
        "seniority_alignment": ("Clarify level, scope, and leadership evidence", "The target level needs explicit evidence of scope."),
        "headline_specificity": ("Tighten target role and specialization", "Recruiters should identify the positioning immediately."),
        "about_depth": ("Replace generic summary language with proof", "The About section should establish positioning and evidence."),
    }
    ranked = []
    for signal in signals:
        name = signal["name"]
        if name not in actions:
            continue
        action, rationale = actions[name]
        ranked.append((signal["score"], name, action, rationale))
    ranked.sort(key=lambda row: (row[0], row[1]))
    return [Improvement(i, name, action, rationale) for i, (_, name, action, rationale) in enumerate(ranked, 1)]
