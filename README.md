# Engineering Standards

Welcome to the Engineering Standards repository. This repository houses the "Layered Context Architecture" for our engineering guidelines.

## Philosophy

We believe standards should be:

1. **Universal**: Core truths apply everywhere.
2. **Specific**: Language idioms matter.
3. **Local**: Projects have unique constraints.

## Structure

* **/core**: Universal principles (DRY, SOLID, Security).
* **/languages**: Tech-stack specific guides (Python, Delphi).
* **/templates**: Tools to apply these standards.

## Usage

### For Humans

Read the specific guides in `/languages` or generate a full PDF/Markdown using the `generate_docs.py` script.

### For AI Agents

Use the `generate_docs.py` script to generate a system prompt that includes Core + Language + Project Context for high-quality code reviews.

## Generation Script

This repository includes a `generate_docs.py` script to build the documentation and prompts.

**Prerequisites:**

* `uv` installed.

**Usage:**

```bash
# Generate everything (Human Docs + Generic Prompt + All Language Prompts)
uv run scripts/generate_docs.py

# Generate ONLY the Python LLM Prompt (useful for CI/CD)
uv run scripts/generate_docs.py -l python

# Generate Python LLM Prompt with Project Specific Context (Layer 3)
uv run scripts/generate_docs.py -l python -c path/to/project-context.md
```

**Output:**
Artifacts are generated in the `dist/` directory.
