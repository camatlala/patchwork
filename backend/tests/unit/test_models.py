from app.store.db import get_engine, get_sessionmaker, init_db
from app.store.models import Session, Message, FileCacheEntry, TokenUsage

def test_create_and_query_session(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    session = Session(repo_url="https://example.com/repo.git", status="running")
    db.add(session)
    db.commit()
    db.refresh(session)

    assert session.id is not None
    assert session.status == "running"

    msg = Message(session_id=session.id, role="user", content="fix the bug")
    db.add(msg)
    db.commit()

    cache_entry = FileCacheEntry(
        session_id=session.id, file_path="src/foo.py", content_hash="abc123", content="print(1)"
    )
    db.add(cache_entry)

    usage = TokenUsage(session_id=session.id, turn=1, prompt_tokens=100, completion_tokens=50)
    db.add(usage)
    db.commit()

    assert db.query(Message).count() == 1
    assert db.query(FileCacheEntry).count() == 1
    assert db.query(TokenUsage).count() == 1
