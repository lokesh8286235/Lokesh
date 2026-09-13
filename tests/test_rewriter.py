from linkedin_optimizer.models import RewriteCandidate
from linkedin_optimizer.rewriter import generate_rewrite_candidates, validate_claim_preservation


def test_weak_bullet_gets_explicit_evidence_slots() -> None:
    candidates = generate_rewrite_candidates(["Worked on an application."])
    assert candidates
    candidate = candidates[0]
    assert candidate.missing_evidence
    assert "[add verified" in candidate.rewritten
    assert validate_claim_preservation(candidate)


def test_existing_metrics_and_technologies_are_preserved() -> None:
    candidates = generate_rewrite_candidates(
        ["Built a Python service for 10K users, reducing p95 latency by 35%."]
    )
    candidate = candidates[0]
    assert "10K" in candidate.rewritten
    assert "35%" in candidate.rewritten
    assert "Python" in candidate.rewritten
    assert validate_claim_preservation(candidate)


def test_strong_bullet_needs_no_fabricated_evidence() -> None:
    candidates = generate_rewrite_candidates(
        ["Architected a Python RAG service for 10K users, reducing p95 latency by 35% and doubling throughput."]
    )
    candidate = candidates[0]
    assert candidate.missing_evidence == []
    assert candidate.rewritten == candidate.original


def test_weakest_bullet_is_selected_first() -> None:
    candidates = generate_rewrite_candidates([
        "Architected a Python RAG service for 10K users, reducing p95 latency by 35%.",
        "Worked on an application.",
    ], limit=1)
    assert candidates[0].original == "Worked on an application."


def test_claim_guard_rejects_removed_metric() -> None:
    candidate = RewriteCandidate(
        original="Reduced latency by 35% using Python.",
        rewritten="Reduced latency using Python.",
        rationale="bad rewrite",
    )
    assert not validate_claim_preservation(candidate)
