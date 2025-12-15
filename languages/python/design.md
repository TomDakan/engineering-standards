---
title: Python Design Guidelines
type: language-guide
language: python
topic: design
version: 1.0.0
---

#### Modern Python Idioms

* **Type Hinting**: Use type hints for all function arguments and return values.
  * *Constraint*: 100% of public API must be typed. `mypy` strict mode should be enabled.
  * *Bad*: `def greet(name): ...`
  * *Good*: `def greet(name: str) -> str: ...`

* **Complexity Verification**:
  * *Constraint*: Functions must have a Cyclomatic Complexity under 10 (checked by `mccabe` or `ruff`).
  * *Action*: Refactor complex logic into helper functions or classes.

* **List Comprehensions**: Use list comprehensions for simple transformations.
  * *Bad*: `squares = []` then loop `squares.append(x**2)`
  * *Good*: `squares = [x**2 for x in range(10)]`

* **Context Managers**: Always use context managers (`with` statement) for resource management (files, network connections).
  * *Bad*: `f = open(...) ... f.close()`
  * *Good*: `with open(...) as f: ...`

#### Structural Pattern Matching

* **Pattern Match**: Use `match/case` (Python 3.10+) for parsing complex data structures or state machines instead of deep `if/elif` chains.
  * *Example*:

    ```python
    match command:
        case {"action": "quit"}: exit()
        case {"action": "move", "direction": d}: move(d)
    ```

#### Advanced Typing

* **Protocols**: Prefer `typing.Protocol` (structural typing) over Abstract Base Classes when you only care if an object *has* certain methods, not what it inherits from.
* **Generics & TypeVar**: Use `TypeVar` to enforce relationships between arguments and return values (e.g., "this function returns the same type it was given").
* **ParamSpec**: Mandatory for decorators and higher-order functions.
  * *Constraint*: Do not type decorators as accepting `Callable[..., Any]`. Use `ParamSpec` to capture and preserve the input signature of the wrapped function.
  * *Example*:

    ```python
    P = ParamSpec("P")
    R = TypeVar("R")
    def retry(func: Callable[P, R]) -> Callable[P, R]: ...
    ```

#### Known Pitfalls

* **Mutable Default Arguments**: Never use mutable objects (lists, dicts) as default arguments.
  * *Bad*: `def append_to(element, to=[]):`
  * *Good*: `def append_to(element, to: Optional[list] = None): if to is None: to = []`

## Verification Checklist

* **Type Safety**
  * Are all public functions fully type-hinted?
  * Are complex `Any` or `Dict` types avoided in favor of Dataclasses or TypedDicts?
* **Complexity**
  * Is the cyclomatic complexity of every function under 10?
  * Are functions short (approx. < 30 lines)?
