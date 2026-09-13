import re

from .evidence import evidence_score
from .matching import role_alignment
from .models import OptimizationReport, Profile, Role, Signal
from .rewriter import generate_rewrite_candidates
from .scoring import business_impact_score, ownership_score, technical_depth_score

_SENIORITY = re.compile(
    r"\b(?:principal|staff|senior|lead|manager|director|head|mid-level|junior)\b", re.I,
)

WEIGHTS = {
    "headline_specificity": 0.05,
    "about_depth": 0.05,
    "evidence_quality": 0.15,
    "ownership": 0.15,
    "technical_depth": 0.10,
    "business_impact": 0.15,
    "keyword_coverage": 0.25,
    "seniority_alignment": 0.10,
}


def _seniority_alignment(profile_text: str, role_text: str) -> tuple[float, str]:
    profile_levels = {x.lower() for x in _SENIORITY.findall(profile_text)}
    role_levels = {x.lower() for x in _SENIORITY.findall(role_text)}
    if not role_levels:
        return 100.0, "No explicit seniority level detected in target role."
    if profile_levels & role_levels:
        matched = ", ".join(sorted(profile_levels & role_levels))
        return 100.0, f"Matched seniority signal(s): {matched}."
    if profile_levels:
        return 55.0, (
            f"Profile signals {', '.join(sorted(profile_levels))}; "
            f"target requests {', '.join(sorted(role_levels))}."
        )
    return 35.0, "No explicit seniority signal found in profile."


def analyze_v2(profile: Profile, role: Role) -> OptimizationReport:
    """Score positioning with independent, transparent anti-gaming dimensions."""
    headline = profile.headline.strip()
    about = profile.about.strip()
    experience = "\n".join(x.strip() for x in profile.experience if x.strip())
    skills = " ".join(profile.skills)
    full_text = "\n".join((headline, about, experience, skills))
    target_text = f"{role.title} {role.description}"

    matched, missing, keyword_score = role_alignment(full_text, target_text)
    evidence, evidence_signals = evidence_score(experience)
    ownership, ownership_signals = ownership_score(experience)
    technical, technical_signals = technical_depth_score(experience)
    impact, impact_signals = business_impact_score(experience)
    seniority, seniority_evidence = _seniority_alignment(headline + "\n" + experience, target_text)
    rewrite_candidates = generate_rewrite_candidates(profile.experience)

    headline_score = min(100.0, 35 + min(len(headline), 120) * 0.45) if headline else 0.0
    about_score = min(100.0, 25 + min(len(about), 1800) / 18) if about else 0.0

    signals = [
        Signal(
            category="headline", name="headline_specificity", score=round(headline_score, 1),
            evidence=headline or "Headline is empty.",
            recommendation=("Keep the target role and strongest specialization explicit."
                            if headline else "Add a specific target role and core specialization."),
        ),
        Signal(
            category="about", name="about_depth", score=round(about_score, 1),
            evidence=f"{len(about)} characters provided.",
            recommendation=("Lead with positioning, then prove it with outcomes and scope."
                            if about else "Add a concise positioning statement followed by evidence."),
        ),
        Signal(
            category="experience", name="evidence_quality", score=evidence,
            evidence=(f"Metrics: {evidence_signals['metrics']}; actions: {evidence_signals['actions']}; "
                      f"scope terms: {evidence_signals['scope_terms']} ."),
            recommendation=("Prioritize quantified outcomes, ownership verbs, and explicit scale."
                            if evidence < 80 else "Evidence is strong; keep outcomes tied to your personal contribution."),
        ),
        Signal(
            category="experience", name="ownership", score=ownership,
            evidence=f"Distinct ownership/action signals: {ownership_signals['ownership_signals']}.",
            recommendation=("Use precise ownership verbs for work you personally delivered."
                            if ownership < 60 else "Ownership is explicit; keep claims tied to shipped work."),
        ),
        Signal(
            category="technical_depth", name="technical_depth", score=technical,
            evidence=f"Distinct technical/system signals: {technical_signals['technical_signals']}.",
            recommendation=("Name concrete systems and engineering concepts, not just generic skills."
                            if technical < 60 else "Technical depth is visible; connect technologies to engineering decisions."),
        ),
        Signal(
            category="impact", name="business_impact", score=impact,
            evidence=(f"Metrics: {impact_signals['metrics']}; causal links: {impact_signals['causal_links']}; "
                      f"impact terms: {impact_signals['impact_terms']}; scope terms: {impact_signals['scope_terms']} ."),
            recommendation=("Tie technical work to measurable speed, reliability, cost, user, or business outcomes."
                            if impact < 60 else "Impact evidence is visible; preserve the strongest causal outcomes."),
        ),
        Signal(
            category="role_alignment", name="keyword_coverage", score=keyword_score,
            evidence=f"Matched {len(matched)} of {len(matched) + len(missing)} target terms.",
            recommendation=("Coverage is strong; validate that matched terms reflect real experience."
                            if keyword_score >= 70 else "Add only missing role terms genuinely supported by experience."),
        ),
        Signal(
            category="seniority", name="seniority_alignment", score=seniority,
            evidence=seniority_evidence,
            recommendation=("Make scope and ownership explicit when the target role expects a higher level."
                            if seniority < 80 else "Seniority signals are aligned; preserve ownership and scope language."),
        ),
    ]

    overall = round(sum(signal.score * WEIGHTS[signal.name] for signal in signals), 1)
    return OptimizationReport(
        overall_score=overall, signals=signals, matched_keywords=matched, missing_keywords=missing,
        rewrite_candidates=rewrite_candidates,
    )
