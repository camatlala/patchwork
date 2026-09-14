from app.context.scorer import score_relevance, rank_files

def test_score_relevance_favors_keyword_matches():
    task = "fix the login authentication bug"
    high = score_relevance(task, "src/auth/login.py", "def authenticate(user): ...")
    low = score_relevance(task, "src/reports/export.py", "def export_csv(data): ...")
    assert high > low

def test_rank_files_orders_descending():
    task = "fix the login authentication bug"
    files = {
        "src/auth/login.py": "def authenticate(user): ...",
        "src/reports/export.py": "def export_csv(data): ...",
    }
    ranked = rank_files(task, files)
    assert ranked[0][0] == "src/auth/login.py"
    assert ranked[0][1] >= ranked[1][1]
