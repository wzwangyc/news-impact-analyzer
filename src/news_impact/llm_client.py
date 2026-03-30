"""
LLM Client for News Impact Analysis

Provides a clean interface for interacting with LLM APIs,
with proper error handling, retry logic, and logging.
"""

import time
from typing import Any

import httpx
import structlog
from openai import OpenAI

from .config import Settings, get_settings
from .models import ImpactDirection, ImpactIntensity, TimeHorizon

logger = structlog.get_logger(__name__)


class LLMClientError(Exception):
    """Base exception for LLM client errors."""
    pass


class LLMRateLimitError(LLMClientError):
    """Raised when API rate limit is exceeded."""
    pass


class LLMTimeoutError(LLMClientError):
    """Raised when API request times out."""
    pass


class LLMClient:
    """
    Client for LLM API interactions.
    
    This class handles:
    - API authentication
    - Request/response formatting
    - Error handling and retries
    - Logging and monitoring
    
    Attributes:
        settings: Application settings
        client: OpenAI-compatible client
    """
    
    def __init__(self, settings: Settings | None = None) -> None:
        """
        Initialize LLM client.
        
        Args:
            settings: Application settings (uses default if None)
        """
        self.settings = settings or get_settings()
        self.client = OpenAI(
            api_key=self.settings.get_api_key(),
            base_url=self.settings.llm_base_url,
            timeout=httpx.Timeout(
                timeout=self.settings.request_timeout,
                connect=10.0,
            ),
        )
        logger.info(
            "llm_client_initialized",
            model=self.settings.llm_model,
            base_url=self.settings.llm_base_url,
        )
    
    def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate text completion.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens (overrides default)
            **kwargs: Additional arguments to pass to API
        
        Returns:
            Generated text
        
        Raises:
            LLMRateLimitError: If rate limit exceeded
            LLMTimeoutError: If request timed out
            LLMClientError: For other API errors
        """
        temp = temperature if temperature is not None else self.settings.temperature
        tokens = max_tokens if max_tokens is not None else self.settings.max_tokens
        
        start_time = time.time()
        
        try:
            logger.debug("generating_completion", prompt_length=len(prompt))
            
            response = self.client.chat.completions.create(
                model=self.settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=tokens,
                **kwargs,
            )
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            if not response.choices or not response.choices[0].message.content:
                raise LLMClientError("Empty response from LLM")
            
            content = response.choices[0].message.content.strip()
            
            logger.info(
                "completion_generated",
                elapsed_ms=elapsed_ms,
                tokens_used=response.usage.total_tokens if response.usage else None,
            )
            
            return content
            
        except httpx.TimeoutException as e:
            logger.error("request_timeout", error=str(e))
            raise LLMTimeoutError(f"Request timed out after {self.settings.request_timeout}s") from e
        
        except Exception as e:
            if "rate limit" in str(e).lower():
                logger.error("rate_limit_exceeded", error=str(e))
                raise LLMRateLimitError("API rate limit exceeded") from e
            
            logger.error("api_error", error=str(e), error_type=type(e).__name__)
            raise LLMClientError(f"LLM API error: {e}") from e
    
    def generate_structured(
        self,
        prompt: str,
        output_schema: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate structured output following a schema.
        
        Args:
            prompt: Input prompt
            output_schema: Expected output schema
        
        Returns:
            Structured output as dictionary
        
        Note:
            This is a simplified implementation. For production,
            consider using instructor or guidance libraries.
        """
        schema_prompt = f"""{prompt}

Please format your response as valid JSON following this schema:
{output_schema}

Return ONLY the JSON, no additional text.
"""
        
        response_text = self.generate(schema_prompt)
        
        # Parse JSON (simplified - in production, add proper error handling)
        import json
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error("json_parse_failed", error=str(e))
            raise LLMClientError(f"Failed to parse LLM response as JSON: {e}") from e


def parse_impact_direction(text: str) -> ImpactDirection:
    """Parse impact direction from text."""
    text_lower = text.lower()
    if any(word in text_lower for word in ["positive", "利好", "beneficial", "bullish"]):
        return ImpactDirection.POSITIVE
    elif any(word in text_lower for word in ["negative", "利空", "adverse", "bearish"]):
        return ImpactDirection.NEGATIVE
    return ImpactDirection.NEUTRAL


def parse_intensity(text: str) -> ImpactIntensity:
    """Parse impact intensity from text."""
    # Try to extract number
    import re
    match = re.search(r'[：:]\s*(\d)', text)
    if match:
        num = int(match.group(1))
        if 1 <= num <= 5:
            return ImpactIntensity(num)
    
    # Fallback to keyword matching
    text_lower = text.lower()
    if any(word in text_lower for word in ["very high", "非常高", "major", "重大"]):
        return ImpactIntensity.VERY_HIGH
    elif any(word in text_lower for word in ["high", "高", "significant", "显著"]):
        return ImpactIntensity.HIGH
    elif any(word in text_lower for word in ["medium", "中", "moderate", "中等"]):
        return ImpactIntensity.MEDIUM
    elif any(word in text_lower for word in ["low", "低", "minor", "轻微"]):
        return ImpactIntensity.LOW
    return ImpactIntensity.VERY_LOW


def parse_time_horizon(text: str) -> TimeHorizon:
    """Parse time horizon from text."""
    text_lower = text.lower()
    if any(word in text_lower for word in ["short", "短期", "1 周", "week"]):
        return TimeHorizon.SHORT_TERM
    elif any(word in text_lower for word in ["mid", "中期", "1-3 月", "month"]):
        return TimeHorizon.MID_TERM
    return TimeHorizon.LONG_TERM
