#!/usr/bin/env python3
"""
Command-line interface for News Impact Analyzer.

Usage:
    news-impact "新闻内容" [--language zh|en] [--output json|text]

Examples:
    news-impact "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"
    news-impact "央行宣布降准" --language en --output json
"""

import argparse
import json
import sys
from datetime import datetime

import structlog
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from .analyzer import NewsImpactAnalyzer
from .config import ConfigurationError
from .llm_client import LLMClientError
from .llm_client import LLMRateLimitError
from .llm_client import LLMTimeoutError

# Configure logging
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger("INFO"),
)

console = Console()


def _validate_news_argument(news: str) -> None:
    """
    Validate news command-line argument.

    Fail Fast: Reject invalid arguments before any processing.

    Args:
        news: News text from command line

    Raises:
        ValueError: If news is invalid
    """
    if not news:
        raise ValueError("News text cannot be empty")

    if not news.strip():
        raise ValueError("News text cannot be only whitespace")

    length = len(news.strip())

    if length < 10:
        raise ValueError(
            f"News text too short ({length} chars). Minimum 10 characters."
        )

    if length > 10_000:
        raise ValueError(
            f"News text too long ({length} chars). Maximum 10,000 characters."
        )


def create_sector_table(
    sectors: list,
    title: str,
    color: str,
) -> Table:
    """
    Create a rich table for sector rankings.

    Args:
        sectors: List of RankedSector objects
        title: Table title
        color: Color for table border

    Returns:
        Rich Table object
    """
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        border_style=color,
    )

    table.add_column("Rank", style="dim", width=5)
    table.add_column("Sector", style=color)
    table.add_column("Intensity", justify="right")
    table.add_column("Logic", width=60)

    for sector in sectors:
        # Truncate logic if too long
        logic = sector.logic
        if len(logic) > 55:
            logic = logic[:52] + "..."

        table.add_row(
            str(sector.rank),
            sector.sector_name,
            "⭐" * sector.intensity,
            logic,
        )

    return table


def print_text_report(result: dict, language: str = "zh") -> None:
    """
    Print analysis report in text format.

    Args:
        result: Analysis result dictionary
        language: Output language
    """
    # Header
    console.print()
    console.print(
        Panel(
            "[bold blue]📰 News Impact Analysis Report[/bold blue]\n"
            f"[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            border_style="blue",
        )
    )

    # News
    console.print("\n[bold]📝 News:[/bold]")
    console.print(f"  {result['news_analysis'].news_text[:200]}...")

    # Bullish sectors
    if result["bullish_top5"]:
        console.print()
        console.print(
            create_sector_table(
                result["bullish_top5"],
                "📈 Top 5 Beneficiaries (利好)",
                "green",
            )
        )

    # Bearish sectors
    if result["bearish_top5"]:
        console.print()
        console.print(
            create_sector_table(
                result["bearish_top5"],
                "📉 Top 5 Negatively Impacted (利空)",
                "red",
            )
        )

    # Full summary
    if "full_summary" in result:
        console.print("\n[bold]📋 Full Report:[/bold]")
        console.print(Markdown(result["full_summary"]))

    # Metadata
    meta = result.get("metadata", {})
    console.print()
    console.print(
        Panel(
            f"[dim]Model: {meta.get('model', 'N/A')}[/dim]\n"
            f"[dim]Processing Time: {meta.get('processing_time_ms', 0)}ms[/dim]\n"
            f"[dim]Language: {meta.get('language', 'N/A')}[/dim]",
            border_style="dim",
        )
    )


def print_json_report(result: dict) -> None:
    """
    Print analysis report in JSON format.

    Args:
        result: Analysis result dictionary
    """
    # Convert to serializable format
    output = {
        "news_analysis": result["news_analysis"].model_dump(),
        "sector_analyses": {
            k: v.model_dump() for k, v in result["sector_analyses"].items()
        },
        "bullish_top5": [
            {
                "rank": s.rank,
                "sector_code": s.sector_code,
                "sector_name": s.sector_name,
                "intensity": s.intensity,
                "logic": s.logic,
            }
            for s in result["bullish_top5"]
        ],
        "bearish_top5": [
            {
                "rank": s.rank,
                "sector_code": s.sector_code,
                "sector_name": s.sector_name,
                "intensity": s.intensity,
                "logic": s.logic,
            }
            for s in result["bearish_top5"]
        ],
        "recommendations": result["recommendations"],
        "risks": result["risks"],
        "signals_to_watch": result["signals_to_watch"],
        "metadata": result["metadata"],
    }

    console.print_json(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> int:
    """
    Main entry point for CLI with Fail Fast validation.

    Fail Fast Principles:
    - Validate configuration at startup
    - Validate command-line arguments immediately
    - Fail on first error, don't continue
    - Clear error messages with actionable guidance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Analyze news impact on A-share market sectors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  news-impact "央行宣布降准 0.5 个百分点"
  news-impact "央行降准" --language en --output json
  news-impact "地产新政" --output text
        """,
    )

    parser.add_argument(
        "news",
        type=str,
        help="News content to analyze (10-10000 characters)",
    )

    parser.add_argument(
        "--language",
        "-l",
        type=str,
        choices=["zh", "en"],
        default="zh",
        help="Output language (default: zh)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    # Fail Fast: Validate news argument before initialization
    try:
        _validate_news_argument(args.news)
    except ValueError as e:
        console.print(f"\n[bold red]❌ Invalid Input:[/bold red] {e}")
        console.print(
            '\n[dim]Usage: news-impact "新闻内容" [--language zh|en] [--output json|text][/dim]'
        )
        return 1

    try:
        # Fail Fast: Initialize analyzer (validates configuration)
        with console.status("[bold green]Initializing analyzer..."):
            analyzer = NewsImpactAnalyzer(language=args.language)

        # Run analysis
        with console.status("[bold green]Analyzing news impact..."):
            result = analyzer.analyze(args.news)

        # Add news text to result for display
        result["news_analysis"].news_text = args.news

        # Output results
        if args.output == "json":
            print_json_report(result)
        else:
            print_text_report(result, args.language)

        return 0

    except ConfigurationError as e:
        # Fail Fast: Configuration errors are critical, provide clear guidance
        console.print(f"\n[bold red]❌ Configuration Error:[/bold red] {e}")
        console.print(
            "\n[yellow]To fix:[/yellow]\n"
            "1. Copy .env.example to .env: [dim]cp .env.example .env[/dim]\n"
            "2. Edit .env and set DASHSCOPE_API_KEY\n"
            "3. Get API key from: https://bailian.console.aliyun.com/"
        )
        return 1

    except LLMRateLimitError as e:
        # Fail Fast: Rate limit - don't retry automatically
        console.print(f"\n[bold red]❌ Rate Limit Error:[/bold red] {e}")
        console.print(
            "\n[yellow]To fix:[/yellow] Wait 1 minute and retry, or reduce request frequency"
        )
        return 1

    except LLMTimeoutError as e:
        # Fail Fast: Timeout - provide actionable guidance
        console.print(f"\n[bold red]❌ Timeout Error:[/bold red] {e}")
        console.print(
            "\n[yellow]To fix:[/yellow]\n"
            "1. Check network connection\n"
            "2. Reduce news text length\n"
            "3. Increase REQUEST_TIMEOUT in .env"
        )
        return 1

    except LLMClientError as e:
        # Fail Fast: Other API errors
        console.print(f"\n[bold red]❌ API Error:[/bold red] {e}")
        console.print("\n[yellow]To fix:[/yellow] Check API key and network connection")
        return 1

    except Exception as e:
        # Fail Fast: Unexpected errors - provide full details in verbose mode
        console.print(f"\n[bold red]❌ Unexpected Error:[/bold red] {type(e).__name__}")
        console.print(f"[dim]Details: {e}[/dim]")

        if args.verbose:
            console.print("\n[bold]Stack Trace:[/bold]")
            import traceback

            traceback.print_exc()
        else:
            console.print("\n[dim]Run with --verbose for full stack trace[/dim]")

        return 1


if __name__ == "__main__":
    sys.exit(main())
