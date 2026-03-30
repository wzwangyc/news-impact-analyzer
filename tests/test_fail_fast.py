"""
Fail Fast Tests

Tests that verify the application fails fast on invalid inputs,
configuration errors, and edge cases.

Fail Fast Principles Tested:
1. Input validation - reject invalid inputs immediately
2. Configuration validation - fail at startup if misconfigured
3. Type safety - reject wrong types
4. Error reporting - clear, actionable error messages
5. No silent failures - all errors are reported
"""

import os

import pytest

from news_impact import NewsImpactAnalyzer
from news_impact.config import ConfigurationError
from news_impact.config import Settings
from news_impact.llm_client import LLMClient
from news_impact.llm_client import LLMClientError


class TestConfigurationValidation:
    """Test configuration validation with Fail Fast principles."""

    def test_missing_api_key_raises_error(self) -> None:
        """Fail Fast: Missing API key should fail immediately."""
        # Temporarily remove API key from environment
        original_key = os.environ.pop("DASHSCOPE_API_KEY", None)

        try:
            # Should raise ConfigurationError
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            error_msg = str(exc_info.value)
            assert "API key" in error_msg or "DASHSCOPE_API_KEY" in error_msg

        finally:
            # Restore original key
            if original_key:
                os.environ["DASHSCOPE_API_KEY"] = original_key

    def test_placeholder_api_key_rejected(self) -> None:
        """Fail Fast: Placeholder API keys should be rejected."""
        os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            assert "not configured" in str(exc_info.value).lower()

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)

    def test_short_api_key_rejected(self) -> None:
        """Fail Fast: Too short API keys should be rejected."""
        os.environ["DASHSCOPE_API_KEY"] = "too_short"

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            assert "too short" in str(exc_info.value).lower()

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)

    def test_invalid_base_url_rejected(self) -> None:
        """Fail Fast: Invalid base URL should be rejected."""
        os.environ["DASHSCOPE_API_KEY"] = "sk-valid_key_1234567890"
        os.environ["LLM_BASE_URL"] = "not-a-valid-url"

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            assert "Invalid LLM_BASE_URL" in str(exc_info.value)

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)
            os.environ.pop("LLM_BASE_URL", None)

    def test_timeout_too_low_rejected(self) -> None:
        """Fail Fast: Timeout below minimum should be rejected."""
        os.environ["DASHSCOPE_API_KEY"] = "sk-valid_key_1234567890"
        os.environ["REQUEST_TIMEOUT"] = "5"  # Below minimum of 10

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            assert "too low" in str(exc_info.value).lower()

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)
            os.environ.pop("REQUEST_TIMEOUT", None)

    def test_timeout_too_high_rejected(self) -> None:
        """Fail Fast: Timeout above maximum should be rejected."""
        os.environ["DASHSCOPE_API_KEY"] = "sk-valid_key_1234567890"
        os.environ["REQUEST_TIMEOUT"] = "500"  # Above maximum of 300

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            assert "too high" in str(exc_info.value).lower()

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)
            os.environ.pop("REQUEST_TIMEOUT", None)


class TestInputValidation:
    """Test input validation with Fail Fast principles."""

    @pytest.fixture
    def analyzer(self) -> NewsImpactAnalyzer:
        """Create analyzer for testing."""
        return NewsImpactAnalyzer(language="zh")

    def test_empty_news_rejected(self, analyzer: NewsImpactAnalyzer) -> None:
        """Fail Fast: Empty news should be rejected immediately."""
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("")

        assert "empty" in str(exc_info.value).lower()

    def test_whitespace_only_news_rejected(self, analyzer: NewsImpactAnalyzer) -> None:
        """Fail Fast: Whitespace-only news should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("   ")

        assert "whitespace" in str(exc_info.value).lower()

    def test_too_short_news_rejected(self, analyzer: NewsImpactAnalyzer) -> None:
        """Fail Fast: Too short news should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("太短")

        assert "too short" in str(exc_info.value).lower()

    def test_non_string_news_rejected(self, analyzer: NewsImpactAnalyzer) -> None:
        """Fail Fast: Non-string input should be rejected with TypeError."""
        with pytest.raises(TypeError) as exc_info:
            analyzer.analyze(123)  # type: ignore

        assert "must be a string" in str(exc_info.value).lower()

    def test_none_news_rejected(self, analyzer: NewsImpactAnalyzer) -> None:
        """Fail Fast: None input should be rejected with TypeError."""
        with pytest.raises(TypeError) as exc_info:
            analyzer.analyze(None)  # type: ignore

        assert "must be a string" in str(exc_info.value).lower()

    def test_valid_news_accepted(self, analyzer: NewsImpactAnalyzer) -> None:
        """Verify that valid news is accepted (doesn't fail validation)."""
        # This will fail at API level (no mock), but should pass input validation
        try:
            analyzer.analyze("央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元")
        except LLMClientError:
            # Expected - API call will fail without proper mocking
            # But input validation passed
            pass


class TestLLMClientValidation:
    """Test LLM client validation with Fail Fast principles."""

    @pytest.fixture
    def llm_client(self) -> LLMClient:
        """Create LLM client for testing."""
        return LLMClient()

    def test_empty_prompt_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: Empty prompt should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            llm_client.generate("")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_short_prompt_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: Too short prompt should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            llm_client.generate("太短")

        assert "too short" in str(exc_info.value).lower()

    def test_invalid_temperature_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: Invalid temperature should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            llm_client.generate("Valid prompt that is long enough", temperature=-1.0)

        assert "temperature" in str(exc_info.value).lower()

    def test_invalid_max_tokens_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: Invalid max_tokens should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            llm_client.generate("Valid prompt that is long enough", max_tokens=50)

        assert "max_tokens" in str(exc_info.value).lower()

    def test_none_prompt_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: None prompt should be rejected."""
        with pytest.raises((ValueError, TypeError)):
            llm_client.generate(None)  # type: ignore

    def test_non_string_prompt_rejected(self, llm_client: LLMClient) -> None:
        """Fail Fast: Non-string prompt should be rejected."""
        with pytest.raises((ValueError, TypeError)):
            llm_client.generate(123)  # type: ignore


class TestErrorMessages:
    """Test that error messages are clear and actionable."""

    def test_configuration_error_has_guidance(self) -> None:
        """Fail Fast: Configuration errors should include fix instructions."""
        os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                Settings()

            error_msg = str(exc_info.value)
            # Error message should tell user what to do
            assert any(
                word in error_msg.lower()
                for word in [
                    "configure",
                    "set",
                    "get",
                    "https://",
                    "bailian",
                ]
            )

        finally:
            os.environ.pop("DASHSCOPE_API_KEY", None)

    def test_input_error_has_example(self) -> None:
        """Fail Fast: Input validation errors should include examples."""
        analyzer = NewsImpactAnalyzer(language="zh")

        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("太短")

        error_msg = str(exc_info.value)
        # Error message should include guidance
        assert any(
            word in error_msg.lower()
            for word in [
                "minimum",
                "example",
                "characters",
                "10",
            ]
        )
