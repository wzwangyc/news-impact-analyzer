"""
Data Models for News Impact Analysis

Defines all data structures used throughout the application with proper
type hints and validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ImpactDirection(str, Enum):
    """Direction of impact on a sector."""
    POSITIVE = "positive"  # 利好
    NEGATIVE = "negative"  # 利空
    NEUTRAL = "neutral"    # 中性


class ImpactIntensity(str, Enum):
    """Intensity level of impact."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class EventType(str, Enum):
    """Type of news event."""
    POLICY = "policy"              # 政策发布
    REGULATION = "regulation"      # 监管行动
    COMPANY = "company"            # 公司公告
    MACRO = "macro"                # 宏观经济
    INTERNATIONAL = "international"  # 国际事件
    MARKET = "market"              # 市场动态
    OTHER = "other"                # 其他


class TimeHorizon(str, Enum):
    """Time horizon for impact."""
    SHORT_TERM = "short_term"      # 短期 (1 周)
    MID_TERM = "mid_term"          # 中期 (1-3 月)
    LONG_TERM = "long_term"        # 长期 (3 月以上)


class NewsAnalysis(BaseModel):
    """
    Analysis result of a news item.
    
    Attributes:
        event_type: Type of event
        related_sectors: List of directly related sectors
        overall_direction: Overall impact direction
        overall_intensity: Overall impact intensity
        key_facts: Key factual points
        uncertainties: Unclear or uncertain aspects
        raw_analysis: Original LLM output for reference
    """
    event_type: EventType
    related_sectors: list[str] = Field(default_factory=list)
    overall_direction: ImpactDirection
    overall_intensity: ImpactIntensity
    key_facts: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    raw_analysis: str
    
    class Config:
        use_enum_values = False


class SectorAnalysis(BaseModel):
    """
    Analysis result for a specific sector.
    
    Attributes:
        sector_code: Sector identifier
        sector_name: Sector name (in output language)
        direction: Impact direction for this sector
        intensity: Impact intensity (1-5)
        time_horizon: Expected time horizon
        direct_impact: Direct impact description
        indirect_impact: Indirect impact description
        affected_subsectors: List of affected sub-sectors
        key_logic: Core impact transmission logic
        confidence: Confidence level (0-1)
        raw_analysis: Original LLM output for reference
    """
    sector_code: str
    sector_name: str
    direction: ImpactDirection
    intensity: ImpactIntensity
    time_horizon: TimeHorizon
    direct_impact: str
    indirect_impact: str
    affected_subsectors: list[str] = Field(default_factory=list)
    key_logic: str
    confidence: float = Field(ge=0.0, le=1.0)
    raw_analysis: str


@dataclass
class RankedSector:
    """A sector with its ranking information."""
    sector_code: str
    sector_name: str
    intensity: int
    logic: str
    rank: int


@dataclass
class ImpactReport:
    """
    Complete impact analysis report.
    
    This is the main output of the analysis pipeline.
    
    Attributes:
        news_text: Original news text
        news_analysis: News analysis result
        sector_analyses: Analysis for each sector
        bullish_top5: Top 5 positively impacted sectors
        bearish_top5: Top 5 negatively impacted sectors
        recommendations: Investment recommendations
        risks: Risk warnings
        signals_to_watch: Signals to monitor
        metadata: Additional metadata
    """
    news_text: str
    news_analysis: NewsAnalysis
    sector_analyses: dict[str, SectorAnalysis]
    bullish_top5: list[RankedSector]
    bearish_top5: list[RankedSector]
    recommendations: dict[str, str]  # time_horizon -> recommendation
    risks: list[str]
    signals_to_watch: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate report structure."""
        if len(self.bullish_top5) > 5:
            raise ValueError("bullish_top5 cannot exceed 5 items")
        if len(self.bearish_top5) > 5:
            raise ValueError("bearish_top5 cannot exceed 5 items")
    
    @property
    def timestamp(self) -> datetime:
        """Get report generation timestamp."""
        return self.metadata.get("timestamp", datetime.now())
    
    @property
    def language(self) -> str:
        """Get report language."""
        return self.metadata.get("language", "zh")


class AnalysisRequest(BaseModel):
    """
    Request model for news impact analysis.
    
    Attributes:
        news_text: News content to analyze
        language: Output language preference
        include_raw: Whether to include raw LLM outputs
        sector_filter: Optional list of sectors to analyze (None = all)
    """
    news_text: str = Field(..., min_length=10, max_length=10000)
    language: str = Field(default="zh", pattern="^(zh|en)$")
    include_raw: bool = Field(default=True)
    sector_filter: list[str] | None = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "news_text": "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元",
                "language": "zh",
                "include_raw": True,
                "sector_filter": None,
            }
        }


class AnalysisResponse(BaseModel):
    """
    Response model for news impact analysis.
    
    Attributes:
        success: Whether analysis succeeded
        report: Analysis report (if successful)
        error: Error message (if failed)
        processing_time_ms: Processing time in milliseconds
    """
    success: bool
    report: ImpactReport | None = None
    error: str | None = None
    processing_time_ms: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "report": None,  # Would contain full report
                "error": None,
                "processing_time_ms": 5432,
            }
        }
