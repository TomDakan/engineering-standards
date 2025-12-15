# Code Review Checklist v1.0.0

This checklist is auto-generated from the engineering standards. Use it to verify PRs.

## Core Standards

### Architecture & Design

#### Coupling & Cohesion
- [ ] Is high cohesion maintained (related things stay together)?
- [ ] Is loose coupling preserved (dependencies are minimized and explicit)?
- [ ] Are circular dependencies avoided?
#### DRY (Don't Repeat Yourself)
- [ ] Is duplicated logic extracted into reusable functions or components?
- [ ] Are magic numbers/strings replaced with named constants?
#### SOLID Principles (General Application)
- [ ] Is the Open/Closed principle respected (open for extension, closed for modification)?
- [ ] Are abstractions leaked? (Does the caller know too much about the implementation?)
#### Type Safety & Data Modeling
- [ ] Are primitives replaced with rich domain types where appropriate?
- [ ] Are interfaces used to define contracts for dependencies?
- [ ] Is null/none handled explicitly (e.g., Option types)?
#### Object-Oriented Best Practices
- [ ] Is deep inheritance avoided in favor of composition?
- [ ] Are dependencies injected (no hidden `new` or global access)?
- [ ] Is strict encapsulation maintained (no leaking internal state)?
#### Functional & Event-Driven
- [ ] Are Value Objects immutable?
- [ ] Is business logic isolated from I/O side effects?
- [ ] Are events used correctly for decoupling, without creating "Event Spaghetti"?
- [ ] Are event flows traceable (correlation_id)?
#### System Boundaries
- [ ] Does the code respect architectural boundaries (e.g., Domain ignoring UI)?
- [ ] Are DTOs used at boundaries to prevent leaking internal models?
### Readability & Clarity

#### Naming Conventions
- [ ] Do variable, function, and class names clearly reveal their intent?
- [ ] Are names consistent with the existing codebase style?
- [ ] Are abbreviations avoided unless they are universally understood?
#### Complexity
- [ ] Are functions short and focused on a single task (Single Responsibility Principle)?
- [ ] Is the nesting depth minimized (avoiding "arrow code")?
- [ ] Can complex conditional logic be simplified or extracted into helper functions?
#### Comments & Documentation
- [ ] Do comments explain the "why" rather than the "what" (the code shows the "what")?
- [ ] Are outdated comments removed?
- [ ] Is public API documentation present and accurate?
### Reliability & Error Handling

#### Error Strategy
- [ ] Are expected failures handled as return values (Result types) instead of exceptions?
- [ ] Are exceptions reserved for truly unexpected scenarios?
- [ ] Are errors caught at the appropriate level?
- [ ] Are exceptions specific rather than generic (e.g., `ValueError` vs `Exception`)?
- [ ] Are swallowed exceptions avoided (no empty catch blocks)?
#### Resilience
- [ ] Do all external calls have timeouts?
- [ ] Are retries bounded and exponential (not infinite/immediate)?
- [ ] Is circuit breaking involved for unstable dependencies?
#### Resource Management
- [ ] Are resources (sockets, files, DB connections) properly closed or disposed of, even in error states?
- [ ] Is there a rollback mechanism for failed multi-step operations?
#### Data Integrity
- [ ] Are operations atomic? (State is valid even after failure).
- [ ] Is shared state thread-safe?
- [ ] Are race conditions or deadlocks considered?
#### Observability
- [ ] Do logs contain searchable context (IDs) and correct log levels?
- [ ] Are exceptions wrapped to preserve cause but decoupled from implementation details?
### Security

#### Input Validation
- [ ] Is all external input validated and sanitized before use?
#### Deserialization
- [ ] Are unsafe serialization libraries avoided?
- [ ] Is the deserialization process restricted to data types only?
#### Data Exposure
- [ ] Is sensitive data (passwords, tokens, PII) kept out of logs and source control?
### Performance & Efficiency

#### Database
- [ ] Are N+1 queries avoided (no queries inside loops)?
- [ ] Is `SELECT *` avoided in favor of specific columns?
- [ ] Are indexes present for query predicates?
#### Memory & Resources
- [ ] Are large datasets processed stream-wise?
- [ ] Are resources properly released?
#### Algorithms
- [ ] Are $O(n^2)$ partial matches replaced with efficient lookups?
### API Design

#### HTTP Compliance
- [ ] Are standard status codes used (not always returning 200)?
- [ ] Are safe methods (GET) effectively read-only?
- [ ] Is the API versioned?
#### Data & Errors
- [ ] Are dates formatted as ISO 8601?
- [ ] Do error responses follow the defined schema?
### Testing & Quality Assurance

#### Test Coverage
- [ ] Does the new code have accompanying unit tests?
- [ ] Do tests cover edge cases and failure modes, not just the "happy path"?
#### Test Quality
- [ ] Are the tests readable and maintainable?
- [ ] Are assertions specific and meaningful?

## Language Specifics

### Delphi
### Python
* **Traceability**
  * Do async worker functions accept `correlation_id`?
  * Is context propagated to all background tasks?
* **Safety**
  * Is `asyncio.TaskGroup` (or equivalent) used instead of naked `create_task`?
  * Are blocking calls avoided in the event loop?
* **Type Safety**
  * Are all public functions fully type-hinted?
  * Are complex `Any` or `Dict` types avoided in favor of Dataclasses or TypedDicts?
* **Complexity**
  * Is the cyclomatic complexity of every function under 10?
  * Are functions short (approx. < 30 lines)?
* **Style**
  * Does code pass `ruff` linting without errors?
  * Are imports absolute (no `from . import`)?
  * Are line lengths respected (soft 90, hard 120)?
* **Conventions**
  * Do function/variable names match `^[a-z_][a-z0-9_]*$`?
  * Do class names match `^[A-Z][a-zA-Z0-9]*$`?
  * Are "Hungarian notation" prefixes avoided (except where mandated)?
