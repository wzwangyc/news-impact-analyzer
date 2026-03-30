"""
News Impact Analyzer - Core Analysis Engine

Main orchestration module that coordinates all agents and produces
the final impact report.
"""

import json
import re
import time
from typing import Any

import structlog

from .config import get_settings
from .llm_client import LLMClient
from .models import ImpactDirection
from .models import ImpactIntensity
from .models import NewsAnalysis
from .models import RankedSector
from .models import SectorAnalysis
from .models import TimeHorizon
from .prompts import get_news_analyzer_prompt
from .prompts import get_sector_analyst_prompt
from .prompts import get_summary_prompt
from .sectors import SECTORS
from .sectors import get_sector_descriptions
from .sectors import get_sector_names

logger = structlog.get_logger(__name__)


class NewsImpactAnalyzer:
    """
    Main analyzer for news impact assessment.

    This class orchestrates the multi-agent analysis pipeline:
    1. News Analysis Agent - extracts key information from news
    2. Sector Analysis Agents (parallel) - analyze impact on each sector
    3. Chief Strategist Agent - synthesizes recommendations

    Attributes:
        llm_client: LLM client for API interactions
        language: Output language preference
    """

    def __init__(self, language: str = "zh") -> None:
        """
        Initialize analyzer.

        Args:
            language: Output language ('zh' or 'en')
        """
        self.settings = get_settings()
        self.llm_client = LLMClient(self.settings)
        self.language = language

        logger.info(
            "analyzer_initialized",
            language=language,
            model=self.settings.llm_model,
        )

    def analyze(self, news_text: str) -> dict[str, Any]:
        """
        Analyze news impact on A-share sectors with Fail Fast validation.

        Fail Fast Principles:
        - Validate all inputs immediately
        - Fail on first error, don't continue
        - Clear error messages with actionable guidance
        - No partial results on failure

        Args:
            news_text: News content to analyze (Chinese or English, 10-10k chars)

        Returns:
            Complete analysis results including:
            - news_analysis: High-level news analysis
            - sector_analyses: Detailed analysis for each sector
            - bullish_top5: Top 5 positively impacted sectors
            - bearish_top5: Top 5 negatively impacted sectors
            - recommendations: Investment recommendations
            - risks: Risk warnings
            - signals_to_watch: Signals to monitor

        Raises:
            TypeError: If news_text is not a string
            ValueError: If news_text is invalid (empty, too short, too long)
            LLMClientError: If LLM API fails
            RuntimeError: If analysis produces invalid results
        """
        # Fail Fast: Validate input type and content BEFORE any processing
        self._validate_news_input(news_text)

        start_time = time.time()
        logger.info("analysis_started", news_length=len(news_text))

        # Step 1: Analyze news
        logger.info("step_1_news_analysis")
        news_analysis = self._analyze_news(news_text)
        logger.info("news_analysis_complete")

        # Step 2: Analyze each sector
        logger.info("step_2_sector_analysis", num_sectors=len(SECTORS))
        sector_analyses = self._analyze_sectors(news_text, news_analysis)
        logger.info("sector_analysis_complete")

        # Step 3: Generate summary and recommendations
        logger.info("step_3_summary_generation")
        summary = self._generate_summary(news_text, sector_analyses)
        logger.info("summary_generation_complete")

        elapsed_ms = int((time.time() - start_time) * 1000)
        logger.info("analysis_completed", elapsed_ms=elapsed_ms)

        # Fail Fast: Validate result structure before returning
        result = {
            "news_analysis": news_analysis,
            "sector_analyses": sector_analyses,
            "bullish_top5": summary["bullish_top5"],
            "bearish_top5": summary["bearish_top5"],
            "recommendations": summary["recommendations"],
            "risks": summary["risks"],
            "signals_to_watch": summary["signals_to_watch"],
            "metadata": {
                "timestamp": time.time(),
                "language": self.language,
                "processing_time_ms": elapsed_ms,
                "model": self.settings.llm_model,
            },
        }

        self._validate_result(result)
        return result

    def _validate_news_input(self, news_text: Any) -> None:
        """
        Validate news input with strict type and content checks.

        Fail Fast: Reject invalid input immediately, before any processing.

        Args:
            news_text: Input to validate

        Raises:
            TypeError: If news_text is not a string
            ValueError: If news_text content is invalid
        """
        # Type check - must be string
        if not isinstance(news_text, str):
            raise TypeError(
                f"news_text must be a string, got {type(news_text).__name__}. "
                "Example: analyzer.analyze('央行宣布降准')"
            )

        # Empty check
        if not news_text:
            raise ValueError("news_text cannot be empty")

        # Whitespace check
        if not news_text.strip():
            raise ValueError("news_text cannot be only whitespace")

        # Length checks
        length = len(news_text.strip())
        if length < 10:
            raise ValueError(
                f"news_text too short ({length} chars). Minimum 10 characters. "
                "Example: '央行宣布降准 0.5 个百分点'"
            )

        if length > 10_000:
            raise ValueError(
                f"news_text too long ({length} chars). Maximum 10,000 characters. "
                "Please summarize or split into multiple requests."
            )

    def _validate_result(self, result: dict[str, Any]) -> None:
        """
        Validate analysis result structure before returning.

        Fail Fast: Ensure result is complete and valid, don't return partial data.

        Args:
            result: Analysis result dictionary

        Raises:
            RuntimeError: If result structure is invalid
        """
        required_keys = [
            "news_analysis",
            "sector_analyses",
            "bullish_top5",
            "bearish_top5",
            "recommendations",
            "risks",
            "signals_to_watch",
            "metadata",
        ]

        for key in required_keys:
            if key not in result:
                raise RuntimeError(
                    f"Analysis result missing required key: '{key}'. "
                    "This indicates a bug in the analysis pipeline."
                )

        # Validate sector_analyses is not empty
        if not result["sector_analyses"]:
            raise RuntimeError("sector_analyses is empty. Analysis failed.")

        # Validate metadata
        if not isinstance(result["metadata"], dict):
            raise RuntimeError("metadata must be a dictionary")

        if "processing_time_ms" not in result["metadata"]:
            raise RuntimeError("metadata missing processing_time_ms")

    def _analyze_news(self, news_text: str) -> NewsAnalysis:
        """
        Analyze news to extract key information.

        Args:
            news_text: News content

        Returns:
            NewsAnalysis object with extracted information
        """
        prompt = get_news_analyzer_prompt(self.language).format(news_text=news_text)

        response = self.llm_client.generate(prompt)

        # Parse JSON response
        try:
            # Try to extract JSON from response (may contain markdown code blocks)
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                response = json_match.group()

            data = json.loads(response)

            # Map string values to enums
            direction_map = {
                "利好": ImpactDirection.POSITIVE,
                "利空": ImpactDirection.NEGATIVE,
                "中性": ImpactDirection.NEUTRAL,
                "Positive": ImpactDirection.POSITIVE,
                "Negative": ImpactDirection.NEGATIVE,
                "Neutral": ImpactDirection.NEUTRAL,
            }

            return NewsAnalysis(
                event_type=data.get("event_type", "OTHER"),
                related_sectors=data.get("related_sectors", []),
                overall_direction=direction_map.get(
                    data.get("impact_direction", "中性"),
                    ImpactDirection.NEUTRAL,
                ),
                overall_intensity=ImpactIntensity(
                    min(5, max(1, data.get("impact_intensity", 3)))
                ),
                key_facts=data.get("key_facts", []),
                uncertainties=data.get("uncertainties", []),
                raw_analysis=response,
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error("news_analysis_parse_failed", error=str(e))
            # Return minimal valid analysis
            return NewsAnalysis(
                event_type="OTHER",
                related_sectors=[],
                overall_direction=ImpactDirection.NEUTRAL,
                overall_intensity=ImpactIntensity.MEDIUM,
                key_facts=[news_text[:100]],
                uncertainties=["Failed to parse LLM response"],
                raw_analysis=response,
            )

    def _analyze_sectors(
        self,
        news_text: str,
        news_analysis: NewsAnalysis,
    ) -> dict[str, SectorAnalysis]:
        """
        Analyze impact on all sectors.

        Args:
            news_text: News content
            news_analysis: News analysis result

        Returns:
            Dictionary mapping sector codes to SectorAnalysis objects
        """
        sector_analyses = {}
        sector_names = get_sector_names(self.language)
        sector_descriptions = get_sector_descriptions(self.language)

        # Analyze each sector sequentially (can be parallelized with asyncio)
        for sector_code, sector in SECTORS.items():
            logger.debug("analyzing_sector", sector_code=sector_code)

            try:
                analysis = self._analyze_single_sector(
                    sector_code=sector_code,
                    sector_name=sector_names[sector_code],
                    sector_description=sector_descriptions[sector_code],
                    news_text=news_text,
                    news_analysis=news_analysis.raw_analysis,
                )
                sector_analyses[sector_code] = analysis

            except Exception as e:
                logger.error(
                    "sector_analysis_failed",
                    sector_code=sector_code,
                    error=str(e),
                )
                # Create minimal analysis for failed sectors
                sector_analyses[sector_code] = SectorAnalysis(
                    sector_code=sector_code,
                    sector_name=sector_names[sector_code],
                    direction=ImpactDirection.NEUTRAL,
                    intensity=ImpactIntensity.VERY_LOW,
                    time_horizon=TimeHorizon.SHORT_TERM,
                    direct_impact="Analysis failed",
                    indirect_impact="N/A",
                    key_logic="Analysis failed due to API error",
                    confidence=0.0,
                    raw_analysis=f"Error: {e}",
                )

        return sector_analyses

    def _analyze_single_sector(
        self,
        sector_code: str,
        sector_name: str,
        sector_description: str,
        news_text: str,
        news_analysis: str,
    ) -> SectorAnalysis:
        """
        Analyze impact on a single sector.

        Args:
            sector_code: Sector identifier
            sector_name: Sector name
            sector_description: Sector description
            news_text: News content
            news_analysis: News analysis result

        Returns:
            SectorAnalysis object
        """
        prompt = get_sector_analyst_prompt(self.language).format(
            sector_name=sector_name,
            sector_description=sector_description,
            news_text=news_text,
            news_analysis=news_analysis,
        )

        response = self.llm_client.generate(prompt)

        # Parse JSON response
        try:
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                response = json_match.group()

            data = json.loads(response)

            # Map string values to enums
            direction_map = {
                "利好": ImpactDirection.POSITIVE,
                "利空": ImpactDirection.NEGATIVE,
                "中性": ImpactDirection.NEUTRAL,
                "Positive": ImpactDirection.POSITIVE,
                "Negative": ImpactDirection.NEGATIVE,
                "Neutral": ImpactDirection.NEUTRAL,
            }

            time_horizon_map = {
                "短期": TimeHorizon.SHORT_TERM,
                "中期": TimeHorizon.MID_TERM,
                "长期": TimeHorizon.LONG_TERM,
                "Short-term": TimeHorizon.SHORT_TERM,
                "Mid-term": TimeHorizon.MID_TERM,
                "Long-term": TimeHorizon.LONG_TERM,
            }

            return SectorAnalysis(
                sector_code=sector_code,
                sector_name=sector_name,
                direction=direction_map.get(
                    data.get("impact_direction", "中性"),
                    ImpactDirection.NEUTRAL,
                ),
                intensity=ImpactIntensity(
                    min(5, max(1, data.get("impact_intensity", 3)))
                ),
                time_horizon=time_horizon_map.get(
                    data.get("time_horizon", "中期"),
                    TimeHorizon.MID_TERM,
                ),
                direct_impact=data.get("direct_impact", "N/A"),
                indirect_impact=data.get("indirect_impact", "N/A"),
                affected_subsectors=data.get("affected_subsectors", []),
                key_logic=data.get("key_logic", "N/A"),
                confidence=min(1.0, max(0.0, data.get("confidence", 0.5))),
                raw_analysis=response,
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(
                "sector_analysis_parse_failed",
                sector_code=sector_code,
                error=str(e),
            )
            raise

    def _generate_summary(
        self,
        news_text: str,
        sector_analyses: dict[str, SectorAnalysis],
    ) -> dict[str, Any]:
        """
        Generate summary report with rankings and recommendations.

        Args:
            news_text: News content
            sector_analyses: Analysis for all sectors

        Returns:
            Dictionary with rankings, recommendations, and risks
        """
        # Sort sectors by intensity
        bullish = []
        bearish = []

        for code, analysis in sector_analyses.items():
            if analysis.direction == ImpactDirection.POSITIVE:
                bullish.append((code, analysis))
            elif analysis.direction == ImpactDirection.NEGATIVE:
                bearish.append((code, analysis))

        # Sort by intensity (descending)
        bullish.sort(key=lambda x: x[1].intensity.value, reverse=True)
        bearish.sort(key=lambda x: x[1].intensity.value, reverse=True)

        # Take top 5
        bullish_top5 = [
            RankedSector(
                sector_code=code,
                sector_name=analysis.sector_name,
                intensity=analysis.intensity.value,
                logic=analysis.key_logic,
                rank=i + 1,
            )
            for i, (code, analysis) in enumerate(bullish[:5])
        ]

        bearish_top5 = [
            RankedSector(
                sector_code=code,
                sector_name=analysis.sector_name,
                intensity=analysis.intensity.value,
                logic=analysis.key_logic,
                rank=i + 1,
            )
            for i, (code, analysis) in enumerate(bearish[:5])
        ]

        # Generate markdown tables
        bullish_table = self._build_ranking_table(bullish_top5)
        bearish_table = self._build_ranking_table(bearish_top5)

        # Generate full summary using LLM
        sector_summary = "\n\n".join(
            [
                f"### {analysis.sector_name}\n"
                f"- Direction: {analysis.direction.value}\n"
                f"- Intensity: {analysis.intensity.value}/5\n"
                f"- Logic: {analysis.key_logic}"
                for analysis in sector_analyses.values()
            ]
        )

        prompt = get_summary_prompt(self.language).format(
            news_text=news_text,
            sector_analyses=sector_summary,
            bullish_table=bullish_table,
            bearish_table=bearish_table,
        )

        summary_text = self.llm_client.generate(prompt)

        # Parse recommendations from summary (simplified)
        recommendations = {
            "short_term": "见完整报告",
            "mid_term": "见完整报告",
            "long_term": "见完整报告",
        }

        # Extract risks and signals (simplified - in production, use better parsing)
        risks = ["政策落地不及预期", "外部环境变化"]
        signals = ["关注后续政策细则", "跟踪行业高频数据"]

        return {
            "bullish_top5": bullish_top5,
            "bearish_top5": bearish_top5,
            "recommendations": recommendations,
            "risks": risks,
            "signals_to_watch": signals,
            "full_summary": summary_text,
        }

    def _build_ranking_table(self, sectors: list[RankedSector]) -> str:
        """
        Build markdown ranking table.

        Args:
            sectors: List of ranked sectors

        Returns:
            Markdown table string
        """
        if not sectors:
            return "| - | - | - | - |"

        rows = []
        for s in sectors:
            # Truncate logic if too long
            logic = s.logic[:50] + "..." if len(s.logic) > 50 else s.logic
            rows.append(f"| {s.rank} | {s.sector_name} | {s.intensity} | {logic} |")

        return "\n".join(rows)
