# altavida-projects

Monorepo for Altavida's applications.

## Getting Started

### Prerequisites

- Node.js >= 18
- npm >= 9
- An OpenAI API key

### Install OpenAI Codex CLI

```bash
npm install -g @openai/codex
```

Set your API key:

```bash
export OPENAI_API_KEY="sk-..."
```

### Run Codex in this project

```bash
# Interactive REPL
codex

# One-shot question
codex "what does this codebase do?"

# Automated edit with confirmation
codex --approval-mode auto-edit "add input validation to the login form"
```

Project-level configuration lives in [`.codex/config.yaml`](.codex/config.yaml).  
Agent instructions for AI tools live in [`AGENTS.md`](AGENTS.md).
