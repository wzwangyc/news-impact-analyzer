# 快速安装和使用指南

## 📦 安装

### 1. 克隆项目

```bash
cd C:\Users\28916\.openclaw\workspace
git clone https://github.com/wzwangyc/news-impact-analyzer.git
cd news-impact-analyzer
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装项目
pip install -e .
```

或者直接安装（不使用虚拟环境）：

```bash
pip install -e "C:\Users\28916\.openclaw\workspace\news-impact-analyzer"
```

### 3. 配置 API Key

```bash
# 复制环境配置模板
copy .env.example .env

# 编辑 .env 文件，填入你的 DashScope API Key
notepad .env
```

在 `.env` 文件中填入：

```env
DASHSCOPE_API_KEY=你的 API_KEY_这里
```

获取 API Key：https://bailian.console.aliyun.com/

---

## 🚀 使用方式

### 方式 1：命令行工具

```bash
# 分析中文新闻
news-impact "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"

# 分析英文新闻
news-impact "Central bank announces RRR cut" --language en

# 输出 JSON 格式
news-impact "央行降准" --output json
```

### 方式 2：Python API

创建测试脚本 `test_analysis.py`：

```python
from news_impact import NewsImpactAnalyzer

# 初始化分析器
analyzer = NewsImpactAnalyzer(language="zh")

# 分析新闻
news = "央行宣布降准 0.5 个百分点"
result = analyzer.analyze(news)

# 查看结果
print("\n📈 利好 Top 5:")
for sector in result["bullish_top5"]:
    print(f"  {sector.rank}. {sector.sector_name} (强度：{'⭐' * sector.intensity})")
    print(f"     逻辑：{sector.logic}")

print("\n📉 利空 Top 5:")
for sector in result["bearish_top5"]:
    print(f"  {sector.rank}. {sector.sector_name} (强度：{'⭐' * sector.intensity})")
    print(f"     逻辑：{sector.logic}")
```

运行：

```bash
python test_analysis.py
```

---

## 🧪 测试

```bash
# 安装测试依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 查看测试覆盖率
pytest --cov=src/news_impact --cov-report=html

# 打开覆盖率报告
start htmlcov\index.html
```

---

## 📝 代码质量检查

```bash
# 类型检查
mypy src/news_impact

# 代码格式化检查
black --check src/news_impact tests

# Linting
ruff check src/news_impact

# 格式化代码
black src/news_impact tests
```

---

## 🎯 示例新闻

试试这些示例新闻：

### 宏观经济

```bash
news-impact "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"
```

预期结果：
- ✅ 利好：银行、证券、房地产
- ❌ 利空：无明显利空

### 行业政策

```bash
news-impact "工信部：加快新能源汽车充电桩建设，目标 2025 年建成 2000 万个"
```

预期结果：
- ✅ 利好：汽车、电子、电力
- ❌ 利空：石油石化（替代效应）

### 公司事件

```bash
news-impact "某大型地产公司债务违约，涉及金额 50 亿元"
```

预期结果：
- ✅ 利好：无明显利好
- ❌ 利空：房地产、银行、建材

---

## ⚙️ 高级配置

### 更换模型

编辑 `.env`：

```env
# 更快的模型（成本低，质量略低）
LLM_MODEL_NAME=qwen-turbo

# 或更好的模型（成本高，质量最好）
LLM_MODEL_NAME=qwen-max
```

### 调整并发数

编辑 `.env`：

```env
# 增加并发（更快，但可能触发限流）
MAX_CONCURRENT_REQUESTS=10

# 减少并发（更稳定）
MAX_CONCURRENT_REQUESTS=3
```

### 调整超时时间

```env
# 增加超时（适合长新闻）
REQUEST_TIMEOUT=120

# 减少超时（更快失败）
REQUEST_TIMEOUT=30
```

---

## 🐛 常见问题

### Q: 提示 "API key expired"

A: 检查 `.env` 文件中的 API Key 是否正确，确保没有多余的空格或引号。

### Q: 分析速度太慢

A: 
1. 减少并发数（`MAX_CONCURRENT_REQUESTS=3`）
2. 使用更快的模型（`LLM_MODEL_NAME=qwen-turbo`）
3. 检查网络连接

### Q: 输出乱码

A: 确保终端使用 UTF-8 编码：

```bash
# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Q: 测试失败

A: 某些测试需要 API Key，跳过它们：

```bash
pytest -m "not skip"
```

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/wzwangyc/news-impact-analyzer/issues
- **邮件**: wangreits@163.com

---

*最后更新：2026-03-31*
