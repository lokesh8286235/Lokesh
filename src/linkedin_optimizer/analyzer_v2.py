import re

from .evidence import evidence_score
from .matching import role_alignment
from .models import OptimizationReport, Profile, Role, Signal

_METRIC = re.compile(r"\b(?:\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?[KMB]?|\d+x)\b", re.I)
_SENIORITY = re.compile(
    r"\b(?:principal|staff|senior|lead|manager|director|architect|head|senior-level|mid-level|junior)\b",
    re.I,
)


def analyze_v2(profile: Profile, role: Role) -> OptimizationReport:
    """Analyze positioning, evidence, role coverage, and seniority alignment.

    Kept as a separate entry point so the existing scoring contract remains stable while
    the stronger scoring model is evaluated independently.
    """
    headline = profile.headline.strip()
    about = profile.about.strip()
    experience = "\n".join(x.strip() for x in profile.experience if x.strip())
    skills = " ".join(profile.skills)
    full_text = "\n".join((headline, about, experience, skills))
    target_text = f"{role.title} {role.description}"

    matched, missing, keyword_score = role_alignment(full_text, target_text)
    evidence, evidence_signals = evidence_score(experience)

    headline_score = min(100.0, 35 + min(len(headline), 120) * 0.45) if headline else 0.0
    about_score = min(100.0, 25 + min(len(about), 1800) / 18) if about else 0.0

    profile_levels = {x.lower() for x in _SENIORITY.findall(full_text)}
    role_levels = {x.lower() for x in _SENIORITY.findall(target_text)}
    if not role_levels:
        seniority_score = 100.0
        seniority_evidence = "No explicit seniority level detected in target role."
    elif profile_levels & role_levels:
        seniority_score = 100.0
        seniority_evidence = f"Matched seniority signal(s): {', '.join(sorted(profile_levels & role_levels))}."
    elif profile_levels:
        seniority_score = 55.0
        seniority_evidence = f"Profile signals {', '.join(sorted(profile_levels))}; target requests {', '.join(sorted(role_levels))}."
    else:
        seniority_score = 35.0
        seniority_evidence = "No explicit seniority signal found in profile."

    metric_count = len(_METRIC.findall(experience))
    impact_score = min(100.0, metric_count * 25.0)

    signals = [
        Signal(
            category="headline",
            name="headline_specificity",
            score=round(headline_score, 1),
            evidence=headline or "Headline is empty.",
            recommendation=("Keep the target role and strongest specialization explicit."
                            if headline else "Add a specific target role and core specialization."),
        ),
        Signal(
            category="about",
            name="about_depth",
            score=round(about_score, 1),
            evidence=f"{len(about)} characters provided.",
            recommendation=("Lead with positioning, then prove it with outcomes and scope."
                            if about else "Add a concise positioning statement followed by evidence."),
        ),
        Signal(
            category="experience",
            name="evidence_quality",
            score=evidence,
            evidence=(f"Metrics: {evidence_signals['metrics']}; actions: {evidence_signals['actions']}; "
                      f"scope terms: {evidence_signals['scope_terms']}.") ,
            recommendation=("Prioritize quantified outcomes, ownership verbs, and explicit scale."
                            if evidence < 80 else "Evidence is strong; keep outcomes tied to your personal contribution."),
        ),
        Signal(
            category="experience",
            name="measurable_impact",
            score=impact_score,
            evidence=f"Detected {metric_count} measurable value signal(s).",
            recommendation=("Add truthful metrics for scale, latency, reliability, cost, or business impact."
                            if impact_score < 75 else "Metrics provide useful proof; preserve the strongest outcome signals."),
        ),
        Signal(
            category="role_alignment",
            name="keyword_coverage",
            score=keyword_score,
            evidence=f"Matched {len(matched)} of {len(matched) + len(missing)} target terms.",
            recommendation=("Coverage is strong; validate that matched terms reflect real experience."
                            if keyword_score >= 70 else "Add only missing role terms genuinely supported by your experience."),
        ),
        Signal(
            category="seniority",
            name="seniority_alignment",
            score=seniority_score,
            evidence=seniority_evidence,
            recommendation=("Make scope and ownership explicit when the target role expects a higher level."
                            if seniority_score < 80 else "Seniority signals are aligned; preserve ownership and scope language."),
        ),
    ]

    weights = {
        "headline_specificity": 0.10,
        "about_depth": 0.10,
        "evidence_quality": 0.20,
        "measurable_impact": 0.15,
        "keyword_coverage": 0.30,
        "seniority_alignment": 0.15,
    }
    overall = round(sum(signal.score * weights[signal.name] for signal in signals), 1)
    return OptimizationReport(
        overall_score=overall,
        signals=signals,
        matched_keywords=matched,
        missing_keywords=missing,
    )
