#!/usr/bin/env python3
"""
完整系统测试脚本 - 测试新闻影响分析器的所有功能

运行方式：
py tests/test_full_system.py

测试范围：
1. 配置加载和验证
2. 输入验证（Fail Fast）
3. 实际 API 调用
4. 结果验证
5. 输出格式
"""

import sys
import time
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from news_impact import NewsImpactAnalyzer
from news_impact.config import ConfigurationError
from news_impact.config import get_settings
from news_impact.llm_client import LLMClient


def test_1_configuration():
    """测试 1: 配置加载"""
    print("\n" + "=" * 60)
    print("测试 1: 配置加载和验证")
    print("=" * 60)

    try:
        settings = get_settings()
        print("[OK] 配置加载成功")
        print(f"   - API Key: {settings.llm_api_key.get_secret_value()[:10]}...")
        print(f"   - Base URL: {settings.llm_base_url}")
        print(f"   - Model: {settings.llm_model}")
        print(f"   - Language: {settings.language}")
        return True
    except ConfigurationError as e:
        print(f"[FAIL] 配置错误：{e}")
        return False
    except Exception as e:
        print(f"[FAIL] 未知错误：{e}")
        return False


def test_2_input_validation():
    """测试 2: 输入验证（Fail Fast）"""
    print("\n" + "=" * 60)
    print("测试 2: 输入验证（Fail Fast 原则）")
    print("=" * 60)

    analyzer = NewsImpactAnalyzer(language="zh")
    tests_passed = 0
    tests_total = 0

    # 测试 2.1: 空字符串
    tests_total += 1
    try:
        analyzer.analyze("")
        print("[FAIL] 测试 2.1 失败：空字符串应该被拒绝")
    except ValueError as e:
        print(f"[OK] 测试 2.1 通过：空字符串被正确拒绝 - {e}")
        tests_passed += 1

    # 测试 2.2: 过短字符串
    tests_total += 1
    try:
        analyzer.analyze("太短")
        print("[FAIL] 测试 2.2 失败：短字符串应该被拒绝")
    except ValueError as e:
        print(f"[OK] 测试 2.2 通过：短字符串被正确拒绝 - {e}")
        tests_passed += 1

    # 测试 2.3: 非字符串类型
    tests_total += 1
    try:
        analyzer.analyze(123)  # type: ignore
        print("[FAIL] 测试 2.3 失败：非字符串应该被拒绝")
    except TypeError as e:
        print(f"[OK] 测试 2.3 通过：非字符串被正确拒绝 - {e}")
        tests_passed += 1

    # 测试 2.4: None 值
    tests_total += 1
    try:
        analyzer.analyze(None)  # type: ignore
        print("[FAIL] 测试 2.4 失败：None 应该被拒绝")
    except (TypeError, ValueError) as e:
        print(f"[OK] 测试 2.4 通过：None 被正确拒绝 - {e}")
        tests_passed += 1

    print(f"\n输入验证测试：{tests_passed}/{tests_total} 通过")
    return tests_passed == tests_total


def test_3_llm_api():
    """测试 3: LLM API 调用"""
    print("\n" + "=" * 60)
    print("测试 3: LLM API 调用")
    print("=" * 60)

    try:
        client = LLMClient()

        # 简单测试
        prompt = "用一句话说明什么是人工智能"
        print(f"发送提示：{prompt}")

        start_time = time.time()
        response = client.generate(prompt)
        elapsed = time.time() - start_time

        print(f"[OK] API 调用成功 ({elapsed:.2f}s)")
        print(f"   响应：{response[:100]}...")

        return True, response
    except Exception as e:
        print(f"[FAIL] API 调用失败：{e}")
        return False, None


def test_4_full_analysis():
    """测试 4: 完整新闻分析"""
    print("\n" + "=" * 60)
    print("测试 4: 完整新闻分析（真实 API 调用）")
    print("=" * 60)

    # 测试新闻
    test_news = [
        "央行宣布降准 0.5 个百分点，释放长期资金约 1 万亿元",
        "工信部：加快新能源汽车充电桩建设，目标 2025 年建成 2000 万个",
    ]

    analyzer = NewsImpactAnalyzer(language="zh")
    results = []

    for i, news in enumerate(test_news, 1):
        print(f"\n测试新闻 {i}: {news}")
        print("-" * 60)

        try:
            start_time = time.time()
            result = analyzer.analyze(news)
            elapsed = time.time() - start_time

            print(f"[OK] 分析完成 ({elapsed:.2f}s)")

            # 验证结果结构
            required_keys = [
                "news_analysis",
                "sector_analyses",
                "bullish_top5",
                "bearish_top5",
                "recommendations",
                "risks",
                "signals_to_watch",
            ]

            missing_keys = [k for k in required_keys if k not in result]
            if missing_keys:
                print(f"[FAIL] 结果缺少关键字段：{missing_keys}")
                results.append(False)
                continue

            # 显示摘要
            print("\n[RESULT] 结果摘要:")
            print(f"   利好板块数：{len(result['bullish_top5'])}")
            print(f"   利空板块数：{len(result['bearish_top5'])}")
            print(f"   分析板块总数：{len(result['sector_analyses'])}")

            if result["bullish_top5"]:
                print("\n   [BULLISH] 利好 Top 3:")
                for s in result["bullish_top5"][:3]:
                    stars = "*" * s.intensity
                    print(f"      {s.rank}. {s.sector_name} (强度：{stars})")

            if result["bearish_top5"]:
                print("\n   [BEARISH] 利空 Top 3:")
                for s in result["bearish_top5"][:3]:
                    stars = "*" * s.intensity
                    print(f"      {s.rank}. {s.sector_name} (强度：{stars})")

            results.append(True)

        except Exception as e:
            print(f"[FAIL] 分析失败：{e}")
            results.append(False)

    passed = sum(results)
    total = len(results)
    print(f"\n完整分析测试：{passed}/{total} 通过")
    return passed == total


def test_5_output_formats():
    """测试 5: 输出格式"""
    print("\n" + "=" * 60)
    print("测试 5: 输出格式验证")
    print("=" * 60)

    analyzer = NewsImpactAnalyzer(language="zh")
    news = "央行降准"

    try:
        result = analyzer.analyze(news)

        # 检查元数据
        if "metadata" not in result:
            print("❌ 缺少 metadata 字段")
            return False

        metadata = result["metadata"]
        print("[OK] 元数据完整:")
        print(f"   - 语言：{metadata.get('language', 'N/A')}")
        print(f"   - 处理时间：{metadata.get('processing_time_ms', 0)}ms")
        print(f"   - 模型：{metadata.get('model', 'N/A')}")

        # 检查 sector_analyses
        if not result["sector_analyses"]:
            print("[FAIL] sector_analyses 为空")
            return False

        print(f"[OK] 板块分析：{len(result['sector_analyses'])} 个行业")

        # 检查第一个板块的详细分析
        first_sector_code = list(result["sector_analyses"].keys())[0]
        first_sector = result["sector_analyses"][first_sector_code]

        print(f"\n[OK] 示例板块分析 ({first_sector.sector_name}):")
        print(f"   - 方向：{first_sector.direction.value}")
        print(f"   - 强度：{first_sector.intensity.value}/5")
        print(f"   - 时效：{first_sector.time_horizon.value}")
        print(f"   - 逻辑：{first_sector.key_logic[:50]}...")

        return True

    except Exception as e:
        print(f"[FAIL] 输出格式验证失败：{e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("新闻影响分析器 - 完整系统测试")
    print("=" * 60)

    tests = [
        ("配置加载", test_1_configuration),
        ("输入验证", test_2_input_validation),
        ("LLM API", test_3_llm_api),
        ("完整分析", test_4_full_analysis),
        ("输出格式", test_5_output_formats),
    ]

    results = []
    start_time = time.time()

    for name, test_func in tests:
        try:
            result = test_func()

            # 处理返回多个值的情况
            if isinstance(result, tuple):
                success = result[0]
            else:
                success = result

            results.append(success)
        except Exception as e:
            print(f"\n❌ 测试 {name} 异常：{e}")
            results.append(False)

    total_time = time.time() - start_time

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (name, _) in enumerate(tests):
        status = "[PASS]" if results[i] else "[FAIL]"
        print(f"  {status} - {name}")

    print(f"\n总计：{passed}/{total} 测试通过")
    print(f"总耗时：{total_time:.2f}s")

    if passed == total:
        print("\n[SUCCESS] 所有测试通过！系统可以投入使用！")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} 个测试失败，需要修复！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
