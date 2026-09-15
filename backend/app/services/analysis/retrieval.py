from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ResumeChunk
from app.services.resumes import embeddings

EVIDENCE_SECTIONS = {"Experience", "Projects"}
EVIDENCE_SECTION_BOOST = 0.85
TOP_K = 3

def retrieve_evidence_with_vector(
    db: Session, resume_id: str, query_vector: list[float], category: str = "required_skill"
) -> list[dict]:
    distance = ResumeChunk.embedding.cosine_distance(query_vector)
    stmt = (
        select(ResumeChunk)
        .where(ResumeChunk.resume_id == resume_id)
        .order_by(distance)
    )
    candidates = db.execute(stmt).all()

    scored = []
    for chunk, raw_distance in candidates:
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

def retrieve_evidence(db: Session, resume_id: str, requirement_text: str, category: str = "required_skill") -> list[dict]:
    query_vector = embeddings.embed_text(requirement_text)
    return retrieve_evidence_with_vector(db, resume_id, query_vector, category)    

def _section_weight(section: str, category: str) -> float:
    if category == "education":
        return EVIDENCE_SECTION_BOOST if section == "Education" else 1.0
    return EVIDENCE_SECTION_BOOST if section in EVIDENCE_SECTIONS else 1.0