from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ResumeChunk
from app.services.resumes import embeddings

EVIDENCE_SECTIONS = {"Experience", "Projects"}

EVIDENCE_SECTION_BOOST = 0.85

CANDIDATE_POOL_SIZE = 10
TOP_K = 3

def retrieve_evidence(db: Session, resume_id: str, requirement_text: str, category: str = "required_skill") -> list[dict]:
    query_vector = embeddings.embed_text(requirement_text)

    stmt = (
        select(ResumeChunk)
        .where(ResumeChunk.resume_id == resume_id)
        .order_by(ResumeChunk.embedding.cosine_distance(query_vector))
        .limit(CANDIDATE_POOL_SIZE)
    )
    candidates = db.execute(stmt).scalars().all()

    scored = []
    for chunk in candidates:
        raw_distance = _cosine_distance(chunk.embedding, query_vector)
        weight = _section_weight(chunk.section, category)
        scored.append(
            {
                "section": chunk.section,
                "content": chunk.content,
                "distance": raw_distance * weight,
            }
        )


    scored.sort(key=lambda x: x["distance"])
    return scored[:TOP_K]

def _section_weight(section: str, category: str) -> float:
    if category == "education":
        return EVIDENCE_SECTION_BOOST if section == "Education" else 1.0
    return EVIDENCE_SECTION_BOOST if section in EVIDENCE_SECTIONS else 1.0

def _cosine_distance(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    cosine_similarity = dot / (norm_a * norm_b)
    return 1 - cosine_similarity