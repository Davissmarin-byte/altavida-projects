# altavida-projects

Monorepo for Altavida's applications.

## Getting Started

### Prerequisites

- Node.js >= 18
- npm >= 9
- An OpenAI API key
- A Firecrawl API key

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

### Install Firecrawl CLI

```bash
npx -y firecrawl-cli@latest init --all --browser
```

Set your API key in `.env`:

```bash
FIRECRAWL_API_KEY=fc-...
```

### Run Firecrawl in this project

```bash
# Search the web
firecrawl search "your query"

# Scrape a URL
firecrawl scrape "https://example.com"

# Interact with a live page
firecrawl interact "https://example.com"

# Verify installation
firecrawl --status
```

Firecrawl configuration lives in [`.firecrawl/`](.firecrawl/).
