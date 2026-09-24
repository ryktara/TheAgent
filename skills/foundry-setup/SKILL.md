---
name: foundry-setup
description: Check and set up this machine for Foundry after installing the plugin: doctor, pnpm and Playwright browsers, codebase-memory-mcp registration, validate, a 30-second self-test; prints "ready" or the exact missing item. Run once per machine and again after upgrades.
invocation: user
model: haiku
reads: [evals/briefs/*.md, evals/expected/*.yaml, data/palettes.csv]
writes: [~/.claude.json]
gate: python scripts/foundry.py setup
---

# /foundry-setup — one command, one machine

Subscription-only: the check never looks for an API key; a logged-in Claude Code session is
the only credential. Every step is idempotent, so rerunning after a fix is the normal path.

## Steps

1. **Check.**

   ```
   python scripts/foundry.py setup
   ```

   Prints the doctor table (python 3.11+, node 20+, git, codebase-memory-mcp binary and MCP
   registration, optional semgrep/docker), pnpm, Playwright browsers, validate, and the
   self-test (every golden brief matches its pack, palette contrast passes).
   Done when: the last line is `setup: ready`, or lists the missing items.

2. **Apply the fixes it can make.** When items are missing and the human agrees:

   ```
   python scripts/foundry.py setup --apply
   ```

   Installs pnpm through corepack, Playwright chromium through `npx playwright install`, and
   writes the codebase-memory MCP entry into `~/.claude.json` (it prints the JSON first). Node,
   git, python and the codebase-memory-mcp binary are installed by the human from
   docs/INSTALL-WINDOWS.md or docs/INSTALL-MAC-LINUX.md; the command says which line to run.
   Done when: a rerun of step 1 prints `setup: ready`.

3. **Report** (≤6 lines): the `setup:` line, what `--apply` changed, and the one manual step
   left, if any. Restart Claude Code after an MCP registration.
   Done when: the report is sent.

## Reference

| Item | Checked by | Fix |
|------|-----------|-----|
| python, node, git | `doctor --build` | winget / brew / apt lines in docs/INSTALL-*.md |
| codebase-memory-mcp | binary on PATH + entry in ~/.claude.json | its install.ps1/.sh, then `setup --apply` |
| pnpm | `pnpm` on PATH | `corepack enable && corepack prepare pnpm@latest --activate` |
| Playwright browsers | `ms-playwright` cache folder | `npx playwright install chromium` |
| plugin health | `validate` + self-test | reinstall the plugin, or report the failing line |
