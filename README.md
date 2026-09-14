# Patchwork — AI Coding Harness

Self-hosted webapp where an AI agent inspects, edits, and tests code inside an isolated Docker sandbox, with token-optimized context (relevance scoring, summarization, diffing, caching, pruning).

## Prerequisites

- Python 3.11+
- Node 18+ / npm
- Docker daemon running (required for sandbox execution — Tasks touching `sandbox/` and the e2e test need it)
- An API key for at least one LLM provider (Anthropic and/or OpenAI)

## Build the sandbox image

```bash
docker build -t patchwork-sandbox:latest docker/
```

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables (all optional, shown with defaults):

| Variable | Default | Purpose |
|---|---|---|
| `PATCHWORK_DB_PATH` | `patchwork.db` | SQLite file path |
| `PATCHWORK_SANDBOX_IMAGE` | `patchwork-sandbox:latest` | Docker image used per session |
| `PATCHWORK_MAX_TURNS` | `40` | Agent loop turn budget per session |
| `PATCHWORK_MAX_TOKENS` | `500000` | Token budget per session before pausing |
| `ANTHROPIC_API_KEY` | — | Required to use the Claude adapter |
| `OPENAI_API_KEY` | — | Required to use the OpenAI adapter |

Run tests:

```bash
pytest tests/unit -v                    # no external deps
pytest tests/integration -v -m integration   # requires Docker daemon
pytest tests/e2e -v -m e2e                   # requires Docker daemon + sandbox image built
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` if the backend isn't on `http://localhost:8000`.
