<h1 align="center">🧵 Patchwork</h1>
<p align="center"><b>AI Coding Harness</b></p>

<p align="center">
  <!-- Typing SVG by DenverCoder1 - https://github.com/DenverCoder1/readme-typing-svg -->
  <a href="https://github.com/DenverCoder1/readme-typing-svg">
    <img src="https://readme-typing-svg.demolab.com/?lines=Self-hosted+AI+coding+agent;Docker-isolated+sandbox+per+session;Token-optimized+context+pipeline;Diff-based+updates+%2B+caching+%2B+pruning&font=Fira%20Code&center=true&width=520&height=45&color=f75c7e&vCenter=true&pause=1000&size=20" /></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-14354C.svg?logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-20232a.svg?logo=react&logoColor=%2361DAFB">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-07405e.svg?logo=sqlite&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white">
  <img alt="pytest" src="https://img.shields.io/badge/Pytest-0A9EDC.svg?logo=pytest&logoColor=white">
  <img alt="Self-hosted" src="https://custom-icon-badges.demolab.com/badge/-Self--hosted-1F222E?style=flat&logoColor=white&logo=home">
</p>

<p align="center">
  Point an AI agent at a git repo. It inspects, edits, and tests code inside an isolated Docker sandbox — with relevance scoring, summarization, diffing, caching, and pruning keeping token spend down.
</p>

<br/>

<details open>
<summary><h2>🧩 Architecture</h2></summary>

FastAPI backend owns the agent loop, LLM provider adapters, Docker orchestration, and the context-optimization pipeline. React SPA frontend streams session activity over a websocket. One Docker container per session is the sandboxed execution surface — the agent loop itself runs in the backend process, never inside the container.

| Piece | Role |
|---|---|
| `app/agent/` | Turn-based agent loop + tool dispatch (read/write file, run command) |
| `app/context/` | Cache → diff → relevance score → summarize → prune pipeline |
| `app/sandbox/` | Docker session manager (`create_session` / `exec` / `destroy`) |
| `app/llm/` | Provider-agnostic adapter (Claude, OpenAI) |
| `app/api/` | REST + websocket for the frontend |

</details>

<details open>
<summary><h2>🚀 Quickstart</h2></summary>

**Prerequisites:** Python 3.11+, Node 18+, Docker daemon running, an API key for Claude and/or OpenAI.

```bash
# 1. Build the sandbox image
docker build -t patchwork-sandbox:latest docker/

# 2. Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

</details>

<details>
<summary><h2>⚙️ Environment Variables</h2></summary>

| Variable | Default | Purpose |
|---|---|---|
| `PATCHWORK_DB_PATH` | `patchwork.db` | SQLite file path |
| `PATCHWORK_SANDBOX_IMAGE` | `patchwork-sandbox:latest` | Docker image used per session |
| `PATCHWORK_MAX_TURNS` | `40` | Agent loop turn budget per session |
| `PATCHWORK_MAX_TOKENS` | `500000` | Token budget per session before pausing |
| `ANTHROPIC_API_KEY` | — | Required to use the Claude adapter |
| `OPENAI_API_KEY` | — | Required to use the OpenAI adapter |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Frontend → backend URL |

</details>

<details>
<summary><h2>🧪 Testing</h2></summary>

```bash
pytest tests/unit -v                          # pure logic, no external deps
pytest tests/integration -v -m integration    # requires Docker daemon
pytest tests/e2e -v -m e2e                    # requires Docker daemon + sandbox image built
```

</details>

<details>
<summary><h2>📌 Status</h2></summary>

Core context pipeline, LLM adapters, agent loop, REST/websocket API, and frontend skeleton are built and unit/integration tested. Docker-dependent tests (`sandbox/`, `tests/e2e`) need a live daemon to verify — run the commands above once Docker is confirmed working locally.

</details>
