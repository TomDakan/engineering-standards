---
title: Python Security
type: language-guide
language: python
topic: security
version: 1.0.0
---

#### Deserialization

* **Flag `pickle`**: Usage of `pickle` and `yaml.load` (unsafe) are critical vulnerabilities. Use `json` or `yaml.safe_load`.

#### Path Safety

* **Pathlib Resolution**: Mandate `pathlib` usage over `os.path` string manipulation to prevent directory traversal attacks.
  * *Check*: Use `.resolve().is_relative_to(base_dir)` to validate paths.

#### Secrets

* **Env Vars**: No hardcoded secrets. Use `os.environ` or a secrets manager.
