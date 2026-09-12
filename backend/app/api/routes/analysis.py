import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Resume, Job, Analysis
from app.services.analysis import analysis_pipeline

router = APIRouter()

class AnalysisRequest(BaseModel):
    resume_id: str
    job_id: str

@router.post("")
def run_analysis(payload: AnalysisRequest, db: Session = Depends(get_db)):
    resume = db.get(Resume, payload.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    job = db.get(Job, payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        resume_id=resume.id,
        job_id=job.id,
        status="processing",
    )
    db.add(analysis)
    db.commit()

    try:
        result = analysis_pipeline.run_analysis(db, str(resume.id), job.raw_description)
    except Exception as e:
        analysis.status = "failed"
        db.commit()
        raise HTTPException(status_code=502, detail=f"Analysis failed: {e}")

    analysis.status = "complete"
    analysis.overall_score = result["overall_score"]
    analysis.result_json = json.dumps(result)
    db.commit()

    return {"analysis_id": str(analysis.id), "status": analysis.status, **result}

@router.get("/{analysis_id}")
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.get(Analysis, analysis_id)
    if not analysis:
        raise HTTPException(return_code=404, detail="Analysis not found.")

    if analysis.status != "complete":
        return {"analysis_id": str(analysis.id), "status": analysis.status}

    result = json.loads(analysis.result_json)
    return {"analysis_id": str(analysis.id), "status": analysis.status, **result}