# Fail Fast 原则实现文档

## 📋 概述

本项目严格遵循 **Fail Fast（快速失败）** 原则，确保：
- 错误尽早暴露
- 问题快速定位
- 调试成本最小化
- 无静默失败

---

## 🎯 五大核心原则

### 1️⃣ 入参提前校验，非法立即抛错终止

**实现位置**: `analyzer.py`, `llm_client.py`, `cli.py`

```python
def analyze(self, news_text: str) -> dict[str, Any]:
    # Fail Fast: 在任何处理之前验证输入
    self._validate_news_input(news_text)
    
    # 只有验证通过才继续执行
    # ...
```

**验证规则**:
- ✅ 类型检查 - 必须是 `str`
- ✅ 空值检查 - 不能为空字符串
- ✅ 空白检查 - 不能仅包含空白字符
- ✅ 长度检查 - 10-10,000 字符
- ✅ 格式检查 - 根据业务规则验证

**错误示例**:
```python
analyzer.analyze("")           # ❌ ValueError: cannot be empty
analyzer.analyze("太短")        # ❌ ValueError: too short (2 chars)
analyzer.analyze(123)          # ❌ TypeError: must be a string
analyzer.analyze(None)         # ❌ TypeError: must be a string
```

**正确示例**:
```python
analyzer.analyze("央行宣布降准 0.5 个百分点")  # ✅ 通过验证
```

---

### 2️⃣ 禁止静默吞错，异常必提示必上报

**实现位置**: `cli.py`, `llm_client.py`

```python
try:
    result = analyzer.analyze(news)
except ConfigurationError as e:
    # ❌ 禁止：pass 或忽略
    # ✅ 必须：清晰报告错误并提供解决方案
    console.print(f"❌ Configuration Error: {e}")
    console.print("To fix: 1. Copy .env.example to .env...")
    return 1
```

**错误处理策略**:

| 错误类型 | 处理方式 | 用户提示 |
|---------|---------|---------|
| `ConfigurationError` | 立即终止 | 配置步骤 + 获取链接 |
| `LLMRateLimitError` | 立即终止 | 等待时间 + 限流说明 |
| `LLMTimeoutError` | 立即终止 | 解决方案（网络/长度/超时） |
| `LLMClientError` | 立即终止 | 检查 API Key + 网络 |
| `ValueError` | 立即终止 | 输入要求 + 示例 |
| `TypeError` | 立即终止 | 类型要求 + 示例 |
| 其他异常 | 立即终止 | 详细错误 + `--verbose` 堆栈 |

**禁止行为**:
```python
# ❌ 禁止：静默吞错
try:
    result = api_call()
except Exception:
    pass  # 绝对不能这样！

# ❌ 禁止：模糊错误
if not result:
    raise Exception("出错了")  # 必须具体说明

# ❌ 禁止：继续执行
if validation_failed:
    log_error()  # 仅记录日志
    continue  # 继续处理 - 不允许！
```

---

### 3️⃣ 强类型约束，数据结构不合法即中断

**实现位置**: `config.py`, `models.py`, `analyzer.py`

**配置验证**:
```python
class Settings(BaseSettings):
    llm_api_key: SecretStr = Field(
        ...,
        min_length=10,
    )
    
    @field_validator('llm_api_key')
    @classmethod
    def validate_api_key_not_empty(cls, v: SecretStr) -> SecretStr:
        key_value = v.get_secret_value()
        
        # 拒绝占位符
        if key_value.lower() in ['your_api_key', 'placeholder']:
            raise ConfigurationError("API key not configured")
        
        # 拒绝过短密钥
        if len(key_value) < 10:
            raise ConfigurationError("API key too short")
        
        return v
    
    model_config = SettingsConfigDict(
        extra="forbid",  # 拒绝未知字段
    )
```

**模型验证**:
```python
class AnalysisRequest(BaseModel):
    news_text: str = Field(..., min_length=10, max_length=10000)
    language: str = Field(default="zh", pattern="^(zh|en)$")
    
    # 自动验证 - 不合法即中断
```

**结果验证**:
```python
def _validate_result(self, result: dict[str, Any]) -> None:
    """验证结果结构完整性，不完整即报错"""
    required_keys = [
        "news_analysis",
        "sector_analyses",
        "bullish_top5",
        # ...
    ]
    
    for key in required_keys:
        if key not in result:
            raise RuntimeError(
                f"Analysis result missing required key: '{key}'"
            )
```

---

### 4️⃣ 接口/依赖异常快速返回，不继续执行

**实现位置**: `llm_client.py`

```python
def generate(self, prompt: str) -> str:
    # 1. 先验证输入
    self._validate_prompt(prompt)  # 失败立即抛出
    
    try:
        # 2. 调用 API
        response = self.client.chat.completions.create(...)
        
        # 3. 验证响应结构
        if not response.choices:
            raise LLMClientError("LLM response has no choices")
        
        if not response.choices[0].message.content:
            raise LLMClientError("LLM returned empty content")
        
        return response.choices[0].message.content.strip()
        
    except httpx.TimeoutException:
        # 4. 依赖异常 - 快速返回，不重试
        raise LLMTimeoutError("Request timed out")
    
    except Exception as e:
        # 5. 区分错误类型，提供针对性提示
        if "rate limit" in str(e).lower():
            raise LLMRateLimitError("API rate limit exceeded")
        if "authentication" in str(e).lower():
            raise LLMClientError("API authentication failed")
        
        raise LLMClientError(f"LLM API error: {e}")
```

**禁止行为**:
```python
# ❌ 禁止：自动重试（除非明确设计）
while True:
    try:
        return api_call()
    except Exception:
        time.sleep(1)  # 不要静默重试！

# ❌ 禁止：降级处理（除非有明确降级策略）
try:
    return api_call()
except Exception:
    return fallback_value()  # 可能掩盖问题

# ✅ 正确：快速失败
return api_call()  # 失败就抛出，让调用者决定
```

---

### 5️⃣ 代码简洁鲁棒，早校验、早报错、早退出

**实现位置**: 全项目

**早校验**:
```python
# ✅ 正确：在函数开头验证所有前置条件
def analyze(self, news_text: str) -> dict[str, Any]:
    self._validate_news_input(news_text)  # 第一行就验证
    self._validate_configuration()        # 然后验证配置
    
    # 验证通过才开始处理
    # ...
```

**早报错**:
```python
# ✅ 正确：发现错误立即抛出
def _validate_prompt(self, prompt: str) -> None:
    if not prompt:
        raise ValueError("Prompt cannot be empty")  # 立即报错
    
    if len(prompt) < 10:
        raise ValueError(f"Prompt too short ({len(prompt)} chars)")  # 立即报错
    
    # 不要收集所有错误再报告 - 第一个错误就终止
```

**早退出**:
```python
# ✅ 正确：错误时立即返回，不继续执行
def main() -> int:
    try:
        _validate_news_argument(args.news)  # 失败立即返回
    except ValueError as e:
        console.print(f"❌ Invalid Input: {e}")
        return 1  # 立即退出，不初始化 analyzer
    
    # 只有验证通过才继续
    analyzer = NewsImpactAnalyzer(...)
    # ...
```

---

## 🧪 测试覆盖

**Fail Fast 测试文件**: `tests/test_fail_fast.py`

### 测试类别

1. **配置验证测试**
   - 缺失 API Key → `ConfigurationError`
   - 占位符 API Key → `ConfigurationError`
   - 过短 API Key → `ConfigurationError`
   - 无效 Base URL → `ConfigurationError`
   - 超时设置越界 → `ConfigurationError`

2. **输入验证测试**
   - 空字符串 → `ValueError`
   - 仅空白字符 → `ValueError`
   - 长度过短 → `ValueError`
   - 非字符串类型 → `TypeError`
   - None 值 → `TypeError`

3. **LLM 客户端验证测试**
   - 空 Prompt → `ValueError`
   - 短 Prompt → `ValueError`
   - 温度越界 → `ValueError`
   - Token 数越界 → `ValueError`

4. **错误消息测试**
   - 配置错误包含解决指引
   - 输入错误包含示例

### 运行测试

```bash
# 运行所有 Fail Fast 测试
pytest tests/test_fail_fast.py -v

# 查看覆盖率
pytest tests/test_fail_fast.py --cov=src/news_impact --cov-report=html
```

---

## 📊 错误处理流程图

```
用户输入
    ↓
[1] 类型检查 (TypeError?)
    ↓ 是 → 立即报错退出
    ↓ 否
[2] 内容检查 (ValueError?)
    ↓ 是 → 立即报错退出
    ↓ 否
[3] 配置验证 (ConfigurationError?)
    ↓ 是 → 立即报错退出
    ↓ 否
[4] 依赖调用 (LLMClientError?)
    ↓ 是 → 立即报错退出
    ↓ 否
[5] 结果验证 (RuntimeError?)
    ↓ 是 → 立即报错退出
    ↓ 否
返回成功结果
```

---

## 🎯 对比：Fail Fast vs. Fail Safe

| 维度 | Fail Fast (本项目) | Fail Safe (不采用) |
|------|-------------------|-------------------|
| **错误暴露** | 立即暴露 | 可能隐藏 |
| **调试难度** | 低（错误点精确） | 高（错误点模糊） |
| **代码复杂度** | 低（简单直接） | 高（大量 try-catch） |
| **用户反馈** | 清晰明确 | 可能困惑 |
| **适用场景** | 开发/测试/生产 | 高可用系统 |
| **本项目选择** | ✅ 采用 | ❌ 不采用 |

**原因**：
- 本项目是**分析工具**，不是关键业务系统
- 需要**快速调试和迭代**
- 用户是**专业人士**，能处理明确错误
- **数据质量**比可用性更重要

---

## 🔍 代码审查清单

提交代码前检查：

- [ ] 所有公共函数都有输入验证
- [ ] 验证逻辑在函数开头（早校验）
- [ ] 错误消息清晰且可操作
- [ ] 没有静默吞错（`except: pass`）
- [ ] 没有模糊错误（`raise Exception("出错了")`）
- [ ] 类型注解完整
- [ ] 配置验证在启动时完成
- [ ] 依赖失败快速返回
- [ ] 结果验证在返回前完成
- [ ] 测试覆盖所有失败路径

---

## 📚 参考资源

- [Fail Fast Principle - Wikipedia](https://en.wikipedia.org/wiki/Fail-fast)
- [The Fail-Fast Principle - Martin Fowler](https://martinfowler.com/ieeeSoftware/failFast.pdf)
- [Pydantic Best Practices](https://docs.pydantic.dev/latest/concepts/models/#best-practices)

---

*最后更新：2026-03-31*
