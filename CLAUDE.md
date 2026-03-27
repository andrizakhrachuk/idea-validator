# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for package management.

```bash
# Install dependencies and set up the project
uv sync

# Run the CLI
uv run idea-validator

# Run parser directly with an idea
python src/idea_validator/parser.py "your business idea here"

# Run with piped input
echo "your business idea" | python src/idea_parser/parser.py
```

## Architecture

`idea-validator` is a CLI tool that takes a free-text business idea and returns structured JSON via OpenAI.

- **Entry point**: `src/idea_validator/__init__.py` — `main()` is registered as the `idea-validator` CLI command in `pyproject.toml`
- **Core logic**: `src/idea_validator/parser.py` — `IdeaStructurer` class wraps the OpenAI chat completions API, sends the idea text to a startup-analyst system prompt, and parses the JSON response into a fixed schema

The output schema includes: `idea_name`, `one_sentence`, `problem`, `target_customer`, `customer_segment`, `value_proposition`, `solution`, `existing_alternatives`, `revenue_model`, `market_type`, `assumptions`, `risks`, `keywords`.

`OPENAI_API_KEY` is read from the environment (`.env` file is gitignored).
