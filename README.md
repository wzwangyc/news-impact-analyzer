# News Impact Analyzer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-000000.svg)](https://mypy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-powered multi-agent system for analyzing the impact of breaking news on A-share market sectors.**

> 📊 **Predict market movements before they happen**  
> 🤖 **Multi-agent simulation with 28+ industry analysts**  
> 🌐 **Bilingual support (Chinese/English)**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/wzwangyc/news-impact-analyzer.git
cd news-impact-analyzer

# Install dependencies
pip install -e ".[dev]"

# Copy environment configuration
cp .env.example .env

# Edit .env and add your API key
# Get API key from: https://bailian.console.aliyun.com/
```

### Usage

**Command Line:**

```bash
# Analyze news (Chinese)
news-impact "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"

# Analyze news (English)
news-impact "Central bank announces 0.5% RRR cut" --language en

# Output as JSON
news-impact "央行降准" --output json
```

**Python API:**

```python
from news_impact import NewsImpactAnalyzer

# Initialize analyzer
analyzer = NewsImpactAnalyzer(language="zh")

# Analyze news
result = analyzer.analyze("央行宣布降准 0.5 个百分点")

# View top beneficiaries
print("利好板块:")
for sector in result["bullish_top5"]:
    print(f"  {sector.rank}. {sector.sector_name} (强度：{sector.intensity}/5)")

# View recommendations
print("\n投资建议:")
print(f"  短期：{result['recommendations']['short_term']}")
```

---

## 📋 Features

### ✨ Core Capabilities

- **Multi-Agent Architecture**: 28+ sector analysts + news analyzer + chief strategist
- **Comprehensive Coverage**: All 28 A-share sectors (SW Level 1 classification)
- **Bilingual Support**: Chinese and English output
- **Structured Output**: JSON and human-readable report formats
- **Production Ready**: Type hints, error handling, logging, testing

### 🎯 Analysis Output

For each news item, the system provides:

1. **News Analysis**: Event type, key facts, uncertainties
2. **Sector Impact**: Direction (positive/negative/neutral), intensity (1-5), time horizon
3. **Top 5 Beneficiaries**: Sectors that benefit most
4. **Top 5 Negatively Impacted**: Sectors that suffer most
5. **Investment Recommendations**: Short/mid/long-term actionable advice
6. **Risk Warnings**: Key risks to monitor
7. **Signals to Watch**: Quantifiable indicators for tracking

---

## 🏗️ Architecture

```
┌─────────────────┐
│   News Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  News Analyzer  │  ← Extracts key information
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sector Analysts │  ← 28 parallel analyses
│  (Bank, Real    │     (one per industry)
│   Estate, etc.) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Chief Strategist│  ← Synthesizes recommendations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Report   │
└─────────────────┘
```

---

## 📦 Project Structure

```
news-impact-analyzer/
├── src/news_impact/
│   ├── __init__.py          # Package exports
│   ├── analyzer.py          # Main orchestration
│   ├── config.py            # Settings management
│   ├── llm_client.py        # LLM API client
│   ├── models.py            # Data models (pydantic)
│   ├── prompts.py           # Prompt templates
│   ├── sectors.py           # Sector definitions
│   └── cli.py               # Command-line interface
├── tests/
│   ├── test_analyzer.py
│   ├── test_models.py
│   └── test_prompts.py
├── pyproject.toml           # Project metadata
├── README.md                # This file
├── .env.example             # Environment template
└── .github/workflows/
    └── ci.yml               # CI/CD pipeline
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DASHSCOPE_API_KEY` | ✅ Yes | - | API key for Qwen model |
| `LLM_BASE_URL` | ❌ No | `https://dashscope.aliyuncs.com/compatible-mode/v1` | API endpoint |
| `LLM_MODEL_NAME` | ❌ No | `qwen-plus` | Model to use |
| `LANGUAGE` | ❌ No | `zh` | Default output language |
| `LOG_LEVEL` | ❌ No | `INFO` | Logging level |

### Model Selection

Available models (Alibaba DashScope):

- `qwen-turbo`: Fastest, cheapest, lower quality
- `qwen-plus`: **Recommended**, balanced speed/quality
- `qwen-max`: Slowest, most expensive, highest quality

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/news_impact --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v

# Type checking
mypy src/news_impact

# Code formatting
black src/news_impact tests

# Linting
ruff check src/news_impact
```

---

## 📊 Example Output

### Text Format

```
╭──────────────────────────────────────────────────────────────╮
│  📰 News Impact Analysis Report                              │
│  Generated: 2026-03-31 03:16:00                              │
╰──────────────────────────────────────────────────────────────╯

📝 News:
  央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元...

╭──────────────────────────────────────────────────────────────╮
│  📈 Top 5 Beneficiaries (利好)                               │
├──────┬──────────────┬─────────────┬──────────────────────────┤
│ Rank │ Sector       │ Intensity   │ Logic                    │
├──────┼──────────────┼─────────────┼──────────────────────────┤
│ 1    │ 银行         │ ⭐⭐⭐⭐⭐     │ 降准释放流动性，降低负债成本 │
│ 2    │ 证券         │ ⭐⭐⭐⭐      │ 市场流动性改善，交易量提升 │
│ 3    │ 房地产       │ ⭐⭐⭐⭐      │ 融资环境改善，缓解债务压力 │
│ 4    │ 建材         │ ⭐⭐⭐       │ 地产链受益，需求预期改善   │
│ 5    │ 钢铁         │ ⭐⭐⭐       │ 下游需求预期好转           │
╰──────┴──────────────┴─────────────┴──────────────────────────╯

📋 Full Report:
## 🎯 投资建议
- 短期（1 周）：关注券商、银行板块的交易性机会
- 中期（1-3 月）：布局地产链估值修复
- 长期（3 月以上）：持续超配科技成长

## ⚠️ 风险提示
- 降准幅度低于预期
- 资金实际投放效果待观察
```

### JSON Format

```json
{
  "news_analysis": {
    "event_type": "MACRO",
    "overall_direction": "positive",
    "overall_intensity": 4,
    "key_facts": ["降准 0.5%", "释放 1 万亿"]
  },
  "bullish_top5": [
    {
      "rank": 1,
      "sector_code": "BANK",
      "sector_name": "银行",
      "intensity": 5,
      "logic": "降准释放流动性，降低负债成本"
    }
  ],
  "recommendations": {
    "short_term": "关注券商、银行板块的交易性机会"
  }
}
```

---

## 🎓 Use Cases

### For Investors
- **Pre-market preparation**: Analyze overnight news before market opens
- **Event-driven trading**: Quick assessment of breaking news impact
- **Portfolio adjustment**: Identify sectors to overweight/underweight

### For Researchers
- **Market efficiency studies**: Test how quickly news is priced in
- **Sentiment analysis**: Compare AI predictions with actual market reactions
- **Cross-sector spillovers**: Study inter-industry relationships

### For Financial Advisors
- **Client communication**: Generate professional reports quickly
- **Investment committees**: Provide data-driven sector views
- **Risk management**: Identify potential downside risks

---

## ⚠️ Limitations

1. **Not Financial Advice**: This tool is for research purposes only. Always do your own due diligence.

2. **Model Limitations**: LLM outputs may contain errors or biases. Verify critical information.

3. **Market Complexity**: Real market movements depend on many factors beyond news sentiment.

4. **Latency**: Analysis takes 30-60 seconds. Not suitable for high-frequency trading.

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality

The project enforces strict code quality standards:

- **Type Hints**: All functions must have type annotations
- **Docstrings**: Google-style docstrings for all public APIs
- **Testing**: Minimum 80% test coverage
- **Formatting**: Black code style
- **Linting**: Ruff for fast linting
- **Type Checking**: Mypy strict mode

### Adding New Sectors

Edit `src/news_impact/sectors.py`:

```python
SECTORS["NEW_SECTOR"] = Sector(
    code="NEW_SECTOR",
    name_zh="新板块",
    name_en="New Sector",
    description_zh="板块描述",
    description_en="Sector description",
)
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data**: A-share sector classification based on SW (申万) industry standards
- **LLM**: Powered by Alibaba Qwen models via DashScope API
- **Inspiration**: Multi-agent architecture inspired by recent advances in AI simulation

---

## 📬 Contact

- **Author**: Yucheng Wang
- **Email**: wangreits@163.com
- **GitHub**: [@wzwangyc](https://github.com/wzwangyc)

---

## 🗺️ Roadmap

- [ ] **v0.2.0**: Add backtesting framework
- [ ] **v0.3.0**: Integrate real-time news feeds
- [ ] **v0.4.0**: Add港股 (HK-share) and 美股 (US-share) support
- [ ] **v0.5.0**: Web dashboard with interactive charts
- [ ] **v1.0.0**: Production release with API server

---

*Last updated: 2026-03-31*
