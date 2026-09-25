# Install on macOS and Linux

Same sequence as [INSTALL-WINDOWS.md](INSTALL-WINDOWS.md); each step's "done when" is identical.

## 1. Base tools

macOS (Homebrew):

```sh
brew install git node python@3.12
```

Debian or Ubuntu:

```sh
sudo apt update && sudo apt install -y git python3 python3-venv curl
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install -y nodejs
```

Done when: `git`, `node` (LTS) and `python3` (3.11+) print versions.

## 2. pnpm

```sh
corepack enable            # prefix with sudo when node lives in /usr
corepack prepare pnpm@latest --activate
```

## 3. Claude Code

```sh
npm install -g @anthropic-ai/claude-code
claude                     # then /login with your subscription account
```

## 4. codebase-memory-mcp

Install with the project's shell installer (see the codebase-memory-mcp README for the current
one-liner), then merge into `~/.claude.json`:

```json
{"mcpServers": {"codebase-memory": {"command": "codebase-memory-mcp", "args": []}}}
```

## 5. Plugin and setup check

```sh
claude plugin marketplace add ryktara/TheAgent     # or a local checkout: /path/to/foundry
claude plugin install foundry@theagent
```

Then in `claude`: `/foundry-setup`. Done when the last line starts with `setup: ready`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `EACCES` on `npm install -g` | `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH |
| Playwright browsers fail on Linux | `pnpm exec playwright install --with-deps` |
| Embedded Postgres cannot write its cache | `export FOUNDRY_PG_HOME=/some/writable/pg17` (default `~/.foundry-pg/pg17`) |
| Port in use | set `WEB_PORT`, `API_PORT`, `FOUNDRY_PG_PORT` in `.env.local` |
| Wizard `.sh` not executable | `chmod +x .foundry/wizard/<slug>.sh` |
