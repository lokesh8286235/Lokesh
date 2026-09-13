"""Deterministic, evidence-backed rewrite recommendations.

The rewriter never invents metrics, employers, technologies, scope, or outcomes.
When a claim is missing, it inserts an explicit evidence slot instead.
"""

import re

from .models import RewriteCandidate
from .scoring import business_impact_score, ownership_score, technical_depth_score

_METRIC_TOKEN = re.compile(
    r"(?:\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\+?|\b\d+(?:\.\d+)?[KMB]\+?|"
    r"\b\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[KMB]?|\b\d+(?:\.\d+)?x\b)",
    re.IGNORECASE,
)
_TECH_TOKEN = re.compile(
    r"\b(?:Python|Java|TypeScript|JavaScript|React|Next\.js|FastAPI|Spring|Kafka|PostgreSQL|"
    r"MySQL|SQL|AWS|Azure|GCP|Docker|Kubernetes|Terraform|Airflow|PyTorch|TensorFlow|"
    r"LangChain|LLM|RAG|MLIR|ONNX|GraphQL|Redis|Snowflake|microservices?|distributed|"
    r"caching|observability|vector|quantization|inference)\b",
    re.IGNORECASE,
)


def _sentences(text: str) -> list[str]:
    return [part.strip(" •-\t") for part in re.split(r"\n+|(?<=[.!?])\s+", text) if part.strip(" •-\t")]


def _bullet_score(text: str) -> float:
    ownership = ownership_score(text)[0]
    technical = technical_depth_score(text)[0]
    impact = business_impact_score(text)[0]
    return round(ownership * 0.35 + technical * 0.25 + impact * 0.40, 1)


def _rewrite(text: str) -> tuple[str, str, list[str]]:
    """Return a safe rewrite, rationale, and explicit evidence gaps."""
    ownership = ownership_score(text)[0]
    technical = technical_depth_score(text)[0]
    impact, impact_signals = business_impact_score(text)
    gaps: list[str] = []
    additions: list[str] = []

    if ownership < 45:
        gaps.append("personal ownership")
        additions.append("[add your verified ownership/action]")
    if technical < 45:
        gaps.append("technical specificity")
        additions.append("[add verified technologies/components]")
    if impact < 45:
        gaps.append("measurable outcome")
        additions.append("[add verified outcome: latency, cost, reliability, scale, or user impact]")
    if impact_signals["scope_terms"] == 0:
        gaps.append("scope/scale")
        additions.append("[add verified scope or scale]")

    if not additions:
        return text, "Already contains strong ownership, technical, and outcome evidence; no rewrite was needed.", []

    rewritten = text.rstrip(" .") + ". " + " ".join(additions) + "."
    rationale = "Strengthen the weakest evidence dimensions without changing the source claim."
    return rewritten, rationale, gaps


def generate_rewrite_candidates(experience: list[str], limit: int = 3) -> list[RewriteCandidate]:
    """Select the weakest experience statements and produce truth-constrained rewrites."""
    statements: list[str] = []
    for entry in experience:
        statements.extend(_sentences(entry))

    ranked = sorted(enumerate(statements), key=lambda item: (_bullet_score(item[1]), item[0]))
    candidates: list[RewriteCandidate] = []
    for _, original in ranked[:limit]:
        rewritten, rationale, missing = _rewrite(original)
        candidates.append(
            RewriteCandidate(
                original=original,
                rewritten=rewritten,
                rationale=rationale,
                missing_evidence=missing,
            )
        )
    return candidates


def validate_claim_preservation(candidate: RewriteCandidate) -> bool:
    """Reject rewrites that remove or add numeric/technology claims."""
    original_metrics = {token.lower() for token in _METRIC_TOKEN.findall(candidate.original)}
    rewritten_metrics = {token.lower() for token in _METRIC_TOKEN.findall(candidate.rewritten)}
    if not original_metrics.issubset(rewritten_metrics):
        return False
    if not rewritten_metrics.issubset(original_metrics):
        return False

    original_tech = {token.lower() for token in _TECH_TOKEN.findall(candidate.original)}
    rewritten_tech = {token.lower() for token in _TECH_TOKEN.findall(candidate.rewritten)}
    if not original_tech.issubset(rewritten_tech):
        return False
    return rewritten_tech.issubset(original_tech)
