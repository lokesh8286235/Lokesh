from linkedin_optimizer.evidence import evidence_score


def test_evidence_score_rewards_metrics_actions_and_scope() -> None:
    score, signals = evidence_score(
        "Architected and deployed a service for 10K users, reducing latency by 35%."
    )
    assert score > 0
    assert signals["metrics"] == 2
    assert signals["actions"] == 2
    assert signals["scope_terms"] == 1


def test_evidence_score_is_zero_without_evidence_signals() -> None:
    score, signals = evidence_score("Worked on software and technology projects.")
    assert score == 0
    assert signals == {"metrics": 0, "actions": 0, "scope_terms": 0}
