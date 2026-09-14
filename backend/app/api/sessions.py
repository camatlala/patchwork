from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from app.store.db import get_engine, get_sessionmaker, init_db
from app.store.models import Session as SessionModel, Message
from app.sandbox.docker_manager import SandboxManager
from app.config import settings

router = APIRouter()

_engine = get_engine(f"sqlite:///{settings.db_path}")
init_db(_engine)
_SessionLocal = get_sessionmaker(_engine)

def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateSessionRequest(BaseModel):
    repo_url: str
    task: str
    auth_token: str | None = None

class SessionResponse(BaseModel):
    session_id: int
    status: str

@router.post("/sessions", response_model=SessionResponse)
def create_session(req: CreateSessionRequest, db: DBSession = Depends(get_db)):
    session = SessionModel(repo_url=req.repo_url, status="pending")
    db.add(session)
    db.commit()
    db.refresh(session)

    db.add(Message(session_id=session.id, role="user", content=req.task))
    db.commit()

    try:
        sandbox = SandboxManager(image=settings.sandbox_image)
        container_id = sandbox.create_session(req.repo_url, req.auth_token)
        session.container_id = container_id
        session.status = "running"
        db.commit()
    except Exception:
        session.status = "failed"
        db.commit()

    return SessionResponse(session_id=session.id, status=session.status)

@router.get("/sessions/{session_id}")
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).get(session_id)
    messages = db.query(Message).filter(Message.session_id == session_id).all()
    return {
        "session_id": session.id,
        "status": session.status,
        "messages": [{"role": m.role, "content": m.content} for m in messages],
    }
