from linkedin_optimizer.scoring import business_impact_score, ownership_score, technical_depth_score


def test_ownership_is_capped_against_verb_stuffing() -> None:
    weak = "Built and developed a service."
    stuffed = "Built developed implemented deployed automated integrated optimized migrated launched delivered."
    assert ownership_score(stuffed)[0] <= 100
    assert ownership_score(stuffed)[0] > ownership_score(weak)[0]


def test_technical_depth_rewards_distinct_system_concepts() -> None:
    shallow = "Python Python Python Python."
    deep = "Python, FastAPI, PostgreSQL, Kafka, Docker, Kubernetes, Redis, RAG, vector retrieval."
    assert technical_depth_score(deep)[0] > technical_depth_score(shallow)[0]


def test_business_impact_rewards_causal_metrics() -> None:
    vague = "Improved the application for users."
    strong = "Reduced p95 latency by 35% for 10K users and increased throughput by 2x."
    assert business_impact_score(strong)[0] > business_impact_score(vague)[0]


def test_business_impact_does_not_treat_years_as_metrics() -> None:
    score, signals = business_impact_score("Worked there from 2021 to 2023 on software.")
    assert signals["metrics"] == 0
    assert score == 0
