import re

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def _tokens(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text)}

def score_relevance(task: str, file_path: str, content: str) -> float:
    task_tokens = _tokens(task)
    if not task_tokens:
        return 0.0

    path_tokens = _tokens(file_path)
    content_tokens = _tokens(content)

    path_overlap = len(task_tokens & path_tokens)
    content_overlap = len(task_tokens & content_tokens)

    path_score = path_overlap / len(task_tokens)
    content_score = content_overlap / len(task_tokens)

    score = 0.6 * path_score + 0.4 * content_score
    return max(0.0, min(1.0, score))

def rank_files(task: str, files: dict[str, str]) -> list[tuple[str, float]]:
    scored = [(path, score_relevance(task, path, content)) for path, content in files.items()]
    return sorted(scored, key=lambda pair: pair[1], reverse=True)
