from linkedin_optimizer.prioritize import prioritize


def test_prioritize_puts_low_score_high_leverage_gaps_first() -> None:
    result = prioritize([
        {"name": "technical_depth", "score": 80},
        {"name": "business_impact", "score": 20},
        {"name": "ownership", "score": 40},
    ])
    assert [item.signal for item in result] == ["business_impact", "ownership", "technical_depth"]
    assert result[0].priority == 1
