from app.context.summarizer import summarize

def test_short_content_unchanged():
    content = "\n".join(f"line{i}" for i in range(10))
    assert summarize(content, max_lines=40) == content

def test_long_content_is_truncated_with_marker():
    content = "\n".join(f"line{i}" for i in range(200))
    result = summarize(content, max_lines=40)
    lines = result.splitlines()
    assert "line0" in result
    assert "line199" in result
    assert any("omitted" in line for line in lines)
    assert len(lines) < 200
