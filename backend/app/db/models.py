import uuid
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import get_settings
from app.db.database import Base

settings = get_settings()
EMBEDDING_DIM = settings.EMBEDDING_DIMENSIONS

def _uuid() -> uuid.UUID:
    return uuid.uuid4()

def _now() -> datetime:
    return datetime.now(timezone.utc)

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    filename: Mapped[str] = mapped_column(String(512))
    s3_key: Mapped[str] = mapped_column(String(1024))
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="uploaded")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    chunks: Mapped[list["ResumeChunk"]] = relationship(back_populates="resume", cascade="all, delete-orphan")

class ResumeChunk(Base):
    __tablename__ = "resume_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    section: Mapped[str] = mapped_column(String(128))
    page: Mapped[int] = mapped_column(Integer, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    resume: Mapped["Resume"] = relationship(back_populates="chunks")

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    url: Mapped[str] = mapped_column(String(2048), nullable=True)
    title: Mapped[str] = mapped_column(String(512), nullable=True)
    company: Mapped[str] = mapped_column(String(512), nullable=True)
    raw_description: Mapped[str] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    overall_score: Mapped[float] = mapped_column(nullable=True)
    result_json: Mapped[str] = mapped_column(Text, nullable=True)  # serialized structured LLM+scoring output
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)