---
name: Documentation Improvement
description: Suggest improvements to documentation
title: "[DOCS] "
labels: ["documentation"]
assignees:
  - wzwangyc
body:
  - type: markdown
    attributes:
      value: |
        Thanks for helping improve our documentation!
  - type: textarea
    id: issue
    attributes:
      label: What documentation needs improvement?
      description: Describe what's unclear, outdated, or missing.
    validations:
      required: true
  - type: textarea
    id: suggestion
    attributes:
      label: Suggested Improvement
      description: How would you improve this documentation?
    validations:
      required: true
  - type: input
    id: file
    attributes:
      label: Affected Documentation File
      description: Which file(s) need updating?
      placeholder: "README.md, docs/API.md, etc."
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our [Code of Conduct](../CODE_OF_CONDUCT.md).
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
