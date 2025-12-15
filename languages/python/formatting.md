---
title: Python Formatting & Style
type: language-guide
language: python
topic: formatting
version: 1.0.0
---

#### Standards

* **PEP 8**: We follow PEP 8 as the baseline guide for Python code.
* **Line Length**: Soft limit at 90 characters, hard limit at 120. Enforced by `pyproject.toml` configuration.
* **Imports**: Use absolute imports (e.g. `from myproject.module import Item`) over relative imports to improve clarity and searchability.

#### Linting

* **Ruff**: For fast linting, import sorting, and formatting.
* **MyPy**: For static type checking.

#### Docstrings

* Use **Google Style** docstrings.
* Every public module, class, and method must have a docstring.

```python
def fetch_user(user_id: int) -> User:
    """Fetches a user from the database.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A User object populated with data.
    """
```

## Verification Checklist

* **Style**
  * Does code pass `ruff` linting without errors?
  * Are imports absolute (no `from . import`)?
  * Are line lengths respected (soft 90, hard 120)?
