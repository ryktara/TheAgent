# Install on Windows 11

From a clean user profile to "ready". Run every block in **PowerShell** (not as administrator
unless a step says so). Close and reopen PowerShell after step 1 so PATH picks up the new tools.

## 1. Base tools

```powershell
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Python.Python.3.12 -e      # any 3.11+ works
```

Done when: `git --version`, `node --version` (LTS) and `python --version` (3.11+) all print.

## 2. pnpm through corepack

```powershell
corepack enable
corepack prepare pnpm@latest --activate
```

If `corepack enable` fails with an access error, run that one line in an administrator PowerShell.
Done when: `pnpm --version` prints.

## 3. Claude Code and login

```powershell
npm install -g @anthropic-ai/claude-code
claude
```

In the first session run `/login` and sign in with your Claude **subscription** account (Pro or
Max). Foundry is subscription-only: no API key is read, stored or needed.
Done when: `claude` opens a session without a login prompt.

## 4. codebase-memory-mcp (required for builds)

```powershell
powershell -c "irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 | iex"
```

Register it as an MCP server: open `%USERPROFILE%\.claude.json` and merge this into the top level
(keep any existing `mcpServers` entries):

```json
{"mcpServers": {"codebase-memory": {"command": "codebase-memory-mcp", "args": []}}}
```

Done when: `codebase-memory-mcp --version` prints in a new PowerShell and `/mcp` in `claude`
lists `codebase-memory`.

## 5. Foundry plugin

```powershell
claude plugin marketplace add "D:\path\to\foundry"      # a local checkout, or <owner>/<repo>
claude plugin install foundry@foundry-local
```

Done when: `/foundry` appears in the slash-command list of a new `claude` session.

## 6. Setup check

In a `claude` session:

```
/foundry-setup
```

It runs `doctor`, installs pnpm and Playwright browsers when missing, registers the
codebase-memory MCP entry when missing, runs `validate`, runs a 30-second self-test, and prints
`ready`. Done when: the last line is `ready`.

Next: [QUICKSTART.md](QUICKSTART.md).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `running scripts is disabled on this system` (npm, pnpm, wizard .ps1) | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Filename too long` in git, or pnpm install fails deep in `node_modules` | 260-character path limit | `git config --global core.longpaths true`; in an administrator PowerShell: `New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force`; keep app folders short (`D:\apps\cafe`) |
| `initdb failed (3221225478)` / exit `0xC0000006` from the embedded Postgres | initdb cannot run from pnpm paths containing `@` and `+` | The scaffold copies Postgres to `C:\pg17` once. If that drive is not writable, set `$env:FOUNDRY_PG_HOME = "D:\pg17"` (any short path) |
| `EADDRINUSE` on 3000/3001, or Postgres `could not bind` on 54330 | another app or a second Foundry project uses the port | set `WEB_PORT`, `API_PORT`, `FOUNDRY_PG_PORT` in the app's `.env.local` (for example 3010, 3011, 54340); integration tests use `FOUNDRY_PG_PORT - 1` |
| `doctor` FAIL on codebase-memory-mcp | binary not on PATH or MCP entry missing | reopen PowerShell after step 4; check the JSON in `.claude.json`; rerun `/foundry-setup` |
| `claude` says not logged in | session expired | run `/login` again with the subscription account |
| semgrep `missing` warning | no native Windows wheel | optional locally; CI runs it (or use WSL) |
