"""Transparent, anti-gaming scoring primitives for profile evidence."""

import re

# Count quantities that look like evidence, while avoiding bare years such as 2021.
_METRIC = re.compile(
    r"\b(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?[KMB]\+?|\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[KMB]?|\d+(?:\.\d+)?x)\b",
    re.I,
)
_SCOPE = re.compile(
    r"\b(?:users?|customers?|documents?|queries?|requests?|records?|services?|teams?|"
    r"gpus?|nodes?|instances?|systems?|applications?|transactions?|images?|events?)\b", re.I,
)
_OWNERSHIP = re.compile(
    r"\b(?:owned|led|drove|spearheaded|architected|designed|built|developed|implemented|"
    r"launched|delivered|migrated|automated|integrated|deployed|optimized|created|"
    r"established|introduced|refactored)\b", re.I,
)
_TECHNICAL = re.compile(
    r"\b(?:python|java|typescript|javascript|react|next\.js|fastapi|spring|kafka|"
    r"postgres(?:ql)?|mysql|sql|aws|azure|gcp|docker|kubernetes|terraform|airflow|"
    r"pytorch|tensorflow|langchain|llm|rag|mlir|onnx|graphql|redis|snowflake|"
    r"microservices?|distributed|caching|observability|vector|quantization|inference|"
    r"c\+\+|multithreading|profiling)\b", re.I,
)
_IMPACT = re.compile(
    r"\b(?:revenue|cost|costs|savings|saved|conversion|retention|uptime|availability|"
    r"sla|manual|hours?|throughput|latency|errors?|accuracy|precision|recall|incidents?|"
    r"tickets?|transactions?)\b", re.I,
)
_CAUSAL = re.compile(
    r"\b(?:reducing|reduced|increasing|increased|improving|improved|saving|saved|"
    r"cut|cuts|lowered|raised|grew|boosted|enabled|resulting|resulted)\b[^.!?]{0,100}"
    r"(?:\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[KMB]?|\d+(?:\.\d+)?x|\d+(?:\.\d+)?[KMB]\+?)\b",
    re.I,
)


def _score(count: int, step: float, cap: float = 100.0) -> float:
    return round(min(cap, count * step), 1)


def ownership_score(text: str) -> tuple[float, dict[str, int]]:
    """Reward distinct ownership signals with diminishing returns to resist verb stuffing."""
    terms = {match.group(0).lower() for match in _OWNERSHIP.finditer(text)}
    # The first few distinct signals matter most; additional verbs add progressively less.
    weights = (18.0, 14.0, 10.0, 7.0, 5.0, 4.0, 3.0)
    score = sum(weights[min(i, len(weights) - 1)] for i in range(len(terms)))
    return round(min(100.0, score), 1), {"ownership_signals": len(terms)}


def technical_depth_score(text: str) -> tuple[float, dict[str, int]]:
    """Reward technical breadth across concrete stack and systems concepts."""
    terms = {m.group(0).lower() for m in _TECHNICAL.finditer(text)}
    return _score(len(terms), 9), {"technical_signals": len(terms)}


def business_impact_score(text: str) -> tuple[float, dict[str, int]]:
    """Reward meaningful outcomes, with stronger credit for quantified impact."""
    metrics = len(_METRIC.findall(text))
    impact_terms = len({m.group(0).lower() for m in _IMPACT.finditer(text)})
    scope_terms = len({m.group(0).lower() for m in _SCOPE.finditer(text)})
    causal_links = len(_CAUSAL.findall(text))
    score = min(100.0, metrics * 22 + causal_links * 18 + impact_terms * 5 + scope_terms * 4)
    return round(score, 1), {
        "metrics": metrics,
        "causal_links": causal_links,
        "impact_terms": impact_terms,
        "scope_terms": scope_terms,
    }


def profile_quality(text: str) -> dict[str, float | dict[str, int]]:
    """Return independent dimensions; no single keyword family can dominate."""
    ownership, ownership_signals = ownership_score(text)
    technical, technical_signals = technical_depth_score(text)
    impact, impact_signals = business_impact_score(text)
    evidence = min(100.0, ownership * 0.35 + technical * 0.25 + impact * 0.40)
    return {
        "ownership": ownership,
        "technical_depth": technical,
        "business_impact": impact,
        "evidence_quality": round(evidence, 1),
        "ownership_signals": ownership_signals,
        "technical_signals": technical_signals,
        "impact_signals": impact_signals,
    }
