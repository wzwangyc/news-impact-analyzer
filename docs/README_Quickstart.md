# Quick Start Guide

Get started with News Impact Analyzer in 5 minutes.

## Installation

### Option 1: From PyPI (after release)

```bash
pip install news-impact-analyzer
```

### Option 2: From Source

```bash
# Clone repository
git clone https://github.com/wzwangyc/news-impact-analyzer.git
cd news-impact-analyzer

# Install dependencies
pip install -e ".[dev]"
```

## Configuration

### 1. Get API Key

Visit: https://bailian.console.aliyun.com/

Get your DashScope API key.

### 2. Set Environment Variable

**Linux/macOS:**
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

**Windows:**
```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

**Or create `.env` file:**
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### CLI (Command Line)

```bash
# Basic usage
news-impact "央行宣布降准 0.5 个百分点"

# English output
news-impact "央行降准" --language en

# JSON output
news-impact "新能源汽车政策" --output json
```

### Python API

```python
from news_impact import NewsImpactAnalyzer

# Initialize
analyzer = NewsImpactAnalyzer(language="zh")

# Analyze news
result = analyzer.analyze("央行宣布降准 0.5 个百分点")

# View results
print("Bullish Sectors:")
for sector in result["bullish_top5"]:
    print(f"  {sector.sector_name}: {sector.logic}")
```

### Async API

```python
import asyncio
from news_impact import NewsImpactAnalyzer

async def main():
    analyzer = NewsImpactAnalyzer()
    result = await analyzer.analyze_async("新闻内容")
    print(result)

asyncio.run(main())
```

## Examples

### Example 1: Single News Analysis

```python
from news_impact import NewsImpactAnalyzer

analyzer = NewsImpactAnalyzer()
result = analyzer.analyze("央行宣布降准")

print(f"Mean return: {result['recommendations']['short_term']}")
```

### Example 2: Batch Analysis

```python
import asyncio
from news_impact import NewsImpactAnalyzer

async def batch_analyze():
    analyzer = NewsImpactAnalyzer()
    
    news_list = [
        "央行降准",
        "新能源汽车政策",
        "AI 监管新规",
    ]
    
    tasks = [analyzer.analyze_async(news) for news in news_list]
    results = await asyncio.gather(*tasks)
    
    for news, result in zip(news_list, results):
        print(f"\n{news}:")
        print(f"  Bullish: {len(result['bullish_top5'])} sectors")

asyncio.run(batch_analyze())
```

### Example 3: Export Results

```python
import json
from news_impact import NewsImpactAnalyzer

analyzer = NewsImpactAnalyzer()
result = analyzer.analyze("央行降准")

# Save to JSON
with open("result.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/news_impact --cov-report=html

# Run specific test
pytest tests/test_models.py -v
```

## Troubleshooting

### "API key not configured"

**Solution:**
```bash
export DASHSCOPE_API_KEY="your_key"
```

### "Request timed out"

**Solution:**
1. Check network connection
2. Increase timeout in `.env`:
   ```
   REQUEST_TIMEOUT=120
   ```

### "News text too short"

**Solution:**
- Minimum 10 characters required
- Example: `"央行降准"` (4 chars) ❌
- Example: `"央行宣布降准 0.5 个百分点"` (11 chars) ✅

## Next Steps

- [API Documentation](API.md) - Full API reference
- [Examples](../examples/) - More examples
- [Contributing](../CONTRIBUTING.md) - How to contribute

---

**Need Help?**

- GitHub Issues: https://github.com/wzwangyc/news-impact-analyzer/issues
- Email: wangreits@163.com
