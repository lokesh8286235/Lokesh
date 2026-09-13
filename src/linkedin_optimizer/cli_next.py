"""Terminal reporting helpers for the LinkedIn Optimizer CLI."""

from .models import ComparisonReport, OptimizationReport


def render_report(report: OptimizationReport) -> str:
    lines = [
        "LINKEDIN OPTIMIZER",
        "────────────────────────────────────────",
        f"Overall alignment       {report.overall_score:.1f} / 100",
        "",
    ]
    lines.extend(f"{signal.name:<24} {signal.score:>5.1f}" for signal in report.signals)
    lines.append("\nMATCHED")
    lines.extend(f"✓ {keyword}" for keyword in report.matched_keywords)
    if not report.matched_keywords:
        lines.append("— None detected")
    lines.append("\nGAPS")
    lines.extend(f"! {keyword}" for keyword in report.missing_keywords)
    if not report.missing_keywords:
        lines.append("✓ No keyword gaps detected")
    lines.append("\nRECOMMENDATIONS")
    for index, signal in enumerate(report.signals, 1):
        if signal.recommendation:
            lines.append(f"{index}. {signal.recommendation}")
    return "\n".join(lines)


def render_comparison(report: ComparisonReport) -> str:
    direction = "↑" if report.score_delta > 0 else "↓" if report.score_delta < 0 else "→"
    lines = [
        "LINKEDIN OPTIMIZER · PROFILE COMPARISON",
        "────────────────────────────────────────",
        f"Before                  {report.before_score:.1f} / 100",
        f"After                   {report.after_score:.1f} / 100",
        f"Change                  {direction} {abs(report.score_delta):.1f} points",
        "\nNEW MATCHES",
    ]
    if report.newly_matched_keywords:
        lines.extend(f"✓ {keyword}" for keyword in report.newly_matched_keywords)
    else:
        lines.append("— None")
    lines.append("\nRESOLVED GAPS")
    if report.resolved_missing_keywords:
        lines.extend(f"✓ {keyword}" for keyword in report.resolved_missing_keywords)
    else:
        lines.append("— None")
    lines.append("\nREMAINING GAPS")
    if report.remaining_missing_keywords:
        lines.extend(f"! {keyword}" for keyword in report.remaining_missing_keywords)
    else:
        lines.append("— None")
    return "\n".join(lines)
