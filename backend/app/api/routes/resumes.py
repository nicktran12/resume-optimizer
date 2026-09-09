import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models import Resume
from app.services import s3

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

    resume_id = str(uuid.uuid4())

    try:
        s3_key = s3.upload_resume(resume_id, contents)
    except Exception:
        raise HTTPException(status_code=502, details="Failed to store resume file. Please try again.")

    resume = Resume(
        id=resume_id,
        filename=file.filename or "resume.pdf",
        s3_key = s3_key,
        status="uploaded",
    )
    db.add(resume)
    db.commit()

    return {"resume_id": str(resume.id), "filename": resume.filename, "status": resume.status}

@router.delete("/{resume_id}")
def delete_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    s3.delete_resume(resume_id)
    db.delete(resume)
    db.commit()

    return {"resume_id": resume_id, "deleted": True}