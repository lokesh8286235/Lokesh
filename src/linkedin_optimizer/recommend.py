"""Evidence-backed rewrite recommendations; never invent facts."""

import re
from dataclasses import dataclass

_METRIC = re.compile(
    r"(?:\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\+?|\b\d+(?:\.\d+)?[KMB]\+?|"
    r"\b\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[KMB]?|\b\d+(?:\.\d+)?x\b)",
    re.IGNORECASE,
)
_SCOPE = re.compile(
    r"\b(?:\d+[KMB]?\+?\s+(?:users?|customers?|documents?|queries?|requests?|records?|teams?))\b",
    re.IGNORECASE,
)
_ACTION = re.compile(
    r"\b(?:built|developed|implemented|designed|architected|deployed|optimized|led|owned|"
    r"migrated|automated|launched|delivered)\b",
    re.IGNORECASE,
)
_IMPACT = re.compile(
    r"\b(?:reduced|increased|improved|saved|boosted|lowered|raised|grew|cut)\b[^.!?]{0,120}",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RewriteRecommendation:
    original: str
    rewritten: str
    reasons: list[str]
    missing_evidence: list[str]


def _missing(text: str) -> list[str]:
    missing = []
    if not _ACTION.search(text):
        missing.append("ownership verb")
    if not _METRIC.search(text):
        missing.append("quantified outcome")
    if not _SCOPE.search(text):
        missing.append("scale/scope")
    if not _IMPACT.search(text):
        missing.append("causal impact")
    return missing


def recommend_bullet(text: str) -> RewriteRecommendation:
    """Improve structure using only facts already present in the supplied bullet."""
    original = text.strip()
    if not original:
        return RewriteRecommendation("", "", [], ["ownership verb", "quantified outcome", "scale/scope"])

    reasons = []
    missing = _missing(original)
    if not _ACTION.search(original):
        reasons.append("Make personal ownership explicit.")
    if not _METRIC.search(original):
        reasons.append("Add a truthful metric if one exists in the source material.")
    if not _SCOPE.search(original):
        reasons.append("Add truthful scale such as users, requests, documents, or infrastructure.")
    if not _IMPACT.search(original):
        reasons.append("Connect the work to a measurable outcome when the source supports it.")

    rewritten = original
    weak_openers = ("worked on ", "helped with ", "responsible for ", "involved in ")
    lower = original.lower()
    for opener in weak_openers:
        if lower.startswith(opener):
            rewritten = "Built " + original[len(opener):].lstrip()
            reasons.append("Replaced passive framing with a concrete delivery verb; verify that 'Built' is factual.")
            break

    return RewriteRecommendation(original, rewritten, reasons, missing)
