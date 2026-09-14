from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """
    Configuration settings for Australian Compliance Multi-Agent Workflow.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "Australia Regulatory Compliance Agentic RAG"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: Optional[str] = None
    PRIMARY_MODEL: str = "gpt-4o"
    GRADER_MODEL: str = "gpt-4o-mini"
    MAX_RETRY_LIMIT: int = 2
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"


@lru_cache()
def get_settings() -> AgentSettings:
    return AgentSettings()
