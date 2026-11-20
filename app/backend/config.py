import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "AI Engineering Zero to Hero API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    ROOT_DIR: Path = BASE_DIR.parent.parent
    CURRICULUM_PATH: Path = ROOT_DIR / "app" / "frontend" / "src" / "data" / "curriculum.json"
    SQLITE_DB_PATH: Path = BASE_DIR / "ai_engineering.db"
    
    # Service URLs
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    
    # Studio & Simulation
    ENABLE_SIMULATOR_FALLBACK: bool = True
    EMBEDDING_DIM: int = 16

settings = Settings()
