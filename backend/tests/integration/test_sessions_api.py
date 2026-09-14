import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.integration

@patch("app.api.sessions.SandboxManager")
def test_create_session_returns_pending_then_id(mock_sandbox_cls, tmp_path, monkeypatch):
    monkeypatch.setenv("PATCHWORK_DB_PATH", f"sqlite:///{tmp_path}/test.db")
    mock_sandbox_cls.return_value.create_session.return_value = "container-123"

    from app.main import create_app
    app = create_app()
    client = TestClient(app)

    response = client.post("/sessions", json={"repo_url": "https://example.com/repo.git", "task": "fix bug"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("pending", "running")
    assert isinstance(body["session_id"], int)

    get_response = client.get(f"/sessions/{body['session_id']}")
    assert get_response.status_code == 200
