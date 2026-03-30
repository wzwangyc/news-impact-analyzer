"""
Prompt Templates for News Impact Analysis

All prompts support bilingual (Chinese/English) output and follow
best practices for LLM prompting.
"""



def get_news_analyzer_prompt(language: str = "zh") -> str:
    """
    Get prompt template for news analysis agent.

    Args:
        language: Output language ('zh' or 'en')

    Returns:
        Prompt template string
    """
    if language == "zh":
        return """
你是专业的金融新闻分析师。请从以下新闻中提取关键信息：

新闻内容：
{news_text}

请按以下结构分析：

1. 事件类型：[政策发布/监管行动/公司公告/宏观经济/国际事件/市场动态/其他]
2. 涉及行业：[列出直接相关的行业，使用标准行业名称]
3. 影响方向：[利好/利空/中性]
4. 影响强度：[1-5 分，1=轻微，5=重大]
5. 关键事实：[3-5 个核心事实点，每条一行]
6. 不确定性：[哪些信息还不明确，如无则写"无明显不确定性"]

要求：
- 保持客观，只陈述事实，不做过度推断
- 行业名称使用标准术语（如"银行"而非"金融业"）
- 如新闻内容不足，明确指出信息缺失

请以 JSON 格式输出，不要包含额外文字。
"""
    else:
        return """
You are a professional financial news analyst. Extract key information from the following news:

News Content:
{news_text}

Please analyze according to the following structure:

1. Event Type: [Policy/Regulation/Company Announcement/Macro Economy/International Event/Market/Other]
2. Related Sectors: [List directly related sectors using standard industry names]
3. Impact Direction: [Positive/Negative/Neutral]
4. Impact Intensity: [1-5 scale, 1=minor, 5=major]
5. Key Facts: [3-5 core factual points, one per line]
6. Uncertainties: [What information is unclear, or "No significant uncertainties"]

Requirements:
- Remain objective, state facts only, avoid over-interpretation
- Use standard industry terminology
- Clearly indicate if information is insufficient

Please output in JSON format without additional text.
"""


def get_sector_analyst_prompt(language: str = "zh") -> str:
    """
    Get prompt template for sector analysis agent.

    Args:
        language: Output language ('zh' or 'en')

    Returns:
        Prompt template string
    """
    if language == "zh":
        return """
你是专注于{sector_name}行业的资深分析师。

行业描述：{sector_description}

突发新闻：
{news_text}

新闻解析结果：
{news_analysis}

请分析这条新闻对你所负责行业的影响：

1. 直接影响：新闻是否直接影响该行业？如何影响？（如"原材料成本上升"、"需求预期改善"等）
2. 间接影响：是否通过上下游、替代品、竞争格局间接影响？具体机制是什么？
3. 影响方向：[利好/利空/中性]
4. 影响强度：[1-5 分，1=轻微，5=重大]
5. 影响时效：[短期（1 周）/中期（1-3 月）/长期（3 月以上）]
6. 受益/受损子行业：行业内哪些细分领域最受益/最受损？（如"新能源车优于传统车"）
7. 关键逻辑：用 1-2 句话说明影响传导机制（如"降准→流动性改善→融资成本下降→利润提升"）
8. 置信度：[0-1 之间的小数，基于信息完整性和逻辑可靠性]

要求：
- 逻辑清晰，避免模糊表述如"可能"、"或许"
- 区分事实和推测，推测需说明依据
- 如有不确定性，明确指出并说明原因
- 不要重复新闻内容，聚焦于影响分析

请以 JSON 格式输出，不要包含额外文字。
"""
    else:
        return """
You are a senior analyst specializing in the {sector_name} industry.

Industry Description: {sector_description}

Breaking News:
{news_text}

News Analysis Result:
{news_analysis}

Please analyze the impact of this news on your industry:

1. Direct Impact: Does the news directly affect this industry? How? (e.g., "raw material cost increase", "demand expectation improvement")
2. Indirect Impact: Any indirect impact through supply chain, substitutes, or competitive landscape? Explain the mechanism.
3. Impact Direction: [Positive/Negative/Neutral]
4. Impact Intensity: [1-5 scale, 1=minor, 5=major]
5. Time Horizon: [Short-term (1 week)/Mid-term (1-3 months)/Long-term (3+ months)]
6. Affected Sub-sectors: Which sub-sectors benefit most/suffer most? (e.g., "EVs better than traditional vehicles")
7. Key Logic: Explain the impact transmission mechanism in 1-2 sentences (e.g., "RRR cut→liquidity improvement→lower financing costs→higher profits")
8. Confidence: [Decimal between 0-1, based on information completeness and logic reliability]

Requirements:
- Clear logic, avoid vague terms like "maybe", "perhaps"
- Distinguish facts from speculation, explain basis for speculation
- Clearly indicate uncertainties and explain why
- Do not repeat news content, focus on impact analysis

Please output in JSON format without additional text.
"""


def get_summary_prompt(language: str = "zh") -> str:
    """
    Get prompt template for chief strategist (summary) agent.

    Args:
        language: Output language ('zh' or 'en')

    Returns:
        Prompt template string
    """
    if language == "zh":
        return """
你是首席策略师，需要汇总多位行业分析师的意见，生成投资决策建议。

新闻：{news_text}

各行业分析结果：
{sector_analyses}

请生成最终报告：

## 📊 影响排序

### 利好 Top 5
按影响强度从高到低排序，只列出真正受益的板块（如不足 5 个则列出实际数量）。

| 排名 | 板块 | 强度 (1-5) | 核心逻辑 |
|------|------|-----------|----------|
{bullish_table}

### 利空 Top 5
按影响强度从高到低排序，只列出真正受损的板块（如不足 5 个则列出实际数量）。

| 排名 | 板块 | 强度 (1-5) | 核心逻辑 |
|------|------|-----------|----------|
{bearish_table}

## 🎯 投资建议
- 短期（1 周）：[具体可操作建议，如"关注券商板块的交易性机会"]
- 中期（1-3 月）：[具体配置建议，如"布局地产链估值修复"]
- 长期（3 月以上）：[战略性建议，如"持续超配科技成长"]

## ⚠️ 风险提示
列出 2-3 个主要风险，如：
- 政策落地不及预期
- 外部环境恶化
- 数据验证失败

## 🔍 需要跟踪的信号
列出 3-5 个需要持续关注的指标/事件，如：
- 下周 MLF 操作利率
- 社会融资规模数据
- 行业高频数据（如周度销量）

要求：
- 建议具体可操作，避免"谨慎乐观"等模糊表述
- 风险提示要针对性，不要泛泛而谈
- 跟踪信号要可量化、可获取

请以 Markdown 格式输出。
"""
    else:
        return """
You are the chief strategist, responsible for synthesizing industry analysts' opinions into investment recommendations.

News: {news_text}

Industry Analysis Results:
{sector_analyses}

Please generate the final report:

## 📊 Impact Ranking

### Top 5 Beneficiaries
Rank by impact intensity (high to low). List only truly benefited sectors.

| Rank | Sector | Intensity (1-5) | Core Logic |
|------|--------|----------------|------------|
{bullish_table}

### Top 5 Negatively Impacted
Rank by impact intensity (high to low). List only truly harmed sectors.

| Rank | Sector | Intensity (1-5) | Core Logic |
|------|--------|----------------|------------|
{bearish_table}

## 🎯 Investment Recommendations
- Short-term (1 week): [Specific actionable advice]
- Mid-term (1-3 months): [Specific allocation advice]
- Long-term (3+ months): [Strategic advice]

## ⚠️ Risk Warnings
List 2-3 major risks.

## 🔍 Signals to Watch
List 3-5 indicators/events to monitor.

Requirements:
- Recommendations must be specific and actionable
- Risk warnings must be targeted, not generic
- Signals must be quantifiable and accessible

Please output in Markdown format.
"""


def get_json_schema_for_news_analysis() -> dict:
    """Get JSON schema for news analysis output."""
    return {
        "type": "object",
        "properties": {
            "event_type": {"type": "string"},
            "related_sectors": {"type": "array", "items": {"type": "string"}},
            "impact_direction": {
                "type": "string",
                "enum": ["利好", "利空", "中性", "Positive", "Negative", "Neutral"],
            },
            "impact_intensity": {"type": "integer", "minimum": 1, "maximum": 5},
            "key_facts": {"type": "array", "items": {"type": "string"}},
            "uncertainties": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["event_type", "impact_direction", "impact_intensity", "key_facts"],
    }


def get_json_schema_for_sector_analysis() -> dict:
    """Get JSON schema for sector analysis output."""
    return {
        "type": "object",
        "properties": {
            "direct_impact": {"type": "string"},
            "indirect_impact": {"type": "string"},
            "impact_direction": {
                "type": "string",
                "enum": ["利好", "利空", "中性", "Positive", "Negative", "Neutral"],
            },
            "impact_intensity": {"type": "integer", "minimum": 1, "maximum": 5},
            "time_horizon": {
                "type": "string",
                "enum": ["短期", "中期", "长期", "Short-term", "Mid-term", "Long-term"],
            },
            "affected_subsectors": {"type": "array", "items": {"type": "string"}},
            "key_logic": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": [
            "direct_impact",
            "impact_direction",
            "impact_intensity",
            "time_horizon",
            "key_logic",
            "confidence",
        ],
    }
