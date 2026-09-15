from sqlalchemy.orm import Session

from app.services.resumes import embeddings
from app.services.analysis import requirement_extractor, retrieval, match_evaluator, scoring, recommendation_generator

def run_analysis(db: Session, resume_id: str, job_raw_description: str) -> dict:
    requirements = requirement_extractor.extract_requirements(job_raw_description)

    requirement_texts = [req.text for req in requirements]
    requirement_vectors = embeddings.embed_batch(requirement_texts)

    items_for_evaluation = []
    for i, (req, vector) in enumerate(zip(requirements, requirement_vectors)):
        evidence = retrieval.retrieve_evidence_with_vector(db, resume_id, vector, category=req.category)
        items_for_evaluation.append({"index": i, "requirement": req.text, "evidence": evidence})

    match_results = match_evaluator.evaluate_matches_batch(items_for_evaluation)
    match_by_index = {m.index: m for m in match_results}

    evaluated_requirements = []
    for i, req in enumerate(requirements):
        result = match_by_index.get(i)
        if result is None:
            match_strength, reasoning = "none", "No evaluation returned for this requirement."
        else:
            match_strength, reasoning = result.match_strength, result.reasoning

        evaluated_requirements.append(
            {
                "text": req.text,
                "category": req.category,
                "match_strength": match_strength,
                "reasoning": reasoning,
            }
        )

    score_breakdown = scoring.compute_score_breakdown(evaluated_requirements)
    overall_score = scoring.compute_overall_score(score_breakdown)

    matched_skills = [
        r["text"] for r in evaluated_requirements
        if r["category"] in ("required_skill", "preferred_skill") and r["match_strength"] == "strong"
    ]

    missing_skills = [
        r["text"] for r in evaluated_requirements
        if r["category"] in ("required_skill", "preferred_skill") and (r["match_strength"] == "none" or r["match_strength"] == "partial")
    ]

    recommendations = recommendation_generator.generate_recommendations(evaluated_requirements)

    return {
        "overall_score": overall_score,
        "score_breakdown": score_breakdown,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": [{"category": r.category, "recommendation": r.recommendation} for r in recommendations],
    }