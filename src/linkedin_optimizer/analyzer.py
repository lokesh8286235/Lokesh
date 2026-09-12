import re
from collections import Counter

from .models import OptimizationReport, Profile, Role, Signal

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9+#.-]*")
_METRIC = re.compile(r"\b(?:\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?[KMB]?|\d+x)\b", re.I)
_STOPWORDS = {
    "about", "after", "also", "and", "are", "been", "being", "built", "for",
    "from", "have", "into", "more", "that", "the", "their", "this", "using",
    "with", "work", "worked", "you", "your", "will", "role", "team", "years",
}


def _tokens(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text) if len(w) > 2 and w.lower() not in _STOPWORDS]


def _keyword_set(text: str) -> set[str]:
    return set(_tokens(text))


def analyze(profile: Profile, role: Role) -> OptimizationReport:
    headline = profile.headline.strip()
    about = profile.about.strip()
    experience = "\n".join(x.strip() for x in profile.experience if x.strip())
    skills = " ".join(profile.skills)
    full_text = "\n".join((headline, about, experience, skills))

    role_words = Counter(_tokens(role.title + " " + role.description))
    profile_words = _keyword_set(full_text)
    target_keywords = {word for word, count in role_words.items() if count >= 1}
    matched = sorted(target_keywords & profile_words)
    missing = sorted(target_keywords - profile_words)

    signals: list[Signal] = []
    headline_score = min(100.0, 35 + min(len(headline), 120) * 0.45) if headline else 0
    signals.append(Signal(
        category="headline", name="headline_specificity", score=round(headline_score, 1),
        evidence=headline or "Headline is empty.",
        recommendation=("Keep the role and strongest technical specialization explicit."
                        if headline else "Add a specific target role and core specialization."),
    ))

    about_score = min(100.0, 25 + min(len(about), 1800) / 18) if about else 0
    signals.append(Signal(
        category="about", name="about_depth", score=round(about_score, 1),
        evidence=f"{len(about)} characters provided.",
        recommendation=("Lead with positioning, then prove it with outcomes and scope."
                        if about else "Add a concise positioning statement followed by evidence."),
    ))

    metric_count = len(_METRIC.findall(experience))
    evidence_score = min(100.0, metric_count * 25.0)
    signals.append(Signal(
        category="experience", name="measurable_evidence", score=evidence_score,
        evidence=f"Detected {metric_count} measurable value signal(s).",
        recommendation=("Preserve concrete metrics and explain what changed because of your work."
                        if metric_count else "Add truthful metrics, scale, latency, volume, reliability, or business outcomes."),
    ))

    keyword_score = 100.0 if not target_keywords else round(100 * len(matched) / len(target_keywords), 1)
    signals.append(Signal(
        category="role_alignment", name="keyword_coverage", score=keyword_score,
        evidence=f"Matched {len(matched)} of {len(target_keywords)} extracted target terms.",
        recommendation=("Coverage is strong; validate that every keyword reflects real experience."
                        if keyword_score >= 70 else "Add only missing role terms that are genuinely supported by your experience."),
    ))

    overall = round(sum(s.score for s in signals) / len(signals), 1)
    return OptimizationReport(
        overall_score=overall,
        signals=signals,
        matched_keywords=matched,
        missing_keywords=missing,
    )
