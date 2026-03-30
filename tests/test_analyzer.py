"""
Tests for News Impact Analyzer

Run with: pytest tests/ -v
"""

import pytest

from news_impact import NewsImpactAnalyzer, Sector
from news_impact.models import ImpactDirection, ImpactIntensity
from news_impact.sectors import SECTORS, get_sector_names


class TestSectorDefinitions:
    """Test sector definitions and utilities."""
    
    def test_sectors_not_empty(self) -> None:
        """Test that SECTORS dictionary is not empty."""
        assert len(SECTORS) > 0
    
    def test_sectors_have_required_fields(self) -> None:
        """Test that all sectors have required fields."""
        for code, sector in SECTORS.items():
            assert sector.code == code
            assert sector.name_zh
            assert sector.name_en
            assert sector.description_zh
            assert sector.description_en
    
    def test_sector_get_name(self) -> None:
        """Test sector name retrieval in different languages."""
        sector = SECTORS["BANK"]
        assert sector.get_name("zh") == "银行"
        assert sector.get_name("en") == "Banks"
    
    def test_sector_get_description(self) -> None:
        """Test sector description retrieval in different languages."""
        sector = SECTORS["BANK"]
        assert "银行" in sector.get_description("zh")
        assert "bank" in sector.get_description("en").lower()
    
    def test_get_sector_names(self) -> None:
        """Test getting all sector names."""
        names_zh = get_sector_names("zh")
        names_en = get_sector_names("en")
        
        assert len(names_zh) == len(names_en)
        assert "BANK" in names_zh
        assert names_zh["BANK"] == "银行"
        assert names_en["BANK"] == "Banks"


class TestNewsImpactAnalyzer:
    """Test NewsImpactAnalyzer class."""
    
    @pytest.fixture
    def analyzer_zh(self) -> NewsImpactAnalyzer:
        """Create Chinese language analyzer."""
        return NewsImpactAnalyzer(language="zh")
    
    @pytest.fixture
    def analyzer_en(self) -> NewsImpactAnalyzer:
        """Create English language analyzer."""
        return NewsImpactAnalyzer(language="en")
    
    def test_analyzer_initialization(self, analyzer_zh: NewsImpactAnalyzer) -> None:
        """Test analyzer initializes correctly."""
        assert analyzer_zh.language == "zh"
        assert analyzer_zh.llm_client is not None
    
    def test_analyzer_rejects_empty_news(self, analyzer_zh: NewsImpactAnalyzer) -> None:
        """Test that empty news is rejected."""
        with pytest.raises(ValueError, match="at least 10 characters"):
            analyzer_zh.analyze("")
        
        with pytest.raises(ValueError, match="at least 10 characters"):
            analyzer_zh.analyze("太短")
    
    @pytest.mark.skip(reason="Requires API key")
    def test_analyze_news_zh(self, analyzer_zh: NewsImpactAnalyzer) -> None:
        """Test news analysis in Chinese."""
        news = "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"
        result = analyzer_zh.analyze(news)
        
        assert "news_analysis" in result
        assert "sector_analyses" in result
        assert "bullish_top5" in result
        assert "bearish_top5" in result
        assert len(result["bullish_top5"]) <= 5
        assert len(result["bearish_top5"]) <= 5
    
    @pytest.mark.skip(reason="Requires API key")
    def test_analyze_news_en(self, analyzer_en: NewsImpactAnalyzer) -> None:
        """Test news analysis in English."""
        news = "Central bank announces 0.5% RRR cut to boost economy"
        result = analyzer_en.analyze(news)
        
        assert "news_analysis" in result
        assert result["metadata"]["language"] == "en"
    
    @pytest.mark.skip(reason="Requires API key")
    def test_bullish_sectors_for_rrr_cut(
        self,
        analyzer_zh: NewsImpactAnalyzer,
    ) -> None:
        """Test that RRR cut benefits financial sectors."""
        news = "央行宣布降准 0.5 个百分点"
        result = analyzer_zh.analyze(news)
        
        # Banks and securities should be in bullish list
        bullish_codes = [s.sector_code for s in result["bullish_top5"]]
        
        # At least one financial sector should benefit
        financial_sectors = {"BANK", "SECURITIES", "INSURANCE"}
        assert bool(financial_sectors & set(bullish_codes))


class TestImpactDirection:
    """Test ImpactDirection enum."""
    
    def test_impact_direction_values(self) -> None:
        """Test impact direction enum values."""
        assert ImpactDirection.POSITIVE.value == "positive"
        assert ImpactDirection.NEGATIVE.value == "negative"
        assert ImpactDirection.NEUTRAL.value == "neutral"


class TestImpactIntensity:
    """Test ImpactIntensity enum."""
    
    def test_impact_intensity_values(self) -> None:
        """Test impact intensity enum values."""
        assert ImpactIntensity.VERY_LOW.value == 1
        assert ImpactIntensity.LOW.value == 2
        assert ImpactIntensity.MEDIUM.value == 3
        assert ImpactIntensity.HIGH.value == 4
        assert ImpactIntensity.VERY_HIGH.value == 5
    
    def test_intensity_range(self) -> None:
        """Test that intensity values are in valid range."""
        for intensity in ImpactIntensity:
            assert 1 <= intensity.value <= 5
