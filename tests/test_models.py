#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for data models.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from news_impact.models import (
    ImpactDirection,
    ImpactIntensity,
    NewsAnalysis,
    SectorAnalysis,
    AnalysisRequest,
    AnalysisResponse,
)


class TestImpactDirection:
    """Test impact direction enum."""
    
    def test_positive_value(self) -> None:
        """Test positive impact direction."""
        assert ImpactDirection.POSITIVE.value == "positive"
    
    def test_negative_value(self) -> None:
        """Test negative impact direction."""
        assert ImpactDirection.NEGATIVE.value == "negative"
    
    def test_neutral_value(self) -> None:
        """Test neutral impact direction."""
        assert ImpactDirection.NEUTRAL.value == "neutral"


class TestImpactIntensity:
    """Test impact intensity enum."""
    
    def test_intensity_values(self) -> None:
        """Test all intensity values."""
        assert ImpactIntensity.VERY_LOW.value == 1
        assert ImpactIntensity.LOW.value == 2
        assert ImpactIntensity.MEDIUM.value == 3
        assert ImpactIntensity.HIGH.value == 4
        assert ImpactIntensity.VERY_HIGH.value == 5
    
    def test_intensity_range(self) -> None:
        """Test intensity values are in valid range."""
        for intensity in ImpactIntensity:
            assert 1 <= intensity.value <= 5


class TestNewsAnalysis:
    """Test news analysis model."""
    
    def test_valid_news_analysis(self) -> None:
        """Test valid news analysis creation."""
        analysis = NewsAnalysis(
            event_type="policy",
            overall_direction=ImpactDirection.POSITIVE,
            overall_intensity=ImpactIntensity.HIGH,
            key_facts=["Fact 1", "Fact 2"],
            raw_analysis="Test analysis",
        )
        
        assert analysis.event_type == "policy"
        assert analysis.overall_direction == ImpactDirection.POSITIVE
        assert analysis.overall_intensity == ImpactIntensity.HIGH
    
    def test_news_analysis_with_related_sectors(self) -> None:
        """Test news analysis with related sectors."""
        analysis = NewsAnalysis(
            event_type="macro",
            related_sectors=["BANK", "SECURITIES"],
            overall_direction=ImpactDirection.POSITIVE,
            overall_intensity=ImpactIntensity.MEDIUM,
            key_facts=["Central bank announces RRR cut"],
            raw_analysis="Test",
        )
        
        assert len(analysis.related_sectors) == 2
        assert "BANK" in analysis.related_sectors


class TestSectorAnalysis:
    """Test sector analysis model."""
    
    def test_valid_sector_analysis(self) -> None:
        """Test valid sector analysis creation."""
        analysis = SectorAnalysis(
            sector_code="BANK",
            sector_name="银行",
            direction=ImpactDirection.POSITIVE,
            intensity=ImpactIntensity.HIGH,
            time_horizon="short_term",
            direct_impact="Liquidity improvement",
            indirect_impact="Lower funding costs",
            key_logic="RRR cut → more liquidity",
            confidence=0.85,
            raw_analysis="Test",
        )
        
        assert analysis.sector_code == "BANK"
        assert analysis.confidence == 0.85
    
    def test_sector_analysis_invalid_confidence(self) -> None:
        """Test that invalid confidence is rejected."""
        with pytest.raises(Exception):
            SectorAnalysis(
                sector_code="BANK",
                sector_name="银行",
                direction=ImpactDirection.POSITIVE,
                intensity=ImpactIntensity.HIGH,
                time_horizon="short_term",
                direct_impact="Test",
                indirect_impact="Test",
                key_logic="Test",
                confidence=1.5,  # > 1.0
                raw_analysis="Test",
            )


class TestAnalysisRequest:
    """Test analysis request model."""
    
    def test_valid_request(self) -> None:
        """Test valid analysis request."""
        request = AnalysisRequest(
            news_text="央行宣布降准 0.5 个百分点",
            language="zh",
            include_raw=True,
        )
        
        assert request.language == "zh"
        assert request.include_raw is True
    
    def test_invalid_language(self) -> None:
        """Test invalid language is rejected."""
        with pytest.raises(Exception):
            AnalysisRequest(
                news_text="Test news",
                language="invalid",  # Only zh/en allowed
            )
    
    def test_short_news_rejected(self) -> None:
        """Test that too short news is rejected."""
        with pytest.raises(Exception):
            AnalysisRequest(
                news_text="太短",  # < 10 chars
            )


class TestAnalysisResponse:
    """Test analysis response model."""
    
    def test_successful_response(self) -> None:
        """Test successful analysis response."""
        response = AnalysisResponse(
            success=True,
            processing_time_ms=1234,
        )
        
        assert response.success is True
        assert response.processing_time_ms == 1234
    
    def test_failed_response(self) -> None:
        """Test failed analysis response."""
        response = AnalysisResponse(
            success=False,
            error="Analysis failed",
            processing_time_ms=100,
        )
        
        assert response.success is False
        assert response.error == "Analysis failed"
