import pytest
from app.llm.registry import get_adapter
from app.llm.claude_adapter import ClaudeAdapter
from app.llm.openai_adapter import OpenAIAdapter

def test_get_adapter_returns_claude():
    adapter = get_adapter("claude", api_key="fake-key")
    assert isinstance(adapter, ClaudeAdapter)

def test_get_adapter_returns_openai():
    adapter = get_adapter("openai", api_key="fake-key")
    assert isinstance(adapter, OpenAIAdapter)

def test_get_adapter_rejects_unknown_provider():
    with pytest.raises(ValueError):
        get_adapter("unknown-provider", api_key="fake-key")
