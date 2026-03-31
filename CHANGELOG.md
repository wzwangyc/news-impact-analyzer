# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bilingual README (English/Chinese)
- GitHub Actions CI/CD pipeline
- Security scan workflow (manual)
- requirements.txt with fixed versions
- .pre-commit-config.yaml for code quality gates

### Changed
- Version bumped to 0.5.0
- License configuration updated to use file reference
- CI workflow simplified to single job
- Security scan changed to manual trigger only

### Fixed
- Black/ruff line-length configuration aligned
- Dependency installation issues in CI
- .gitignore updated to exclude sensitive files

## [0.5.0] - 2026-03-31

### Added
- Complete GitHub top-tier compliance
- Chinese README (README_CN.md)
- Dependency version locking
- Non-blocking code quality checks in CI

### Changed
- Security workflow to manual only (no automatic failures)
- Actions updated to v4/v5

## [0.1.0] - 2026-03-30

### Added
- Initial release
- Multi-agent news impact analysis
- Support for 28 A-share market sectors
- CLI interface
- Python API
- Basic documentation
