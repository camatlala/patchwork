from dataclasses import dataclass, field
from app.llm.base import LLMAdapter
from app.sandbox.docker_manager import SandboxManager
from app.context.pipeline import ContextPipeline
from app.agent.tools import TOOL_SCHEMAS, dispatch_tool_call

@dataclass
class AgentTurnResult:
    done: bool
    assistant_text: str
    tool_results: list[str] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0

class AgentLoop:
    def __init__(self, llm: LLMAdapter, sandbox: SandboxManager, container_id: str, pipeline: ContextPipeline):
        self._llm = llm
        self._sandbox = sandbox
        self._container_id = container_id
        self._pipeline = pipeline
        self._turn = 0

    def run_turn(self, task: str, files: dict[str, str]) -> AgentTurnResult:
        self._turn += 1
        context_entries = self._pipeline.assemble(task, files, turn=self._turn)
        context_text = "\n\n".join(f"# {e['file_path']}\n{e['content']}" for e in context_entries)

        messages = [
            {"role": "user", "content": f"Task: {task}\n\nContext:\n{context_text}"},
        ]
        response = self._llm.complete(messages, TOOL_SCHEMAS)

        tool_results = [
            dispatch_tool_call(self._sandbox, self._container_id, call)
            for call in response.tool_calls
        ]

        return AgentTurnResult(
            done=len(response.tool_calls) == 0,
            assistant_text=response.text,
            tool_results=tool_results,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
        )
