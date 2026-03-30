"""
News Impact Analyzer - A-Share Market News Analysis

AI-powered multi-agent system for analyzing the impact of breaking news
on A-share market sectors.

Example usage:
    >>> from news_impact import NewsImpactAnalyzer
    >>> analyzer = NewsImpactAnalyzer(language="zh")
    >>> result = analyzer.analyze("央行宣布降准 0.5 个百分点")
    >>> print(result["bullish_top5"])
"""

__version__ = "0.1.0"
__author__ = "Yucheng Wang"
__email__ = "wangreits@163.com"

from .analyzer import NewsImpactAnalyzer
from .config import Settings
from .config import get_settings
from .models import ImpactDirection
from .models import ImpactIntensity
from .models import NewsAnalysis
from .models import SectorAnalysis
from .models import TimeHorizon
from .sectors import SECTORS
from .sectors import Sector

__all__ = [
    # Version
    "__version__",
    # Main analyzer
    "NewsImpactAnalyzer",
    # Configuration
    "Settings",
    "get_settings",
    # Models
    "NewsAnalysis",
    "SectorAnalysis",
    "ImpactDirection",
    "ImpactIntensity",
    "TimeHorizon",
    # Sectors
    "SECTORS",
    "Sector",
]
