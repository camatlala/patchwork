import os
import shutil
import subprocess
import tempfile
import pytest
from app.sandbox.docker_manager import SandboxManager
from app.agent.tools import dispatch_tool_call
from app.llm.base import ToolCall

pytestmark = pytest.mark.e2e

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "tiny_repo")


@pytest.fixture
def tiny_git_repo():
    """Copies the fixture files into a fresh temp dir and inits a real git repo there,
    so the fixture source itself stays free of a nested .git."""
    tmp_dir = tempfile.mkdtemp(prefix="patchwork_tiny_repo_")
    for name in os.listdir(FIXTURE_PATH):
        src = os.path.join(FIXTURE_PATH, name)
        if os.path.isfile(src):
            shutil.copy(src, tmp_dir)
    subprocess.run(["git", "init", "-q"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_dir, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp_dir, check=True)
    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_agent_can_fix_bug_and_pass_tests(tiny_git_repo):
    # Bind-mount the fixture directly instead of git-cloning a file:// URL:
    # the sandbox container runs inside Docker Desktop's Linux VM, which
    # can't resolve a host filesystem path via `git clone file://...`.
    manager = SandboxManager(image="patchwork-sandbox:latest")
    container = manager._client.containers.run(
        "patchwork-sandbox:latest",
        detach=True,
        working_dir="/workspace",
        volumes={tiny_git_repo: {"bind": "/workspace", "mode": "rw"}},
    )
    container_id = container.id

    fixed_content = "def add(a, b):\n    return a + b\n"
    write_call = ToolCall(id="1", name="write_file", arguments={"path": "calc.py", "content": fixed_content})
    dispatch_tool_call(manager, container_id, write_call)

    run_call = ToolCall(id="2", name="run_command", arguments={"command": ["python", "-m", "pytest", "test_calc.py"]})
    output = dispatch_tool_call(manager, container_id, run_call)

    assert "1 passed" in output
    manager.destroy(container_id)
