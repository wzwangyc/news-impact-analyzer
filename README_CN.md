# News Impact Analyzer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-000000.svg)](https://mypy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**基于 AI 多 Agent 系统的 A 股市场突发新闻影响分析工具**

[English README](README.md) | [文档](docs/) | [示例](examples/)

> 📊 **在市场波动前预测走势**  
> 🤖 **28+ 行业分析师 Agent 模拟**  
> 🌐 **中英双语支持**

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/wzwangyc/news-impact-analyzer.git
cd news-impact-analyzer

# 安装依赖
pip install -e ".[dev]"

# 复制环境配置
cp .env.example .env

# 编辑 .env 并添加 API Key
# 从以下地址获取 API Key：https://bailian.console.aliyun.com/
```

### 使用方法

**命令行：**

```bash
# 分析中文新闻
news-impact "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元"

# 分析英文新闻
news-impact "Central bank announces 0.5% RRR cut" --language en

# JSON 格式输出
news-impact "央行降准" --output json
```

**Python API：**

```python
from news_impact import NewsImpactAnalyzer

# 初始化分析器
analyzer = NewsImpactAnalyzer(language="zh")

# 分析新闻
result = analyzer.analyze("央行宣布降准 0.5 个百分点")

# 查看利好板块
print("📈 利好 Top 5:")
for sector in result["bullish_top5"]:
    print(f"  {sector.rank}. {sector.sector_name} (强度：{'⭐' * sector.intensity})")
```

---

## 📊 核心功能

### 1. 新闻解析
- 自动提取关键信息
- 事件类型识别（政策/监管/公司公告/宏观经济/国际事件）
- 影响方向和强度评估

### 2. 行业分析
覆盖全部 28 个申万一级行业：
- **金融**: 银行、保险、证券
- **周期**: 房地产、建材、钢铁、煤炭、有色、化工
- **制造**: 汽车、机械、军工、家电
- **科技**: 电子、计算机、通信
- **消费**: 食品饮料、纺织服装、轻工、商贸、社服、美容
- **其他**: 医药、电力、交通、农业、传媒、环保

### 3. 智能推荐
- 利好/利空 Top 5 板块
- 短期/中期/长期投资建议
- 风险提示
- 需要跟踪的信号

---

## 📁 项目结构

```
news-impact-analyzer/
├── src/news_impact/      # 核心包
│   ├── analyzer.py       # 主分析引擎
│   ├── models.py         # 数据模型
│   ├── prompts.py        # Prompt 模板
│   ├── sectors.py        # 行业定义
│   ├── llm_client.py     # LLM 客户端
│   └── config.py         # 配置管理
├── tests/                # 测试套件
├── docs/                 # 文档
├── examples/             # 使用示例
└── scripts/              # 工具脚本
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 带覆盖率
pytest --cov=src/news_impact --cov-report=html

# 类型检查
mypy src/news_impact

# 代码格式化
black src/news_impact tests
```

---

## 📖 文档

- **[理论框架](docs/THEORY.md)** - 多 Agent 系统架构
- **[方法论](docs/METHODOLOGY.md)** - 分析模型详情
- **[快速指南](INSTALL.md)** - 安装和使用指南
- **[Fail Fast 原则](docs/FAIL_FAST.md)** - 工程实践标准

---

## 🔒 安全

参见 [SECURITY.md](SECURITY.md) 了解安全政策和漏洞报告流程。

---

## 🤝 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

### 快速开始

1. Fork 仓库
2. 创建分支：`git checkout -b feature/amazing-feature`
3. 修改代码
4. 运行测试：`pytest`
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 📬 联系方式

- **作者**: Yucheng Wang
- **邮箱**: wangreits@163.com
- **GitHub**: [@wzwangyc](https://github.com/wzwangyc)

---

## 🙏 致谢

- 东方财富 - 金融数据源
- 阿里云百炼 - LLM API 支持
- 开源社区 - 各种优秀的开源工具

---

**最后更新**: 2026-03-31  
**版本**: v0.5.0
