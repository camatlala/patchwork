from app.context.cache import ContextCache
from app.context.differ import build_diff
from app.context.scorer import rank_files
from app.context.summarizer import summarize
from app.context.pruner import prune_context

class ContextPipeline:
    def __init__(self, max_entries: int = 20, summarize_threshold_lines: int = 100):
        self.cache = ContextCache()
        self.max_entries = max_entries
        self.summarize_threshold_lines = summarize_threshold_lines
        self._scores: dict[str, float] = {}

    def assemble(self, task: str, files: dict[str, str], turn: int) -> list[dict]:
        ranked = rank_files(task, files)
        entries = []
        for file_path, score in ranked:
            self._scores[file_path] = score
            content = files[file_path]
            previous = self.cache.get(file_path)
            changed = self.cache.has_changed(file_path, content)

            if not changed and previous is not None:
                body = "NO CHANGE"
            elif previous is None:
                body = build_diff(None, content)
                if content.count("\n") + 1 > self.summarize_threshold_lines:
                    body = summarize(content)
            else:
                body = build_diff(previous, content)

            self.cache.put(file_path, content)
            entries.append({"file_path": file_path, "content": body, "score": score})

        prune_input = [
            {"file_path": e["file_path"], "score": e["score"], "turn_last_used": turn}
            for e in entries
        ]
        current_task_files = {e["file_path"] for e in entries[:1]}  # top match always kept
        kept = prune_context(prune_input, current_task_files, max_entries=self.max_entries)
        kept_paths = {e["file_path"] for e in kept}

        return [e for e in entries if e["file_path"] in kept_paths]
