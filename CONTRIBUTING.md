# Contributing to News Impact Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing.

## 🎯 How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Python version
   - OS version
   - Steps to reproduce
   - Expected vs actual behavior

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Explain:
   - Problem you're solving
   - Proposed solution
   - Alternative approaches considered

### Pull Requests

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following code quality standards
4. **Add tests** for new functionality
5. **Ensure tests pass**: `pytest`
6. **Check code quality**:
   ```bash
   black src/news_impact tests
   ruff check src/news_impact
   mypy src/news_impact
   ```
7. **Submit PR** with clear description

## 📋 Code Standards

### Python Style

- **Black** for code formatting
- **Ruff** for linting
- **Mypy** for type checking
- **Google-style** docstrings

### Type Hints

All functions must have type hints:

```python
def analyze_news(news_text: str) -> dict[str, Any]:
    """Analyze news impact.
    
    Args:
        news_text: News content to analyze
        
    Returns:
        Analysis results dictionary
    """
```

### Testing

- Minimum 80% test coverage
- Use pytest fixtures
- Mock external API calls
- Test edge cases

## 🚀 Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/news-impact-analyzer.git
cd news-impact-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Create branch
git checkout -b feature/your-feature
```

## 🧪 Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/news_impact --cov-report=html

# Specific test file
pytest tests/test_analyzer.py -v

# Type checking
mypy src/news_impact

# Linting
ruff check src/news_impact

# Formatting
black src/news_impact tests
```

## 📝 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add HK-share sector support
fix: correct sector name translation
docs: update README examples
test: add tests for analyzer
refactor: simplify prompt templates
```

## 🔍 Code Review Process

1. All PRs require at least 1 review
2. CI must pass (tests, linting, type checking)
3. Address review feedback promptly
4. Maintain backwards compatibility

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Questions?

Open an issue or contact the maintainers.
