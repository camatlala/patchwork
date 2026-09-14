from dataclasses import dataclass
import os

@dataclass
class Settings:
    db_path: str = os.environ.get("PATCHWORK_DB_PATH", "patchwork.db")
    sandbox_image: str = os.environ.get("PATCHWORK_SANDBOX_IMAGE", "patchwork-sandbox:latest")
    max_turns: int = int(os.environ.get("PATCHWORK_MAX_TURNS", "40"))
    max_tokens_per_session: int = int(os.environ.get("PATCHWORK_MAX_TOKENS", "500000"))

settings = Settings()
