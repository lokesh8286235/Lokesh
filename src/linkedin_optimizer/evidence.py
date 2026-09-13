import re

_METRIC = re.compile(r"\b(?:\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?[KMB]?|\d+x)\b", re.IGNORECASE)
_ACTION = re.compile(
    r"\b(?:built|designed|developed|architected|automated|optimized|improved|reduced|increased|"
    r"deployed|migrated|scaled|led|owned|implemented|launched|delivered|integrated)\b",
    re.IGNORECASE,
)
_SCOPE = re.compile(
    r"\b(?:users?|customers?|documents?|requests?|queries?|records?|services?|"
    r"teams?|gpus?|nodes?|instances?|systems?|applications?)\b",
    re.IGNORECASE,
)


def evidence_score(text: str) -> tuple[float, dict[str, int]]:
    """Score experience evidence using transparent, deterministic signals."""
    metrics = len(_METRIC.findall(text))
    actions = len(_ACTION.findall(text))
    scope = len(_SCOPE.findall(text))

    metric_points = min(metrics, 4) * 15
    action_points = min(actions, 4) * 7.5
    scope_points = min(scope, 4) * 5
    score = min(100.0, metric_points + action_points + scope_points)
    return round(score, 1), {"metrics": metrics, "actions": actions, "scope_terms": scope}
