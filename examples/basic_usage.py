#!/usr/bin/env python3
"""
Example usage of News Impact Analyzer

This script demonstrates how to use the analyzer programmatically.
"""

from news_impact import NewsImpactAnalyzer


def main() -> None:
    """Run example analysis."""
    # Sample news items
    news_samples = [
        {
            "zh": "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元",
            "en": "Central bank announces 0.5% RRR cut, releasing 1 trillion yuan in long-term funds",
        },
        {
            "zh": "工信部：加快新能源汽车充电桩建设，目标 2025 年建成 2000 万个",
            "en": "Ministry of Industry: Accelerate EV charging infrastructure, target 20M chargers by 2025",
        },
        {
            "zh": "某大型地产公司债务违约，涉及金额 50 亿元",
            "en": "Major real estate company defaults on debt, involving 5 billion yuan",
        },
    ]
    
    # Initialize analyzers
    analyzer_zh = NewsImpactAnalyzer(language="zh")
    analyzer_en = NewsImpactAnalyzer(language="en")
    
    # Analyze each news item
    for i, news in enumerate(news_samples, 1):
        print(f"\n{'='*60}")
        print(f"Example {i}")
        print(f"{'='*60}\n")
        
        # Chinese analysis
        print("🇨🇳 Chinese Analysis:")
        print("-" * 40)
        result_zh = analyzer_zh.analyze(news["zh"])
        
        print(f"\n📈 利好 Top 3:")
        for sector in result_zh["bullish_top5"][:3]:
            print(f"  {sector.rank}. {sector.sector_name} (强度：{'⭐' * sector.intensity})")
            print(f"     逻辑：{sector.logic}")
        
        print(f"\n📉 利空 Top 3:")
        for sector in result_zh["bearish_top5"][:3]:
            print(f"  {sector.rank}. {sector.sector_name} (强度：{'⭐' * sector.intensity})")
            print(f"     逻辑：{sector.logic}")
        
        # English analysis
        print("\n🇬🇧 English Analysis:")
        print("-" * 40)
        result_en = analyzer_en.analyze(news["en"])
        
        print(f"\n📈 Top 3 Beneficiaries:")
        for sector in result_en["bullish_top5"][:3]:
            print(f"  {sector.rank}. {sector.sector_name} (Intensity: {'⭐' * sector.intensity})")
            print(f"     Logic: {sector.logic}")
        
        print(f"\n📉 Top 3 Negatively Impacted:")
        for sector in result_en["bearish_top5"][:3]:
            print(f"  {sector.rank}. {sector.sector_name} (Intensity: {'⭐' * sector.intensity})")
            print(f"     Logic: {sector.logic}")
        
        print("\n")


if __name__ == "__main__":
    main()
