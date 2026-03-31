#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for configuration management.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from news_impact.config import Settings, get_settings


class TestSettings:
    """Test configuration settings."""
    
    def test_settings_load_from_env(self, monkeypatch) -> None:
        """Test settings load from environment variables."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key_12345")
        
        settings = Settings()
        assert settings.get_api_key() == "test_key_12345"
    
    def test_settings_default_values(self, monkeypatch) -> None:
        """Test default configuration values."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")
        
        settings = Settings()
        assert settings.llm_base_url == "https://dashscope.aliyuncs.com/compatible-mode/v1"
        assert settings.llm_model == "qwen-plus"
        assert settings.language == "zh"
    
    def test_settings_invalid_api_key(self, monkeypatch) -> None:
        """Test that invalid API key is rejected."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "your_api_key_here")
        
        with pytest.raises(Exception):
            Settings()
    
    def test_settings_invalid_timeout(self, monkeypatch) -> None:
        """Test that invalid timeout is rejected."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")
        monkeypatch.setenv("REQUEST_TIMEOUT", "5")  # Too low
        
        with pytest.raises(Exception):
            Settings()
    
    def test_get_settings_cached(self, monkeypatch) -> None:
        """Test that get_settings returns cached instance."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2  # Same cached instance


class TestModelConfig:
    """Test model configuration validation."""
    
    def test_valid_model_name(self, monkeypatch) -> None:
        """Test valid model names."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")
        monkeypatch.setenv("LLM_MODEL_NAME", "qwen-plus")
        
        settings = Settings()
        assert settings.llm_model in ["qwen-plus", "qwen-max", "qwen-turbo"]
    
    def test_invalid_model_name(self, monkeypatch) -> None:
        """Test invalid model name is rejected."""
        monkeypatch.setenv("DASHSCOPE_API_KEY", "test_key")
        monkeypatch.setenv("LLM_MODEL_NAME", "invalid-model")
        
        # Should use default instead
        settings = Settings()
        assert settings.llm_model == "qwen-plus"
