# altavida-projects — Agent Instructions

This file is read by OpenAI Codex CLI and other AI coding agents to understand the project.

## Project Overview

`altavida-projects` is the monorepo for Altavida's internal and client-facing applications.

## Development Setup

### Prerequisites
- Node.js >= 18
- npm >= 9
- OpenAI Codex CLI: `npm install -g @openai/codex`
- Firecrawl CLI: `npx -y firecrawl-cli@latest init --all --browser`

### Environment Variables
Copy `.env.example` to `.env` and fill in the required values before running any service.
`OPENAI_API_KEY` must be set for Codex CLI to function.
`FIRECRAWL_API_KEY` must be set for Firecrawl to function.

## Repository Structure

```
altavida-projects/
├── AGENTS.md          # AI agent instructions (this file)
├── README.md          # Project overview
├── .codex/
│   └── config.yaml    # Codex CLI project configuration
└── .firecrawl/        # Firecrawl output and configuration
```

## Firecrawl Usage

Firecrawl provides web search, scraping, and interaction capabilities. Use it when you need live web data.

```bash
# Search the web
firecrawl search "your query"

# Scrape a URL
firecrawl scrape "https://example.com" -o .firecrawl/output.md

# Interact with a live page (clicks, forms, login)
firecrawl interact "https://example.com"

# Ask Firecrawl about itself or diagnose a failed job
firecrawl ask "how does X work?"

# Check status
firecrawl --status
```

Default workflow:
1. Start with `firecrawl search` to discover relevant pages.
2. Use `firecrawl scrape` once you have a target URL.
3. Use `firecrawl interact` only when the page requires clicks, forms, or login.
4. If a call fails, run `firecrawl ask` with the failed `jobId` instead of guessing.

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
