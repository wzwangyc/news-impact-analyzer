"""
News Impact Analyzer - Configuration Management

This module handles all configuration settings using pydantic-settings.
Supports both environment variables and .env files.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    
    Attributes:
        llm_api_key: API key for LLM provider (DashScope/Qwen)
        llm_base_url: Base URL for LLM API endpoint
        llm_model: Model name to use for inference
        language: Output language preference (zh/en)
        log_level: Logging level (DEBUG/INFO/WARNING/ERROR)
        max_concurrent_requests: Maximum concurrent API requests
        request_timeout: Timeout for API requests in seconds
    """
    
    # LLM Configuration
    llm_api_key: SecretStr = Field(
        default=...,
        description="API key for LLM provider",
        alias="DASHSCOPE_API_KEY",
    )
    
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Base URL for LLM API",
    )
    
    llm_model: Literal["qwen-plus", "qwen-max", "qwen-turbo"] = Field(
        default="qwen-plus",
        description="Model name for inference",
    )
    
    # Application Settings
    language: Literal["zh", "en"] = Field(
        default="zh",
        description="Output language preference",
    )
    
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level",
    )
    
    max_concurrent_requests: int = Field(
        default=5,
        description="Maximum concurrent API requests",
        ge=1,
        le=20,
    )
    
    request_timeout: int = Field(
        default=60,
        description="Timeout for API requests in seconds",
        ge=10,
        le=300,
    )
    
    # Model Settings
    temperature: float = Field(
        default=0.3,
        description="Sampling temperature for LLM",
        ge=0.0,
        le=2.0,
    )
    
    max_tokens: int = Field(
        default=2000,
        description="Maximum tokens in response",
        ge=100,
        le=8000,
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    def get_api_key(self) -> str:
        """Get API key as plain string."""
        return self.llm_api_key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()
