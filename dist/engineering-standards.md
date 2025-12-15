# Engineering Standards Documentation v1.0.0

This document aggregates all engineering standards for easy reading.

---

## Part 1: Core Principles

### Architecture & Design

Core truths about boundaries, layering, and robust design.

#### Architecture & Design Principles

##### Boundaries & Layering

* **Separation of Concerns**: Distinct sections of code must address distinct concerns. User Interface logic should not bleed into Business Logic, and Database Access details should be hidden from Core Domain logic.
* **Dependency Rule**: Dependencies should point inwards. High-level policies should not depend on low-level details; low-level details should depend on high-level policies.

##### SOLID Principles

* **Single Responsibility Principle (SRP)**: A class or module should have one, and only one, reason to change.
* **Open/Closed Principle (OCP)**: Entities should be open for extension, but closed for modification.
* **Liskov Substitution Principle (LSP)**: Derived classes must be substitutable for their base classes.
* **Interface Segregation Principle (ISP)**: Many client-specific interfaces are better than one general-purpose interface.
* **Dependency Inversion Principle (DIP)**: Depend upon abstractions, not concretions.

##### DRY (Don't Repeat Yourself)

* **Single Representation**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.
* **Duplication**: Duplication leads to inconsistency and maintenance nightmares.

##### Type Safety & Data Modeling

* **Rich Domain Types**: Use specific types (e.g., `CustomerId`) instead of primitives (`int`, `string`) to enforce business rules and prevent swapping arguments.
* **Interface Usage**: Define dependencies by Interfaces (contracts) rather than Concrete Classes.
* **Null Safety**: Handle `null` explicitly. Use `Option` types or strict null-checks to signal absence of value.

##### Object-Oriented Design

* **Composition over Inheritance**: Use inheritance "is-a" sparingly. Prefer composition for sharing behavior to avoid brittle hierarchies.
* **Dependency Injection**: Inject dependencies rather than instantiating them internally. Avoid global state and singletons.
* **Law of Demeter**: Objects should only talk to their immediate friends. Don't reach deeply into other objects' internals.
* **Encapsulation**: Keep mutable state private. Expose behavior (methods), not data (getters/setters).

##### Functional & Event-Driven

* **Immutability**: Value Objects should be immutable. Default to read-only variables unless mutation is strictly required.
* **Side-Effect Isolation**: Separate "Pure Functions" (deterministic, no side effects) from "Impure Functions" (I/O, database writes).
* **Event Architecture**: Ensure event flows are traceable. Use events to decouple domains, not for linear control flow.
* **Traceability**: Messages must include `correlation_id` (process) and `causation_id` (trigger) to allow full debugging of async flows.
* **Pure Core, Imperative Shell**: Isolate business logic (pure) from side effects (shell). Logic should be testable without mocks.

#### Architecture & Design Verification Checklist

* **Coupling & Cohesion**
* Is high cohesion maintained (related things stay together)?
* Is loose coupling preserved (dependencies are minimized and explicit)?
* Are circular dependencies avoided?
* **DRY (Don't Repeat Yourself)**
* Is duplicated logic extracted into reusable functions or components?
* Are magic numbers/strings replaced with named constants?
* **SOLID Principles (General Application)**
* Is the Open/Closed principle respected (open for extension, closed for modification)?
* Are abstractions leaked? (Does the caller know too much about the implementation?)
* **Type Safety & Data Modeling**
* Are primitives replaced with rich domain types where appropriate?
* Are interfaces used to define contracts for dependencies?
* Is null/none handled explicitly (e.g., Option types)?
* **Object-Oriented Best Practices**
* Is deep inheritance avoided in favor of composition?
* Are dependencies injected (no hidden `new` or global access)?
* Is strict encapsulation maintained (no leaking internal state)?
* **Functional & Event-Driven**
* Are Value Objects immutable?
* Is business logic isolated from I/O side effects?
* Are events used correctly for decoupling, without creating "Event Spaghetti"?
* Are event flows traceable (correlation_id)?
* **System Boundaries**
* Does the code respect architectural boundaries (e.g., Domain ignoring UI)?
* Are DTOs used at boundaries to prevent leaking internal models?

### Readability & Clarity

Writing code that can be understood by humans, not just machines.

#### Readability & Clarity Principles

* **Code for Humans**: Write code as if the next person to read it is an exhausted maintainer at 3 AM.

* **Descriptive Naming**: Variable and function names should be descriptive and unambiguous. `customer_id` is better than `cid`.

* **Small Functions**: Functions should do one thing and do it well. If a function is too long, it likely does too many things.

* **Comments**: Use comments to explain *why*, not *what*. The code itself should explain *what* it is doing.

##### Verifiable Metrics

* **Function Length**: Functions should generally be under 30 lines. > 50 lines requires justification.
* **Argument Count**: Functions should have 3 or fewer arguments. > 4 usually suggests a missing Parameter Object or Concept.
* **Cyclomatic Complexity**: Keep complexity low (under 10). Simplify conditional logic.
* **File Size**: Files should logically fit in one head context. Soft limit of 300 lines.

#### Readability & Clarity Verification Checklist

* **Naming Conventions**
* Do variable, function, and class names clearly reveal their intent?
* Are names consistent with the existing codebase style?
* Are abbreviations avoided unless they are universally understood?
* **Complexity**
* Are functions short and focused on a single task (Single Responsibility Principle)?
* Is the nesting depth minimized (avoiding "arrow code")?
* Can complex conditional logic be simplified or extracted into helper functions?
* **Comments & Documentation**
* Do comments explain the "why" rather than the "what" (the code shows the "what")?
* Are outdated comments removed?
* Is public API documentation present and accurate?

### Reliability & Error Handling

Ensuring the system behaves correctly under all conditions, especially failure.

#### Reliability & Error Handling Principles

##### Error Strategy & Flow

* **Exceptions vs Result Types**: Use Result types for expected failures (e.g., `InsufficientFunds`). Reserve exceptions for truly unexpected system states (e.g., `OutOfMemory`).
* **Input Validation**: Validate input at the boundaries of the system. Trust no one.
* **Scope**: Keep `try/catch` blocks as narrow as possible.

##### Resilience Patterns

* **Timeouts & Deadlines**: All external calls (HTTP, DB, RPC) must have explicit timeouts.
* **Retries with Backoff**: Use exponential backoff and jitter for retries. Enforce hard limits on attempts.
* **Circuit Breakers**: Fail fast if a dependent service is down to prevent cascading failures.
* **Idempotency**: Operations should be safe to retry (e.g., checking transaction state before re-charging).

##### Resource Management (RAII)

* **Automatic Cleanup**: Use language constructs (`with`, `defer`, `try-with-resources`) to guarantee resource cleanup.
* **Failure State Cleanup**: Roll back partial changes if a multi-step operation fails (compensating transactions).

##### Data Integrity & Concurrency

* **Atomicity**: Errors must leave the system in a valid state. No partial data corruption.
* **Thread Safety**: Synchronize shared mutable state. Use thread-safe collections where appropriate.

##### Observability & Debuggability

* **Structured Logging**: Use structured formats (e.g., JSON) for logs. Include `correlation_id`, `user_id`, and other context as keys, not just formatted strings.
* **Exception Wrapping**: Preserve original causes (Inner Exception) when re-throwing. Wrap generic errors in domain-specific exceptions.

#### Reliability & Error Handling Verification Checklist

* **Error Strategy**
* Are expected failures handled as return values (Result types) instead of exceptions?
* Are exceptions reserved for truly unexpected scenarios?
* Are errors caught at the appropriate level?
* Are exceptions specific rather than generic (e.g., `ValueError` vs `Exception`)?
* Are swallowed exceptions avoided (no empty catch blocks)?
* **Resilience**
* Do all external calls have timeouts?
* Are retries bounded and exponential (not infinite/immediate)?
* Is circuit breaking involved for unstable dependencies?
* **Resource Management**
* Are resources (sockets, files, DB connections) properly closed or disposed of, even in error states?
* Is there a rollback mechanism for failed multi-step operations?
* **Data Integrity**
* Are operations atomic? (State is valid even after failure).
* Is shared state thread-safe?
* Are race conditions or deadlocks considered?
* **Observability**
* Do logs contain searchable context (IDs) and correct log levels?
* Are exceptions wrapped to preserve cause but decoupled from implementation details?

### Security

Protecting the system and data from malicious intent and accidental exposure.

#### Security Principles

* **Least Privilege**: Components should operate with the minimum permissions necessary to function.

* **Sanitization**: All external input must be sanitized to prevent injection attacks.

* **No Secrets in Code**: Never hardcode credentials or secrets. Use environment variables or secure vaults.

* **Safe Deserialization**: Avoid serialization formats that allow arbitrary code execution (e.g., those that deserialize functions or objects). Prefer data-only formats like JSON.

#### Security Verification Checklist

* **Input Validation**
* Is all external input validated and sanitized before use?
* **Deserialization**
* Are unsafe serialization libraries avoided?
* Is the deserialization process restricted to data types only?
* **Data Exposure**
* Is sensitive data (passwords, tokens, PII) kept out of logs and source control?

### Performance & Efficiency

Implementing systems that use resources responsibly and scale effectively.

#### Performance & Efficiency Principles

##### Database Efficiency

* **Avoid N+1 Queries**: Do not execute queries inside loops. Use eager loading (`JOIN`, `prefetch_related`) to fetch data in batches.
* **Selective Fetching**: Avoid `SELECT *`. Fetch only the columns you need to reduce network and memory overhead.
* **Indexing**: Ensure foreign keys and frequently queried columns are indexed.

##### Memory & Resource Management

* **Streaming**: Process large datasets (files, DB result sets) via streams or iterators, not by loading everything into RAM.
* **Resource Leaks**: Explicitly close resources. Prefer idioms that do this automatically (e.g., `try-with-resources`, `using`, `with`).

##### Algorithmic Efficiency

* **Nested Loops**: Be wary of nested loops over potentially large datasets ($O(n^2)$). Convert to lookups (Hash Maps) where possible ($O(n)$).

#### Performance & Efficiency Verification Checklist

* **Database**
* Are N+1 queries avoided (no queries inside loops)?
* Is `SELECT *` avoided in favor of specific columns?
* Are indexes present for query predicates?
* **Memory & Resources**
* Are large datasets processed stream-wise?
* Are resources properly released?
* **Algorithms**
* Are $O(n^2)$ partial matches replaced with efficient lookups?

### API Design

Creating consistent, predictable, and usable interfaces.

#### API Design Principles

##### HTTP Semantics

* **Status Codes**: Use standard HTTP status codes. `200` OK, `201` Created, `400` Bad Request, `401` Unauthorized, `403` Forbidden, `404` Not Found, `500` Internal Server Error.
* **Verbs**: Use standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) correctly. `GET` must be safe and idempotent.

##### Data Formats

* **ISO 8601**: Use ISO 8601 strings (`YYYY-MM-DDTHH:MM:SSZ`) for all dates and times.
* **JSON First**: JSON is the default format for request and response bodies.
* **Consistent Errors**: Error responses must follow a standard structure (e.g., `{ "error": "code", "message": "human readable" }`).
* **Versioning**: APIs must be versioned (e.g., `/v1/resource` or `Accept: application/vnd.api.v1+json`). Never break existing clients.

#### API Design Verification Checklist

* **HTTP Compliance**
* Are standard status codes used (not always returning 200)?
* Are safe methods (GET) effectively read-only?
* Is the API versioned?
* **Data & Errors**
* Are dates formatted as ISO 8601?
* Do error responses follow the defined schema?

### Testing & Quality Assurance

Ensuring quality through rigorous automated verification.

#### Testing & Quality Assurance Verification Checklist

* **Test Coverage**
* Does the new code have accompanying unit tests?
* Do tests cover edge cases and failure modes, not just the "happy path"?
* **Test Quality**
* Are the tests readable and maintainable?
* Are assertions specific and meaningful?

## Part 2: Language Specific Standards

### Delphi

These standards apply to all Delphi code. They focus on modern Object Pascal practices, memory management, and clean architecture.

#### Contents

* [Design Principles](./design.md): Interfaces, dependency injection, and modern language features.
* [Formatting & Style](./formatting.md): PascalCase, indentation, and code organization.
* [Naming Conventions](./naming.md): `T` prefix, argument naming, and removing Hungarian notation.

## Quick Start

Ensure your IDE is configured with the standard formatter compliance settings (see `DelphiFormatter.config`).

#### Delphi Design

## Modern Object Pascal

* **Interfaces**: Prefer interface-based design over inheritance. Use `IInterface` (or customized descendants) for all service contracts.
* **Generics**: Use `TList<T>`, `TDictionary<K,V>` from `System.Generics.Collections` instead of older `TList` or `TStringList` where improved type safety is possible.
* **Method Injection**: Prefer injecting dependencies via constructor or method arguments rather than creating them inside classes.

## Memory Management

* **Try...Finally**: Every object creation *must* have a matching `try...finally` block if it's not owned by a container.

```delphi
    LObj := TMyClass.Create;
    try
      LObj.DoSomething;
    finally
      LObj.Free;
    end;
```

* **FastMM**: Ensure FastMM is used in FullDebugMode during development to catch leaks.

## Known Pitfalls

* **With Statement**: Avoid the `with` statement. It introduces ambiguity and makes debugging harder.
* **Global Variables**: Severely restrict the use of global variables in initialization sections.

#### Delphi Formatting

# Delphi Formatting & Style

## Standards

*   **Indentation**: 2 spaces. No tabs.
*   **Margins**: 120 characters.

## Code Organization

*   **Class Layout**:
    1.  `private` fields
    2.  `private` methods
    3.  `protected`
    4.  `public` properties
    5.  `public` constructors/destructors
    6.  `public` methods

## Comments

*   Use XML Documentation `///` for all public methods to enable hovering support.

#### Delphi Naming

# Delphi Naming Conventions

## General Rules

*   **Types**: Prefix with `T` (e.g., `TCustomer`).
*   **Interfaces**: Prefix with `I` (e.g., `ICustomerService`).
*   **Fields**: Prefix with `F` (e.g., `FAdHoc`).
*   **Arguments**: Prefix with `A` (e.g., `procedure Update(AName: string)`).
*   **Locals**: Prefix with `L` (e.g., `LResult`).

## Specifics

*   **Components**: We do NOT use Hungarian notation for components (e.g., `btnSubmit`). Use descriptive names `SubmitButton`.
*   **Enums**: Prefix with two or three letters related to the type (e.g., `TStatus = (stActive, stInactive)`).

#### Delphi Concurrency


#### Delphi Security


#### Delphi Testing


### Python

These standards apply to all Python code within the organization. They are designed to ensure consistency, readability, and maintainability across all projects.

#### Contents

* [Design Principles](./design.md): Idioms, patterns, and best practices.
* [Formatting & Style](./formatting.md): Linting, whitespace, and code layout.
* [Naming Conventions](./naming.md): Rules for naming variables, functions, classes, and modules.

#### Python Design

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

#### Python Formatting

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

#### Python Naming

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

#### Python Concurrency

#### I/O Bound (Network/Disk)

* **Modern**: Use `asyncio` for scalable I/O.
* **Event Loop Blocking**: Strict prohibition of blocking I/O (synchronous `requests`, `time.sleep`) within `async` functions.
* **Task Groups**: Use `asyncio.TaskGroup` (Python 3.11+) or safe wrappers to manage background tasks; never use "fire-and-forget" `create_task` without references.
* **Traceability**: All async functions processing business events must accept and propogate `correlation_id` (via context variables or explicit arguments) to ensure logs are traceable across async boundaries.

#### CPU Bound (Math/Data)

* **Standard**: Use `ProcessPoolExecutor` to utilize multiple cores and bypass the GIL.
* **Constraints**: Arguments must be serializable (pickleable). No lambdas, no open sockets.
* **Overhead**: Avoid offloading tiny tasks (microseconds) to a process pool due to start-up overhead.
* **Safety**: Code using multiprocessing must be guarded by `if __name__ == "__main__":`.

## Verification Checklist

* **Traceability**
  * Do async worker functions accept `correlation_id`?
  * Is context propagated to all background tasks?
* **Safety**
  * Is `asyncio.TaskGroup` (or equivalent) used instead of naked `create_task`?
  * Are blocking calls avoided in the event loop?

#### Python Security

#### Deserialization

* **Flag `pickle`**: Usage of `pickle` and `yaml.load` (unsafe) are critical vulnerabilities. Use `json` or `yaml.safe_load`.

#### Path Safety

* **Pathlib Resolution**: Mandate `pathlib` usage over `os.path` string manipulation to prevent directory traversal attacks.
  * *Check*: Use `.resolve().is_relative_to(base_dir)` to validate paths.

#### Secrets

* **Env Vars**: No hardcoded secrets. Use `os.environ` or a secrets manager.

#### Python Testing

#### Framework

* **Pytest**: We use `pytest` as our standard testing framework. Avoid `unittest.TestCase` unless working on legacy code that cannot be easily updated.

#### Modern Idioms

* **Fixtures over `setUp`**: Use `pytest.fixture` for setup and teardown. Fixtures are more modular, scalable, and explicit than `setUp`/`tearDown` methods.
  * *Bad*: `def setUp(self): self.db = connect()`
  * *Good*: `@pytest.fixture \n def db(): ...`

* **Parametrization**: Use `@pytest.mark.parametrize` for data-driven tests instead of loops or repeated test methods.
  * *Bad*: Loop over inputs inside a single test.
  * *Good*: One test case, decorated with multiple inputs.

* **Markers**: Use markers (e.g., `@pytest.mark.slow`, `@pytest.mark.integration`) to categorize tests.


## Part 4: Template Usage

To start a new project, copy `templates/project-context-template.md` to your repository root and fill it in.