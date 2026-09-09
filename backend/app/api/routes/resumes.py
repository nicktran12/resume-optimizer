import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models import Resume, ResumeChunk
from app.services import s3, pdf_parser, section_detector, chunker, embeddings, sanitizer

router = APIRouter()
settings = get_settings()

@router.post("")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File exceeds the {settings.MAX_UPLOAD_MB}MB limit.")

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        pages = pdf_parser.extract_normalized_pages(contents)
        sections = section_detector.detect_sections(pages)
        chunks = chunker.chunk_sections(sections)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not chunks:
        raise HTTPException(status_code=400, details="Could not extract any usable content from this resume.")

    try:
        for c in chunks:
            c["content"] = sanitizer.sanitize_for_llm(c["content"], source=f"resume chunk {c["chunk_index"]}")
            findings = sanitizer.scan_for_injection(c["content"])
            if findings:
                print(f"[SECURITY] Suspicious content in resume chunk {c["chunk_index"]}: {findings}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        vectors = embeddings.embed_batch([c["content"] for c in chunks])
    except:
        raise HTTPException(status_code=502, details="Failed to generate embeddings. Please try again.")

    resume_id = str(uuid.uuid4())

    try:
        s3_key = s3.upload_resume(resume_id, contents)
    except Exception:
        raise HTTPException(status_code=502, details="Failed to store resume file. Please try again.")

    resume = Resume(
        id=resume_id,
        filename=file.filename or "resume.pdf",
        s3_key = s3_key,
        status="ready",
    )
    db.add(resume)
    db.flush()

    for c, vector in zip(chunks, vectors):
        db.add(
            ResumeChunk(
                resume_id=resume.id,
                chunk_index=c["chunk_index"],
                section=c["section"],
                page=c["page"],
                content=c["content"],
                embedding=vector,
            )
        )
    db.commit()

    return {
        "resume_id": str(resume.id), 
        "filename": resume.filename, 
        "status": resume.status,
        "chunk_count": len(chunks),
    }

@router.delete("/{resume_id}")
def delete_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    s3.delete_resume(resume_id)
    db.delete(resume)
    db.commit()

    return {"resume_id": resume_id, "deleted": True}