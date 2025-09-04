from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    app_port: int = 8000
    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "mistral"

    class Config:
        env_file = ".env"

settings = Settings()
