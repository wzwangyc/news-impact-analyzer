# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :x:                |
| 0.2.x   | :x:                |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

We take the security of News Impact Analyzer seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **DO NOT** create a public GitHub issue
2. Email: wangreits@163.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Time

- **Initial response**: Within 24 hours
- **Status update**: Within 7 days
- **Fix timeline**: Depends on severity (critical: 7 days, high: 14 days, medium: 30 days)

## Security Best Practices

### For Users

1. **API Keys**:
   - Never commit `.env` files to Git
   - Use environment variables for API keys
   - Rotate keys regularly

2. **Input Validation**:
   - Validate news text length (10-10,000 characters)
   - Sanitize user inputs
   - Use HTTPS for API calls

3. **Dependencies**:
   - Keep dependencies up to date
   - Run `pip-audit` regularly: `pip install pip-audit && pip-audit`

### For Contributors

1. **Code Security**:
   - No hardcoded credentials
   - Validate all inputs
   - Use parameterized queries (if using databases)
   - Follow secure coding practices

2. **Secret Scanning**:
   - Pre-commit hooks include gitleaks
   - GitHub CodeQL runs on every PR

## Security Scans

This project uses automated security scanning:

- **GitHub CodeQL**: Code vulnerability scanning
- **Dependabot**: Dependency vulnerability alerts
- **pip-audit**: Python dependency auditing
- **bandit**: Python security linting

## Known Security Considerations

1. **LLM API Calls**:
   - News text is sent to external LLM APIs
   - Ensure no sensitive information in news text
   - Use official API endpoints only

2. **Data Privacy**:
   - No user data is stored
   - API keys stored in `.env` (gitignored)
   - No telemetry or analytics

## Security Updates

Security updates will be released as patch versions (e.g., 0.5.1, 0.5.2). Subscribe to releases to stay informed.

---

**Last Updated**: 2026-03-31
**Version**: 0.5.0
