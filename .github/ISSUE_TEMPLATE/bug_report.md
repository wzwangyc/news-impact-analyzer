---
name: Bug Report
description: Create a report to help us improve
title: "[BUG] "
labels: ["bug"]
assignees:
  - wzwangyc
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
      value: "A bug happened!"
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce the issue?
      placeholder: |
        1. Install package
        2. Run command...
        3. See error
      render: bash
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version
      description: What version of News Impact Analyzer are you running?
      placeholder: v0.5.0
    validations:
      required: true
  - type: input
    id: python-version
    attributes:
      label: Python Version
      description: What Python version are you using?
      placeholder: "3.11"
    validations:
      required: true
  - type: input
    id: os
    attributes:
      label: Operating System
      description: What OS are you running?
      placeholder: "Ubuntu 22.04 / Windows 11 / macOS 14"
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant Log Output
      description: Please copy and paste any relevant log output. This will be automatically formatted into code.
      render: shell
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our [Code of Conduct](../CODE_OF_CONDUCT.md).
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
