#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for sector definitions.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from news_impact.sectors import (
    SECTORS,
    Sector,
    get_sector_list,
    get_sector_names,
    get_sector_descriptions,
)


class TestSectorDefinition:
    """Test sector data structure."""
    
    def test_sector_has_required_fields(self) -> None:
        """Test that all sectors have required fields."""
        for code, sector in SECTORS.items():
            assert isinstance(sector, Sector)
            assert sector.code == code
            assert sector.name_zh
            assert sector.name_en
            assert sector.description_zh
            assert sector.description_en
    
    def test_sector_bilingual_names(self) -> None:
        """Test sector names in both languages."""
        bank = SECTORS["BANK"]
        assert bank.get_name("zh") == "银行"
        assert bank.get_name("en") == "Banks"
    
    def test_sector_bilingual_descriptions(self) -> None:
        """Test sector descriptions in both languages."""
        bank = SECTORS["BANK"]
        assert "银行" in bank.get_description("zh")
        assert "bank" in bank.get_description("en").lower()


class TestSectorList:
    """Test sector list utilities."""
    
    def test_get_sector_list(self) -> None:
        """Test getting list of all sector codes."""
        sectors = get_sector_list()
        
        assert isinstance(sectors, list)
        assert len(sectors) > 0
        assert "BANK" in sectors
        assert "SECURITIES" in sectors
    
    def test_get_sector_names_zh(self) -> None:
        """Test getting sector names in Chinese."""
        names = get_sector_names("zh")
        
        assert isinstance(names, dict)
        assert names["BANK"] == "银行"
        assert names["SECURITIES"] == "证券"
    
    def test_get_sector_names_en(self) -> None:
        """Test getting sector names in English."""
        names = get_sector_names("en")
        
        assert isinstance(names, dict)
        assert names["BANK"] == "Banks"
        assert names["SECURITIES"] == "Securities"
    
    def test_get_sector_descriptions(self) -> None:
        """Test getting sector descriptions."""
        descriptions = get_sector_descriptions("zh")
        
        assert isinstance(descriptions, dict)
        assert len(descriptions) == len(SECTORS)
        assert "银行" in descriptions["BANK"]


class TestSectorCoverage:
    """Test sector coverage completeness."""
    
    def test_all_major_sectors_present(self) -> None:
        """Test that all major A-share sectors are present."""
        required_sectors = [
            "BANK", "INSURANCE", "SECURITIES",  # Financial
            "REAL_ESTATE", "BUILDING_MATERIALS", "CONSTRUCTION",  # Real estate
            "STEEL", "COAL", "PETROCHEMICALS", "NONFERROUS_METALS",  # Materials
            "AUTOMOTIVE", "MACHINERY", "DEFENSE", "HOME_APPLIANCES",  # Manufacturing
            "ELECTRONICS", "COMPUTER", "COMMUNICATION",  # Technology
            "PHARMA",  # Healthcare
            "FOOD_BEVERAGE", "TEXTILES", "LIGHT_INDUSTRY", "RETAIL",  # Consumer
            "CONSUMER_SERVICES", "BEAUTY_CARE",
            "UTILITIES", "TRANSPORTATION",  # Utilities
            "AGRICULTURE",  # Agriculture
            "MEDIA", "ENVIRONMENTAL",  # Others
        ]
        
        for sector in required_sectors:
            assert sector in SECTORS, f"Missing sector: {sector}"
    
    def test_sector_count(self) -> None:
        """Test total number of sectors."""
        # Should have 28 major sectors (SW Level 1)
        assert len(SECTORS) >= 25  # At least 25 sectors
