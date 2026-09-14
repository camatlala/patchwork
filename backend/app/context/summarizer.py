def summarize(content: str, max_lines: int = 40) -> str:
    lines = content.splitlines()
    if len(lines) <= max_lines:
        return content

    half = max_lines // 2
    head = lines[:half]
    tail = lines[-half:]
    omitted = len(lines) - len(head) - len(tail)
    marker = f"... [{omitted} lines omitted] ..."
    return "\n".join(head + [marker] + tail)
