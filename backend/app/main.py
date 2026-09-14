from fastapi import FastAPI
from app.api import sessions, stream

def create_app() -> FastAPI:
    app = FastAPI(title="Patchwork")
    app.include_router(sessions.router)
    app.include_router(stream.router)
    return app

app = create_app()
