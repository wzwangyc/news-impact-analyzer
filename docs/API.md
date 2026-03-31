# API Documentation

## Core Classes

### NewsImpactAnalyzer

Main analyzer for news impact analysis.

```python
from news_impact import NewsImpactAnalyzer

# Initialize
analyzer = NewsImpactAnalyzer(language="zh")

# Analyze news
result = analyzer.analyze("央行宣布降准 0.5 个百分点")
```

#### Methods

##### `analyze(news_text: str) -> dict`

Analyze news impact on A-share sectors.

**Parameters:**
- `news_text` (str): News content (10-10,000 characters)

**Returns:**
```python
{
    "news_analysis": NewsAnalysis,
    "sector_analyses": dict[str, SectorAnalysis],
    "bullish_top5": list[RankedSector],
    "bearish_top5": list[RankedSector],
    "recommendations": dict,
    "risks": list[str],
    "signals_to_watch": list[str],
    "metadata": dict,
}
```

**Raises:**
- `TypeError`: If news_text is not a string
- `ValueError`: If news_text is invalid
- `LLMClientError`: If LLM API fails

##### `analyze_async(news_text: str) -> asyncio.Task`

Async version of analyze.

**Example:**
```python
import asyncio

async def main():
    analyzer = NewsImpactAnalyzer()
    result = await analyzer.analyze_async("新闻内容")
```

### NewsAnalysis

News analysis result.

**Attributes:**
- `event_type` (str): Type of event
- `related_sectors` (list[str]): Related sectors
- `overall_direction` (ImpactDirection): Impact direction
- `overall_intensity` (ImpactIntensity): Impact intensity
- `key_facts` (list[str]): Key facts
- `uncertainties` (list[str]): Uncertainties

### SectorAnalysis

Sector-level analysis.

**Attributes:**
- `sector_code` (str): Sector code
- `sector_name` (str): Sector name
- `direction` (ImpactDirection): Impact direction
- `intensity` (ImpactIntensity): Impact intensity (1-5)
- `time_horizon` (TimeHorizon): Time horizon
- `direct_impact` (str): Direct impact
- `indirect_impact` (str): Indirect impact
- `affected_subsectors` (list[str]): Affected subsectors
- `key_logic` (str): Key logic
- `confidence` (float): Confidence (0-1)

### Enums

#### ImpactDirection

```python
ImpactDirection.POSITIVE   # 利好
ImpactDirection.NEGATIVE   # 利空
ImpactDirection.NEUTRAL    # 中性
```

#### ImpactIntensity

```python
ImpactIntensity.VERY_LOW   # 1
ImpactIntensity.LOW        # 2
ImpactIntensity.MEDIUM     # 3
ImpactIntensity.HIGH       # 4
ImpactIntensity.VERY_HIGH  # 5
```

#### TimeHorizon

```python
TimeHorizon.SHORT_TERM  # 短期 (<1 月)
TimeHorizon.MID_TERM    # 中期 (1-3 月)
TimeHorizon.LONG_TERM   # 长期 (>3 月)
```

## Configuration

### Settings

Load configuration from environment variables.

```python
from news_impact.config import Settings

settings = Settings()
```

**Environment Variables:**
- `DASHSCOPE_API_KEY`: API key (required)
- `LLM_BASE_URL`: API base URL (default: https://dashscope.aliyuncs.com/compatible-mode/v1)
- `LLM_MODEL_NAME`: Model name (default: qwen-plus)
- `LANGUAGE`: Output language (default: zh)
- `LOG_LEVEL`: Logging level (default: INFO)

## Error Handling

### LLMClientError

Base exception for LLM errors.

### LLMRateLimitError

API rate limit exceeded.

**Solution:** Wait and retry.

### LLMTimeoutError

Request timed out.

**Solution:** Increase timeout or reduce prompt length.

### ConfigurationError

Invalid configuration.

**Solution:** Check environment variables.

## Examples

### Basic Analysis

```python
from news_impact import NewsImpactAnalyzer

analyzer = NewsImpactAnalyzer()
result = analyzer.analyze("央行宣布降准")

print(f"Bullish: {len(result['bullish_top5'])} sectors")
print(f"Bearish: {len(result['bearish_top5'])} sectors")
```

### Batch Analysis

```python
import asyncio
from news_impact import NewsImpactAnalyzer

async def batch_analyze(news_list):
    analyzer = NewsImpactAnalyzer()
    tasks = [analyzer.analyze_async(news) for news in news_list]
    return await asyncio.gather(*tasks)

results = asyncio.run(batch_analyze(["新闻 1", "新闻 2"]))
```

### Error Handling

```python
from news_impact import NewsImpactAnalyzer
from news_impact.llm_client import LLMClientError

analyzer = NewsImpactAnalyzer()

try:
    result = analyzer.analyze("新闻内容")
except LLMClientError as e:
    print(f"Analysis failed: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
```

---

**Last Updated**: 2026-03-31
**Version**: 0.5.0
