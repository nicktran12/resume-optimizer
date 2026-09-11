MATCH_STRENGTH_VALUES = {"strong": 1.0, "partial": 0.5, "none": 0.0}

CATEGORY_WEIGHTS = {
    "required_skill": 0.60,
    "preferred_skill": 0.35,
    "education": 0.05,
}

def compute_score_breakdown(evaluated_requirements: list[dict]) -> dict:
    buckets: dict[str, list[float]] = {"required_skill": [], "preferred_skill": [], "education": []}

    for req in evaluated_requirements:
        category = req["category"]
        if category not in buckets:
            continue
        buckets[category].append(MATCH_STRENGTH_VALUES.get(req["match_strength"], 0.0))

        def category_score(values: list[float]) -> float:
            if not values:
                return 100.0
            return round((sum(values) / len(values)) * 100, 1)

    return {
        "required_skills": category_score(buckets["required_skill"]),
        "preferred_skills": category_score(buckets["preferred_skill"]),
        "education": category_score(buckets["education"]),
    }

def compute_overall_score(score_breakdown: dict) -> float:
    weighted_sum = (
        score_breakdown["required_skills"] * CATEGORY_WEIGHTS["required_skill"]
        + score_breakdown["preferred_skills"] * CATEGORY_WEIGHTS["preferred_skill"]
        + score_breakdown["education"] * CATEGORY_WEIGHTS["education"]
    )
    return round(weighted_sum, 1)