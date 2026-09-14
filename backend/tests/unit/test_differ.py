from app.context.differ import build_diff

def test_first_read_returns_full_file():
    result = build_diff(None, "line1\nline2\n")
    assert result.startswith("FULL FILE:\n")
    assert "line1" in result

def test_unchanged_content_returns_no_diff_marker():
    result = build_diff("line1\nline2\n", "line1\nline2\n")
    assert result == "NO CHANGE"

def test_changed_content_returns_unified_diff():
    old = "line1\nline2\nline3\n"
    new = "line1\nCHANGED\nline3\n"
    result = build_diff(old, new)
    assert "-line2" in result
    assert "+CHANGED" in result
