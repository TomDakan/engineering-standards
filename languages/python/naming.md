---
title: Python Naming Conventions
type: language-guide
language: python
topic: naming
version: 1.0.0
---

#### General Rules

* **Variables/Functions**: `snake_case` (Regex: `^[a-z_][a-z0-9_]*$`)
* **Classes/Exceptions**: `PascalCase` (Regex: `^[A-Z][a-zA-Z0-9]*$`)
* **Constants**: `UPPER_CASE` (Regex: `^[A-Z_][A-Z0-9_]*$`)
* **Private Members**: `_leading_underscore` (Regex: `^_[a-z_][a-z0-9_]*$`)

#### Specifics

* **Booleans**: Should answer a question (e.g., `is_active`, `has_permission`).
* **Collections**: Should be plural (e.g., `users`, `items`).
* **Interfaces/Abstract Base Classes**: No `I` prefix. Just `Shape`, not `IShape`.

#### Context Matters

* Avoid generic names like `data`, `info`, `manager` unless the scope is extremely small.
* Include units in variable names where ambiguous: `duration_ms`, `file_size_bytes`.

## Verification Checklist

* **Conventions**
  * Do function/variable names match `^[a-z_][a-z0-9_]*$`?
  * Do class names match `^[A-Z][a-zA-Z0-9]*$`?
  * Are "Hungarian notation" prefixes avoided (except where mandated)?
