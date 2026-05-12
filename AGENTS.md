# altavida-projects — Agent Instructions

This file is read by OpenAI Codex CLI and other AI coding agents to understand the project.

## Project Overview

`altavida-projects` is the monorepo for Altavida's internal and client-facing applications.

## Development Setup

### Prerequisites
- Node.js >= 18
- npm >= 9
- OpenAI Codex CLI: `npm install -g @openai/codex`

### Environment Variables
Copy `.env.example` to `.env` and fill in the required values before running any service.
`OPENAI_API_KEY` must be set for Codex CLI to function.

## Repository Structure

```
altavida-projects/
├── AGENTS.md          # AI agent instructions (this file)
├── README.md          # Project overview
└── .codex/
    └── config.yaml    # Codex CLI project configuration
```

## Coding Guidelines

- Write clear, minimal code — avoid over-engineering.
- No unnecessary comments; only add one when the WHY is non-obvious.
- Prefer editing existing files over creating new ones.
- Run tests before committing.

## Git Workflow

- Branch naming: `<type>/<short-description>` (e.g. `feat/add-login`, `fix/broken-auth`)
- Commit messages: imperative mood, present tense (e.g. "Add login endpoint")
- Always open a PR; never push directly to `main`.

## Running Codex CLI

```bash
# Interactive session in the project root
codex

# One-shot prompt
codex "explain the authentication flow"

# Full-auto mode (use with care)
codex --approval-mode full-auto "fix the broken test in src/auth"
```
