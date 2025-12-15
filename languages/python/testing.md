---
title: Python Testing
type: language-guide
language: python
topic: testing
version: 1.0.0
---

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
