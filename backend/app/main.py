from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import resumes, jobs

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins_list,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/health")
def health_check():
  return {"status": "ok", "environment": settings.ENVIRONMENT}

app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])