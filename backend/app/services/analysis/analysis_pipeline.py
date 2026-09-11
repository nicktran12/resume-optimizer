from sqlalchemy.orm import Session

from app.services.analysis import requirement_extractor, retrieval, match_evaluator, scoring, recommendation_generator

def run_analysis(db: Session, resume_id: str, job_raw_description: str) -> dict:
    requirements = requirement_extractor.extract_requirements(job_raw_description)

    evaluated_requirements = []
    for req in requirements:
        evidence = retrieval.retrieve_evidence(db, resume_id, req.text, category=req.category)
        result = match_evaluator.evaluate_match(req.text, evidence)
        evaluated_requirements.append(
            {
                "text": req.text,
                "category": req.category,
                "match_strength": result.match_strength,
                "reasoning": result.reasoning,
                "evidence": evidence,
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
        if r["category"] in ("required_skill", "preferred_skill") and r["match_strength"] == "none"
    ]

    recommendations = recommendation_generator.generate_recommendations(evaluated_requirements)

    evidence_output = [
        {
            "requirement": r["text"],
            "resume_evidence": r["evidence"][0]["content"] if r["evidence"] else "No relevant evidence found.",
            "match": r["match_strength"],
        }
        for r in evaluated_requirements
    ]

    return {
        "overall_score": overall_score,
        "score_breakdown": score_breakdown,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": [{"category": r.category, "recommendation": r.recommendation} for r in recommendations],
        "evidence": evidence_output,
    }