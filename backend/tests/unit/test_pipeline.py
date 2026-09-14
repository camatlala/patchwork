from app.context.pipeline import ContextPipeline

def test_first_assemble_returns_full_or_summarized_content():
    pipeline = ContextPipeline()
    files = {"src/auth/login.py": "def authenticate(user): pass"}
    result = pipeline.assemble("fix login authentication bug", files, turn=1)

    assert len(result) == 1
    assert result[0]["file_path"] == "src/auth/login.py"
    assert "FULL FILE" in result[0]["content"]

def test_second_assemble_with_unchanged_file_returns_no_change():
    pipeline = ContextPipeline()
    files = {"src/auth/login.py": "def authenticate(user): pass"}
    pipeline.assemble("fix login authentication bug", files, turn=1)

    result = pipeline.assemble("fix login authentication bug", files, turn=2)
    assert result[0]["content"] == "NO CHANGE"

def test_assemble_prunes_low_relevance_files_beyond_limit():
    pipeline = ContextPipeline(max_entries=1)
    files = {
        "src/auth/login.py": "def authenticate(user): pass",
        "src/reports/export.py": "def export_csv(data): pass",
    }
    result = pipeline.assemble("fix login authentication bug", files, turn=1)
    assert len(result) == 1
    assert result[0]["file_path"] == "src/auth/login.py"

def test_large_first_read_is_summarized():
    pipeline = ContextPipeline()
    big_content = "\n".join(f"line{i}" for i in range(200))
    files = {"src/big.py": big_content}
    result = pipeline.assemble("fix big.py", files, turn=1)
    assert "omitted" in result[0]["content"]
