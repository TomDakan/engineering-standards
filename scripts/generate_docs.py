import yaml
import jinja2
from pathlib import Path
import sys
import traceback
import argparse
import re


def load_standards():
    try:
        with open("core/standards.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: core/standards.yaml not found.")
        sys.exit(1)


def strip_frontmatter(content):
    """Removes YAML frontmatter from markdown content."""
    if not content:
        return ""
    # Regex to match frontmatter: start of string, ---, content, ---
    # re.DOTALL makes . match newlines
    pattern = r"^---\s*\n.*?\n---\s*\n"
    return re.sub(pattern, "", content, count=1, flags=re.DOTALL)


def setup_jinja():
    # Set up Jinja2 to load templates from the current directory
    template_loader = jinja2.FileSystemLoader(searchpath=".")
    # We want to support strict rendering eventually, but for now we'll allow undefined
    env = jinja2.Environment(
        loader=template_loader, trim_blocks=True, lstrip_blocks=True
    )
    env.filters["strip_frontmatter"] = strip_frontmatter
    return env


def render_template(env, template_path, output_path, context):
    try:
        template = env.get_template(str(template_path))
        rendered = template.render(**context)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Generated: {output_path}")
    except Exception as e:
        Path("dist").mkdir(parents=True, exist_ok=True)
        with open("dist/error.log", "a") as errf:
            errf.write(f"Error rendering {template_path}: {e}\n")
            traceback.print_exc(file=errf)
        print(f"Error rendering {template_path}: {e}")


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return ""


def load_languages():
    languages = {}
    base = Path("languages")
    if not base.exists():
        return languages

    for lang_dir in base.iterdir():
        if lang_dir.is_dir():
            lang_name = lang_dir.name
            languages[lang_name] = {}
            for md_file in lang_dir.glob("*.md"):
                key = md_file.stem
                languages[lang_name][key] = read_file(md_file)
    return languages


def extract_checklists(languages):
    """Extracts 'Verification Checklist' sections from language markdown files."""
    extracted = {}
    checklist_header = "## Verification Checklist"

    for lang, files in languages.items():
        extracted[lang] = []
        for content in files.values():
            if checklist_header in content:
                # Split and take the part after the header
                parts = content.split(checklist_header)
                if len(parts) > 1:
                    # Take the section until the next header or end of file
                    section = parts[1].split("\n#")[0].strip()
                    extracted[lang].append(section)
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description="Generate Engineering Standards Documentation"
    )
    parser.add_argument(
        "--language",
        "-l",
        action="append",
        help="Specify languages to generate (e.g., -l python)",
    )
    parser.add_argument("--context", "-c", help="Path to project context markdown file")
    parser.add_argument("--output", "-o", default="dist", help="Output directory")
    args = parser.parse_args()

    root = Path(".")
    dist = Path(args.output)

    # Load all data first
    print("Loading standards...")
    data = load_standards()

    print("Loading language specifics...")
    all_langs = load_languages()

    # Determine target languages
    if args.language:
        # Validate requested languages
        target_langs = {}
        for lang in args.language:
            if lang in all_langs:
                target_langs[lang] = all_langs[lang]
            else:
                print(
                    f"Warning: Language '{lang}' not found in languages/ directory. Skipping."
                )
    else:
        target_langs = all_langs

    # Load project context if provided
    project_context_content = ""
    if args.context:
        print(f"Loading project context from {args.context}...")
        project_context_content = read_file(args.context)

    # Base context (contains ALL languages so that templates accessing other languages don't break)
    context = {
        "core": data,
        "languages": target_langs,
        "version": "1.0.0",
        "project_context": project_context_content,
    }

    env = setup_jinja()

    # Generation Logic
    # 1. Human Documentation (ALWAYS generated, filtered by context)
    print("Generating human documentation...")
    render_template(
        env, "templates/human-docs.j2", dist / "engineering-standards.md", context
    )

    print("Generating standalone checklist...")
    # Extract checklists from language docs
    lang_checklists = extract_checklists(target_langs)
    checklist_context = context.copy()
    checklist_context["language_checklists"] = lang_checklists

    render_template(
        env, "templates/checklist.j2", dist / "checklist.md", checklist_context
    )

    # 2. If languages are specified, we assume restricted mode: ONLY generate valid prompts for those languages.
    # 3. If NO languages specified, we also generate the Generic Prompt.

    if not args.language:
        print("Generating generic prompt...")
        # Generic LLM Prompt
        render_template(
            env, "templates/llm-prompt.j2", dist / "llm-prompt-generic.txt", context
        )

    # Generate Prompt for each target language
    for lang_name in target_langs:
        print(f"Generating prompt for {lang_name}...")
        lang_context = context.copy()
        lang_context["language"] = lang_name
        render_template(
            env,
            "templates/llm-prompt.j2",
            dist / f"llm-prompt-{lang_name}.txt",
            lang_context,
        )

    print(f"Documentation generation complete in {dist}")


if __name__ == "__main__":
    main()
