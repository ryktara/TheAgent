---
name: release
description: Release the app (phase 14): generate CHANGELOG from ticket commits, deploy config per ADR 0007, runbook, smoke script and user docs with release-skeleton, review them, then pass gate release against a locally started production build.
invocation: user
model: sonnet
reads: [.foundry/adr/0007-deployment-environments.md, .foundry/screens/*.md, data/copy.csv, .foundry/build.yaml, .foundry/wizard/*.md, package.json]
writes: [CHANGELOG.md, apps/*/Dockerfile, compose.prod.yml, Caddyfile, fly.toml, runbook.md, scripts/smoke.mjs, user-docs/*.md, .foundry/handoff.md]
gate: python scripts/foundry.py gate release
---

# /release — orchestrator, phase 14

Ship what the tickets built: every artefact is generated from the repo and the `.foundry/`
specs, then reviewed once by you, then proven by a smoke test on a production build.

## Steps

1. **Preconditions.** `python scripts/foundry.py status`: every feature ticket done or
   consciously deferred (list the deferred ones in the report); `wizard status` shows which
   provider wizards are still pending (they ship stubbed, flagged off).
   Regulated pack (`regulated: true`, e.g. trading-app): the regulator-licence wizard must be done and a
   human must have typed `python scripts/foundry.py release confirm --by <name>`; never run it yourself.
   Done when: the ticket list and pending wizards are known.

2. **Generate.**

   ```
   python scripts/foundry.py release-skeleton
   ```

   Writes CHANGELOG.md (from `feat|fix|chore(T-xxx)` commits), `apps/api/Dockerfile`,
   `apps/web/Dockerfile`, `compose.prod.yml` + `Caddyfile` (VPS) or `fly.toml` (Fly) per ADR
   0007, `runbook.md`, `scripts/smoke.mjs`, `user-docs/cashier-quick-start.{en,ar}.md` and
   `user-docs/manager-guide.en.md` from the screen specs and copy.csv.
   Done when: the command lists the files it wrote.

3. **Review the generated text.** Group CHANGELOG entries by release (`## vX.Y.Z` with the
   date), remove internal chores, name breaking changes. Check the runbook's env table against
   `.env.example` and the wizards. Read both user docs as the persona would; fix copy that is
   wrong for the decided region. Never edit the Dockerfiles for style alone.
   Done when: CHANGELOG has one versioned section, runbook env table equals `.env.example`
   keys, user docs read as instructions.

4. **Production build + smoke.**

   ```
   python scripts/foundry.py gate release
   ```

   The gate checks every file, runs `pnpm run build`, starts api and web from the build on
   ports 3101/3100, and runs `scripts/smoke.mjs` (health, device enrol + whoami, table map,
   home). Fix the build or the app, never the smoke assertions, until it passes.
   Done when: `gate release: pass` with `smoke: N/N passed`.

5. **Tag and hand off.**

   ```
   git add -A && git commit -m "release: vX.Y.Z" && git tag vX.Y.Z
   python scripts/foundry.py handoff write --next-command "deploy per runbook.md" --note "released vX.Y.Z"
   ```

   Done when: the tag exists and `handoff.md` frontmatter has `next_command`.

6. **Report** (≤10 lines): version, tickets included, deferred tickets, pending wizards, deploy
   mode, smoke result, the deploy command from the runbook.
   Done when: the report is sent.

## Reference

| File | Source of truth |
|------|-----------------|
| CHANGELOG.md | `git log` ticket commits |
| Dockerfiles, compose/Caddy or fly.toml | ADR 0007 deploy mode, package names from package.json |
| runbook.md | start/stop, backup/restore, rotate device tokens, reindex, rollback, smoke |
| scripts/smoke.mjs | `/health`, `POST /devices/enrol` + `/whoami`, `/table-map`, `/` |
| user-docs/ | `.foundry/screens/*.md` states + `data/copy.csv` actions (en, ar) |

`gate release` uses `NODE_ENV=production`, `WEB_PORT=3100`, `API_PORT=3101`; the api runs the
TypeScript sources with tsx because workspace packages export `.ts` (runbook notes the trade-off).
