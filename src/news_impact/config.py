"""
News Impact Analyzer - Configuration Management

This module handles all configuration settings using pydantic-settings.
Supports both environment variables and .env files.

Fail Fast: Validates all settings at startup, fails immediately if invalid.
"""

from functools import lru_cache
from typing import Literal

import structlog
from pydantic import Field
from pydantic import SecretStr
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

logger = structlog.get_logger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""

    pass


class Settings(BaseSettings):
    """
    Application settings with strict validation.

    Fail Fast Principles:
    - All required fields validated at instantiation
    - Invalid values rejected immediately
    - Clear error messages for debugging
    - No silent defaults for critical settings

    Attributes:
        llm_api_key: API key for LLM provider (DashScope/Qwen)
        llm_base_url: Base URL for LLM API endpoint
        llm_model: Model name to use for inference
        language: Output language preference (zh/en)
        log_level: Logging level (DEBUG/INFO/WARNING/ERROR)
        max_concurrent_requests: Maximum concurrent API requests
        request_timeout: Timeout for API requests in seconds
    """

    # LLM Configuration - CRITICAL, must be provided
    llm_api_key: SecretStr = Field(
        ...,
        description="API key for LLM provider",
        alias="DASHSCOPE_API_KEY",
        min_length=10,
    )

    @field_validator("llm_api_key")
    @classmethod
    def validate_api_key_not_empty(cls, v: SecretStr) -> SecretStr:
        """Ensure API key is not empty or placeholder."""
        key_value = v.get_secret_value()

        # Check for common placeholder patterns
        placeholders = [
            "your_api_key",
            "your_api_key_here",
            "placeholder",
            "xxx",
            "changeme",
        ]

        if not key_value or key_value.lower() in placeholders:
            raise ConfigurationError(
                "LLM API key is not configured. "
                "Please set DASHSCOPE_API_KEY in .env file or environment variable. "
                "Get API key from: https://bailian.console.aliyun.com/"
            )

        # Check minimum length for valid keys
        if len(key_value) < 10:
            raise ConfigurationError(
                f"LLM API key too short ({len(key_value)} chars). "
                "Expected format: sk-xxxxxxxxxxxxxxxx"
            )

        return v

    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Base URL for LLM API",
    )

    llm_model: Literal["qwen-plus", "qwen-max", "qwen-turbo"] = Field(
        default="qwen-plus",
        description="Model name for inference",
        alias="LLM_MODEL_NAME",
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
        extra="forbid",  # Fail Fast: reject unknown fields
    )

    @field_validator("llm_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Ensure base URL is valid HTTP(S) URL."""
        if not v.startswith(("http://", "https://")):
            raise ConfigurationError(
                f"Invalid LLM_BASE_URL: {v}. Must start with http:// or https://"
            )
        return v

    @field_validator("request_timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Ensure timeout is in reasonable range."""
        if v < 10:
            raise ConfigurationError(f"REQUEST_TIMEOUT too low: {v}s. Minimum: 10s")
        if v > 300:
            raise ConfigurationError(f"REQUEST_TIMEOUT too high: {v}s. Maximum: 300s")
        return v

    def get_api_key(self) -> str:
        """Get API key as plain string."""
        return self.llm_api_key.get_secret_value()

    def validate(self) -> None:
        """
        Explicit validation method for additional checks.

        Fail Fast: Call this at startup to ensure all settings are valid.

        Raises:
            ConfigurationError: If any setting is invalid
        """
        # Trigger validation by accessing all fields
        _ = self.get_api_key()
        _ = self.llm_base_url
        _ = self.llm_model
        _ = self.language

        logger.info("configuration_validated", model=self.llm_model)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance with validation.

    Fail Fast: Validates configuration on first access.
    Subsequent calls return cached instance (no re-validation).

    Returns:
        Settings: Validated application settings

    Raises:
        ConfigurationError: If configuration is invalid
    """
    try:
        settings = Settings()
        settings.validate()
        return settings
    except ConfigurationError:
        raise
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e
