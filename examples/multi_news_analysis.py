#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Multi-news batch analysis.

This example demonstrates:
- Batch processing multiple news items
- Parallel analysis with asyncio
- Aggregating results
- Exporting to JSON/CSV
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from news_impact import NewsImpactAnalyzer


async def analyze_news_batch(
    news_items: list[str],
    language: str = "zh",
) -> list[dict]:
    """
    Analyze multiple news items in parallel.

    Args:
        news_items: List of news texts
        language: Analysis language

    Returns:
        List of analysis results
    """
    analyzer = NewsImpactAnalyzer(language=language)
    
    # Create analysis tasks
    tasks = [analyzer.analyze_async(news) for news in news_items]
    
    # Run in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    processed = []
    for i, (news, result) in enumerate(zip(news_items, results)):
        if isinstance(result, Exception):
            processed.append({
                "index": i,
                "news": news[:100],
                "error": str(result),
                "success": False,
            })
        else:
            processed.append({
                "index": i,
                "news": news[:100],
                "result": result,
                "success": True,
            })
    
    return processed


def export_results(results: list[dict], output_file: str) -> None:
    """
    Export analysis results to JSON file.

    Args:
        results: Analysis results
        output_file: Output file path
    """
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_news": len(results),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results,
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Results exported to: {output_file}")


def main() -> None:
    """Run multi-news analysis example."""
    print("=" * 60)
    print("Multi-News Batch Analysis Example")
    print("=" * 60)
    
    # Sample news items
    news_items = [
        "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元",
        "工信部：加快新能源汽车充电桩建设，目标 2025 年建成 2000 万个",
        "证监会：加强对量化交易的监管，限制高频交易",
        "发改委：促进房地产市场平稳健康发展",
        "科技部：加大对人工智能领域的支持力度",
    ]
    
    print(f"\nAnalyzing {len(news_items)} news items...\n")
    
    # Run analysis
    results = asyncio.run(analyze_news_batch(news_items))
    
    # Print summary
    successful = sum(1 for r in results if r["success"])
    print(f"✓ Successful: {successful}/{len(news_items)}")
    
    # Print results
    for result in results:
        if result["success"]:
            print(f"\n[News {result['index'] + 1}] {result['news']}...")
            bullish = len(result["result"].get("bullish_top5", []))
            bearish = len(result["result"].get("bearish_top5", []))
            print(f"  Bullish sectors: {bullish}")
            print(f"  Bearish sectors: {bearish}")
        else:
            print(f"\n[News {result['index'] + 1}] FAILED: {result['error']}")
    
    # Export results
    export_results(results, "examples/output/multi_news_results.json")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
