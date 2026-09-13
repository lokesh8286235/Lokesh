"""High-level quality report helpers for CLI/API consumers."""

from .models import OptimizationReport
from .prioritize import Improvement, prioritize
from .recommend import RewriteRecommendation, recommend_bullet


def improvement_plan(report: OptimizationReport) -> list[Improvement]:
    return prioritize([signal.model_dump() for signal in report.signals])


def bullet_recommendations(experience: list[str]) -> list[RewriteRecommendation]:
    """Analyze every experience bullet without inventing unsupported facts."""
    return [recommend_bullet(bullet) for bullet in experience if bullet.strip()]
