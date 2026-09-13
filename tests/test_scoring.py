from linkedin_optimizer.scoring import business_impact_score, ownership_score, technical_depth_score


def test_ownership_is_diminishing_and_resists_repetition() -> None:
    weak = "Built and developed a service."
    stuffed = "Built built built built built built built built."
    diverse = "Architected, deployed, optimized, and automated a service."
    assert ownership_score(stuffed)[0] == ownership_score("Built a service.")[0]
    assert ownership_score(diverse)[0] > ownership_score(weak)[0]


def test_technical_depth_rewards_distinct_system_concepts() -> None:
    shallow = "Python Python Python Python."
    deep = "Python, FastAPI, PostgreSQL, Kafka, Docker, Kubernetes, Redis, RAG, vector retrieval."
    assert technical_depth_score(deep)[0] > technical_depth_score(shallow)[0]


def test_business_impact_rewards_causal_metrics() -> None:
    vague = "Improved the application for users."
    strong = "Reduced p95 latency by 35% for 10K users and increased throughput by 2x."
    score, signals = business_impact_score(strong)
    assert score > business_impact_score(vague)[0]
    assert signals["metrics"] >= 3
    assert signals["causal_links"] >= 2


def test_business_impact_recognizes_scaled_quantities_but_not_years() -> None:
    profile = "Processed 500K+ images, indexed 10K+ documents, and served 1,000+ queries/day."
    score, signals = business_impact_score(profile)
    assert signals["metrics"] == 3
    assert score > 0

    year_only, year_signals = business_impact_score("Worked there from 2021 to 2023 on software.")
    assert year_signals["metrics"] == 0
    assert year_only == 0
