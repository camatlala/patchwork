from app.context.pruner import prune_context

def test_current_task_files_always_kept():
    entries = [
        {"file_path": "a.py", "score": 0.1, "turn_last_used": 1},
        {"file_path": "b.py", "score": 0.9, "turn_last_used": 1},
    ]
    result = prune_context(entries, current_task_files={"a.py"}, max_entries=1)
    paths = {e["file_path"] for e in result}
    assert "a.py" in paths

def test_fills_remaining_slots_by_score():
    entries = [
        {"file_path": "a.py", "score": 0.1, "turn_last_used": 1},
        {"file_path": "b.py", "score": 0.9, "turn_last_used": 1},
        {"file_path": "c.py", "score": 0.5, "turn_last_used": 1},
    ]
    result = prune_context(entries, current_task_files=set(), max_entries=2)
    paths = {e["file_path"] for e in result}
    assert paths == {"b.py", "c.py"}
