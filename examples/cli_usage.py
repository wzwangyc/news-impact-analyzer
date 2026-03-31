#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: CLI usage demonstration.

This example shows how to use the news-impact CLI tool.

Usage:
    python examples/cli_usage.py

Or directly from command line:
    news-impact "新闻内容" [OPTIONS]
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str]) -> int:
    """Run command and return exit code."""
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(command)
    return result.returncode


def main() -> None:
    """Run CLI usage examples."""
    print("=" * 60)
    print("News Impact CLI - Usage Examples")
    print("=" * 60)
    
    # Example 1: Basic usage (Chinese)
    print("\n[Example 1] Basic Chinese news analysis:")
    run_command([
        sys.executable, "-m", "news_impact.cli",
        "央行宣布降准 0.5 个百分点",
    ])
    
    # Example 2: English output
    print("\n[Example 2] English output:")
    run_command([
        sys.executable, "-m", "news_impact.cli",
        "央行降准",
        "--language", "en",
    ])
    
    # Example 3: JSON output
    print("\n[Example 3] JSON output:")
    run_command([
        sys.executable, "-m", "news_impact.cli",
        "新能源汽车政策",
        "--output", "json",
    ])
    
    # Example 4: Help
    print("\n[Example 4] Help:")
    run_command([
        sys.executable, "-m", "news_impact.cli",
        "--help",
    ])
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
