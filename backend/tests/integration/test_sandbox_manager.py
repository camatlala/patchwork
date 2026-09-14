import pytest
from app.sandbox.docker_manager import SandboxManager

pytestmark = pytest.mark.integration

def test_create_exec_destroy_cycle():
    manager = SandboxManager(image="patchwork-sandbox:latest")
    container_id = manager.create_session("https://github.com/octocat/Hello-World.git")

    result = manager.exec(container_id, ["ls", "/workspace"])
    assert result.exit_code == 0
    assert "README" in result.stdout

    manager.destroy(container_id)

def test_exec_timeout_is_reported():
    manager = SandboxManager(image="patchwork-sandbox:latest")
    container_id = manager.create_session("https://github.com/octocat/Hello-World.git")

    result = manager.exec(container_id, ["sleep", "10"], timeout=1)
    assert result.timed_out is True

    manager.destroy(container_id)
