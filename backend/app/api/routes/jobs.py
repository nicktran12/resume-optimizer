import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Job
from app.services import sanitizer
from app.services.jobs import job_scraper, job_section_detector

router = APIRouter()

class JobSubmission(BaseModel):
    url: str | None = None
    description: str | None = None

@router.post("")
def submit_job(payload: JobSubmission, db: Session = Depends(get_db)):
    if not payload.url and not payload.description:
        raise HTTPException(status_code=400, detail="Provide either a job url or a pasted description.")

    if payload.description:
        raw_text = payload.description
    else:
        try:
            raw_text = job_scraper.fetch_job_description(payload.url)
        except job_scraper.JobFetchError as e:
            raise HTTPException(status_code=422, detail=str(e))

    try:
        raw_text = sanitizer.sanitize_for_llm(raw_text, source="job description")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    findings = sanitizer.scan_for_injection(raw_text)
    if findings:
        print(f"[SECURITY] Suspicious content in job submission: {findings}")

    sections = job_section_detector.detect_sections(raw_text)
    cleaned_text = "\n\n".join(s["text"] for s in sections)

    if not cleaned_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any usable content from that job description.")
    
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        url=payload.url,
        raw_description=raw_text,
        status="ready",
    )
    db.add(job)
    db.commit()

    return {"job_id": str(job.id), "status": job.status}