"""Foundry phases 9-10: threat model, compliance, tickets.

Imported by foundry.py; Python 3.11+ stdlib only. Skeleton outputs pass their gates unmodified.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

import foundry as F

DATA = F.ROOT / "data"
# Generic money tokens; a pack's `vocabulary.money_tokens` (schema 2.0) replaces them for its jobs.
MONEY_TOKENS = ("payment", "refund", "void", "discount", "tender", "settle")
SEVERITY = {"low": 1, "medium": 2, "high": 3}
BOUNDARY_TYPE = {"internet<->edge": "internet-edge", "edge<->api": "edge-api", "api<->db": "api-db", "api<->payment-provider": "api-third-party",
                 "api<->delivery-platform": "webhook-inbound", "terminal<->local-print-bridge": "terminal-print-bridge", "device<->offline-store": "device-offline-store",
                 "device<->local": "device-local", "admin": "admin"}
DOD = ["typecheck", "unit", "integration", "e2e-smoke", "a11y-axe", "lint", "semgrep", "screenshot", "spec-review", "detect_changes_risk<=medium"]


def _rows(name: str) -> list[dict]:
    return F.data_rows(name)


def _money_tokens(pack: dict | None = None) -> tuple[str, ...]:
    pack = pack if pack is not None else F.ACTIVE_PACK.get("pack") or {}
    return tuple(str(t) for t in (F.vocab(pack, "money_tokens") or MONEY_TOKENS))


def _money_job(job: str, pack: dict | None = None) -> bool:
    return any(t in job for t in _money_tokens(pack))


def _fm(path: Path) -> tuple[dict, str]:
    fm_text, _, body = F.split_frontmatter(path.read_text(encoding="utf-8"))
    return F.parse_yaml(fm_text), body


def _region(ledger: dict, pack: dict) -> str:
    for d in ledger.get("decisions", []):
        if d.get("maps_to") == "region.country" or d["id"] == "region":
            return str(d["value"])
    return next(iter(pack.get("regional") or {"AE": {}}))


def _decision(ledger: dict, qid: str) -> Any:
    d = next((d for d in ledger.get("decisions", []) if d["id"] == qid), None)
    return d["value"] if d else None


# ----------------------------------------------------------------------------- applicability
def _conditions(pack: dict, ledger: dict, arch_fm: dict, spec: dict) -> set[str]:
    conds = {"always", "web", "backoffice", "staff_pin", "device_auth", "manager_override", "shifts", "money", "integrations"}
    region = _region(ledger, pack)
    conds.add(f"region={region}")
    if region in ("AE", "SA", "PK", "EG"):
        conds.add("region in (AE,SA)") if region in ("AE", "SA") else None
        conds.add("fiscal")
    pay = _decision(ledger, "payments")
    if pay and pay != "cash-only":
        conds.add("payments=card"); conds.add("payments"); conds.add("webhooks")
    if _decision(ledger, "offline") is True or str((pack.get("nfr_defaults") or {}).get("offline")) == "required":
        conds.add("offline=true")
    if str(_decision(ledger, "branches")) == "multi":
        conds.add("multi-branch")
    if _decision(ledger, "delivery") is True:
        conds.add("delivery"); conds.add("webhooks")
    if any("print" in k or "print" in str(v) for k, v in (pack.get("stack_default") or {}).items()):
        conds.add("printing")
    if "room-charge" in (pack.get("should_have") or []):
        conds.add("room_charge")
    if "loyalty" in (pack.get("must_have") or []) + (pack.get("should_have") or []):
        conds.add("loyalty")
    if any(p.startswith("/webhooks/") for p in (spec.get("paths") or {})):
        conds.add("webhooks")
    conds.add("subagents")
    conds.add("scanner")
    return conds


def applicable_controls(pack: dict, ledger: dict, arch_fm: dict, spec: dict) -> list[dict]:
    conds = _conditions(pack, ledger, arch_fm, spec)
    out = []
    for r in _rows("security-controls"):
        if r["applies_when"] in conds:
            out.append(r)
    return out


# ----------------------------------------------------------------------------- phase 9: threats
def _money_op(op: dict) -> bool:
    xf = op.get("x-foundry") or {}
    job = str(xf.get("job", ""))
    return _money_job(job) or any(t in str(op.get("operationId", "")) for t in ("payment", "refund"))


def threat_skeleton(pack: dict, ledger: dict, arch_fm: dict, spec: dict, prd_sections: dict) -> tuple[str, dict]:
    ctrl_by_id = {r["id"]: r for r in _rows("security-controls")}
    applicable = applicable_controls(pack, ledger, arch_fm, spec)
    app_ids = {r["id"] for r in applicable}
    patterns = _rows("threat-patterns")
    boundaries = list(arch_fm.get("trust_boundaries") or [])
    exposure = {"internet-edge": 3, "webhook-inbound": 3, "edge-api": 3, "api-third-party": 2, "device-local": 2, "device-offline-store": 2, "terminal-print-bridge": 1, "api-db": 1, "admin": 2}
    out = ["---", f"pack: {F._yq(pack['slug'])}", f"decisions_hash: {F._yq(F.decisions_hash(ledger))}", f"boundaries: {F._yq(boundaries)}", "---", "",
           f"# Threat model — {pack['name']}", "", "STRIDE per trust boundary from data/threat-patterns.csv, controls from data/security-controls.csv",
           "filtered by this project's decisions. Operation authz matrix from openapi.yaml `x-foundry`.", ""]
    risks: list[tuple[int, str, str, str, str]] = []
    for b in boundaries + ["admin"]:
        btype = BOUNDARY_TYPE.get(b, b)
        rows = [p for p in patterns if p["boundary_type"] == btype]
        out += [f"## Boundary: {b}", "", "| Id | STRIDE | Threat | Controls | Severity |", "|----|--------|--------|----------|----------|"]
        for p in rows:
            ctrls = [c for c in p["typical_mitigation_control_ids"].split(";") if c]
            shown = ", ".join(f"`{c}`" for c in ctrls)
            out.append(f"| {p['id']} | {p['stride']} | {p['threat']} | {shown} | {p['severity_default']} |")
            score = SEVERITY.get(p["severity_default"], 1) * exposure.get(btype, 1)
            risks.append((score, p["id"], b, p["threat"], shown))
        out.append("")
    out += ["## Operation authz matrix", "", "| operationId | Job | Personas | Authz | Audit | Idempotent | Money | Controls |", "|-------------|-----|----------|-------|-------|------------|-------|----------|"]
    money_ctrls = [c["id"] for c in applicable if c["family"] in ("access", "business-logic", "error-log") and c["id"] in ("SEC-ACC-01", "SEC-ACC-02", "SEC-ACC-04", "SEC-BL-01", "SEC-BL-03", "SEC-BL-04", "SEC-BL-05", "SEC-BL-06", "SEC-LOG-02", "SEC-SESS-07", "SEC-API-01")]
    base_ctrls = ["SEC-ACC-01", "SEC-ACC-02", "SEC-IN-01", "SEC-LOG-01"]
    for path, methods in (spec.get("paths") or {}).items():
        for m, op in (methods or {}).items():
            if m not in ("get", "post", "patch", "put", "delete"):
                continue
            xf = op.get("x-foundry") or {}
            money = _money_op(op)
            ctrls = list(base_ctrls) + (money_ctrls if money else []) + (["SEC-API-04", "SEC-CRY-06"] if str(path).startswith("/webhooks") else []) + (["SEC-API-11", "SEC-OFF-01"] if str(path).startswith("/sync") else [])
            ctrls = [c for c in dict.fromkeys(ctrls) if c in app_ids or c in base_ctrls]
            out.append(f"| `{op.get('operationId')}` | {xf.get('job', '-')} | {', '.join(map(str, xf.get('personas') or []))} | {xf.get('authz', '-')} | {'yes' if xf.get('audit') else 'no'} | {'yes' if xf.get('idempotent') else 'no'} | {'yes' if money else 'no'} | {', '.join(f'`{c}`' for c in ctrls)} |")
    risks.sort(key=lambda r: (-r[0], r[1]))
    out += ["", "## Top 10 risks", "", "| Rank | Score | Boundary | Threat | Controls |", "|-----:|------:|----------|--------|----------|"]
    for i, (score, pid, b, threat, shown) in enumerate(risks[:10], 1):
        out.append(f"| {i} | {score} | {b} | {threat} ({pid}) | {shown} |")
    out += ["", "## Abuse cases", "", "<!-- model: write one table per risky workflow (payment, refund, offline sync): actor, goal, path, control that stops it, residual risk -->", "",
            "| Workflow | Actor | Goal | Path | Stopped by | Residual |", "|----------|-------|------|------|------------|----------|",
            f"| payment | {(pack.get('personas') or ['operator'])[0]} | pocket cash by marking card paid | mark tender card without terminal approval | `SEC-PAY-02` approval code required; `SEC-PAY-05` nightly reconciliation | manual approval-code entry offline, audited |",
            "| refund | manager | refund to own card | refund to a tender not on the order | `SEC-PAY-04` refund via provider token of the original payment; `SEC-BL-04` cap | cash refund fallback needs owner PIN |",
            "| offline sync | device | replay events to duplicate orders | resend outbox with reused seq | `SEC-API-11` monotonic seq; `SEC-BL-11` client UUID dedupe | none beyond audit |", "",
            "## Blocking findings", "", "- none", ""]
    region = _region(ledger, pack)
    reg = (pack.get("regional") or {}).get(region) or {}
    pay = _decision(ledger, "payments")
    if not pay or pay == "cash-only":
        scope, reason = "na", "no card payments in scope"
    else:
        scope, reason = "SAQ-A", f"provider {pay}: hosted page or redirect online, semi-integrated terminal in person; card fields never on merchant pages (SEC-PAY-01, SEC-PAY-02)"
    prd_controls = sorted(set(re.findall(r"`(C-[A-Z]+-\d+)`", prd_sections.get("8", ""))))
    compliance = {"pack": pack["slug"], "region": region, "decisions_hash": F.decisions_hash(ledger), "pci_scope": scope, "pci_reason": reason,
                  "controls": [{"id": c, "source": "pack compliance.md", "status": "planned", "evidence": None, "owner": None} for c in prd_controls]
                  + [{"id": c["id"], "source": c["source"], "status": "planned", "evidence": None, "owner": None} for c in applicable]}
    return "\n".join(out), compliance


def _dump_compliance(c: dict) -> str:
    out = [f"pack: {F._yq(c['pack'])}", f"region: {F._yq(c['region'])}", f"decisions_hash: {F._yq(c['decisions_hash'])}", f"pci_scope: {F._yq(c['pci_scope'])}", f"pci_reason: {F._yq(c['pci_reason'])}", "controls:"]
    out += [f"  - {F._yq(x)}" for x in c["controls"]]
    return "\n".join(out) + "\n"


def run_threat_skeleton(project: Path, root: Path) -> int:
    import foundry_phases as P
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    arch_fm, _ = _fm(project / ".foundry" / "architecture.md")
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    md, comp = threat_skeleton(pack, ledger, arch_fm, spec, P._read_prd_sections(project))
    (project / ".foundry" / "threats.md").write_text(md, encoding="utf-8", newline="\n")
    (project / ".foundry" / "compliance.yaml").write_text(_dump_compliance(comp), encoding="utf-8", newline="\n")
    plan = ["# Compliance evidence plan", "", "| Control | Source | Evidence by | Status |", "|---------|--------|-------------|--------|"]
    ctrl_by_id = {r["id"]: r for r in _rows("security-controls")}
    for c in comp["controls"]:
        v = ctrl_by_id.get(c["id"], {}).get("verify", "review")
        plan.append(f"| `{c['id']}` | {c['source']} | {v} | {c['status']} |")
    (project / ".foundry" / "compliance-evidence-plan.md").write_text("\n".join(plan) + "\n", encoding="utf-8", newline="\n")
    print(f"threat-skeleton: {len(arch_fm.get('trust_boundaries') or [])} boundaries, {len(comp['controls'])} controls, pci_scope {comp['pci_scope']} -> .foundry/threats.md, compliance.yaml, compliance-evidence-plan.md")
    return 0


def gate_security(project: Path, root: Path) -> list[str]:
    import foundry_design as D
    import foundry_phases as P
    errs = D.gate_screens(project, root)
    if errs:
        return errs
    tp = project / ".foundry" / "threats.md"
    cp = project / ".foundry" / "compliance.yaml"
    if not tp.exists() or not cp.exists():
        return [f"{tp if not tp.exists() else cp} missing"]
    fm, body = _fm(tp)
    boundaries = fm.get("boundaries") or []
    for b in boundaries:
        sec = body.split(f"## Boundary: {b}", 1)[1].split("\n## ", 1)[0] if f"## Boundary: {b}" in body else ""
        n = len(re.findall(r"^\| TP-", sec, re.M))
        if n < 4:
            errs.append(f"boundary {b} has {n} STRIDE rows; need 4")
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    matrix = body.split("## Operation authz matrix", 1)[1].split("\n## ", 1)[0] if "## Operation authz matrix" in body else ""
    ctrl_by_id = {r["id"]: r for r in _rows("security-controls")}
    for path, methods in (spec.get("paths") or {}).items():
        for m, op in (methods or {}).items():
            if m not in ("get", "post", "patch", "put", "delete"):
                continue
            oid = op.get("operationId")
            row = re.search(rf"^\| `{re.escape(str(oid))}` \|(.*)$", matrix, re.M)
            if not row:
                errs.append(f"operation {oid} has no authz row")
                continue
            if _money_op(op):
                fams = {ctrl_by_id[c]["family"] for c in re.findall(r"`(SEC-[A-Z]+-\d+)`", row.group(1)) if c in ctrl_by_id}
                for need in ("access", "business-logic", "error-log"):
                    if need not in fams:
                        errs.append(f"money operation {oid} lacks a {need} control")
                authz = (op.get("x-foundry") or {}).get("authz", "").lower()
                if "any authenticated" in authz:
                    errs.append(f"money operation {oid} authz is 'any authenticated' (blocking)")
    comp = F.parse_yaml(cp.read_text(encoding="utf-8"))
    if not comp.get("pci_scope"):
        errs.append("compliance.yaml: pci_scope missing")
    comp_ids = {c["id"] for c in comp.get("controls") or []}
    for cid in set(re.findall(r"`(C-[A-Z]+-\d+)`", P._read_prd_sections(project).get("8", ""))):
        if cid not in comp_ids:
            errs.append(f"PRD §8 control {cid} not in compliance.yaml")
    for line in body.splitlines():
        if line.startswith("| TP-") and "| high |" in line and "`SEC-" not in line:
            errs.append(f"high severity threat without control: {line[:60]}")
    return errs


# ----------------------------------------------------------------------------- phase 10: tickets
def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _ticket_md(t: dict) -> str:
    fm = ["---", f"id: {F._yq(t['id'])}", f"title: {F._yq(t['title'])}", f"type: {F._yq(t['type'])}", f"blockedBy: {F._yq(t['blockedBy'])}", f"jobs: {F._yq(t['jobs'])}",
          f"screens: {F._yq(t['screens'])}", f"operations: {F._yq(t['operations'])}", f"adrs: {F._yq(t['adrs'])}", f"controls: {F._yq(t['controls'])}", f"estimate: {F._yq(t['estimate'])}",
          f"files_likely_touched: {F._yq(t['files'])}", "acceptance_tests:"] + [f"  - {F._yq(a)}" for a in t["tests"]] + [f"dod: {F._yq(DOD)}", "---", ""]
    body = [f"# {t['id']} — {t['title']}", "", "## Slice", "", t["slice"], "", "## Acceptance tests", ""] + [f"{i}. {a}" for i, a in enumerate(t["tests"], 1)] + ["", "## Definition of done", ""] + [f"- {d}" for d in DOD] + [""]
    return "\n".join(fm + body)


def _entity_order(domain: dict) -> list[str]:
    """Topological order of entities by *_id references (referenced first)."""
    names = [e["name"] for e in domain["entities"]]
    snake = {re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower(): n for n in names}
    deps: dict[str, set[str]] = {n: set() for n in names}
    for e in domain["entities"]:
        for f in e["fields"]:
            if f.endswith("_id") and snake.get(f[:-3]) and snake[f[:-3]] != e["name"]:
                deps[e["name"]].add(snake[f[:-3]])
    order: list[str] = []
    seen: set[str] = set()
    def visit(n: str, stack: set[str]):
        if n in seen or n in stack:
            return
        stack.add(n)
        for d in sorted(deps[n]):
            visit(d, stack)
        stack.discard(n)
        seen.add(n)
        order.append(n)
    for n in names:
        visit(n, set())
    return order


SCAFFOLD_TITLES = {'auth': 'Auth: device enrolment, staff sign-in, step-up approval', 'tenancy': 'Tenancy and branch scoping with RLS', 'schema': 'Schema, migrations, seed data', 'tokens': 'Design tokens, shell layout, RTL switch, component base', 'offline': 'Offline store and sync outbox'}


def _title(pack: dict, key: str) -> str:
    """Pack 2.0 `vocabulary.scaffold_ticket_titles.<key>` for T-001..T-005; generic fallback."""
    return str(F.vocab(pack, f"scaffold_ticket_titles.{key}", SCAFFOLD_TITLES[key]))


def tickets_skeleton(project: Path, root: Path) -> list[dict]:
    import foundry_phases as P
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    P.apply_pack_contexts(pack)
    offline_ctx = P.OFFLINE_CONTEXTS  # generalisation fix (P10): no offline ticket or offline acceptance test for offline-forbidden packs
    ledger = F.load_ledger(project, sel["chosen"])
    domain = F.parse_yaml((project / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    arch_fm, _ = _fm(project / ".foundry" / "architecture.md")
    comp = F.parse_yaml((project / ".foundry" / "compliance.yaml").read_text(encoding="utf-8")) if (project / ".foundry" / "compliance.yaml").exists() else {"controls": []}
    jobs_in_scope, _ = P._in_scope_ids(project, pack)
    job_by_id = {j["id"]: j for j in pack.get("jobs") or []}
    stack_id = arch_fm.get("stack_id", "nextjs-pwa")
    stacks = {r["stack_id"]: r for r in _rows("stacks")}
    sd = pack.get("stack_default") or {}
    api_stack = stacks.get(sd.get("api", "hono-node"), {})
    web_stack = stacks.get(stack_id, {})
    entity_ctx = {e["name"]: e["owned_by"] for e in domain["entities"]}
    inv_by_entity = {e["name"]: e["invariants"] for e in domain["entities"]}
    ops_by_job: dict[str, list[str]] = {}
    public_ops: set[str] = set()
    for path, methods in (spec.get("paths") or {}).items():
        for m, op in (methods or {}).items():
            if m not in ("get", "post", "patch", "put", "delete"):
                continue
            job = (op.get("x-foundry") or {}).get("job")
            ops_by_job.setdefault(job, []).append(op["operationId"])
            if not str(path).startswith("/admin"):
                public_ops.add(op["operationId"])
    screen_files = {p.stem: p for p in (project / ".foundry" / "screens").glob("*.md")} if (project / ".foundry" / "screens").exists() else {}
    screens_by_job: dict[str, list[str]] = {}
    for sid, p in screen_files.items():
        fm, _ = _fm(p)
        for j in fm.get("jobs") or []:
            screens_by_job.setdefault(j, []).append(sid)
    tickets: list[dict] = []
    def T(idn, title, ttype, blocked, jobs=(), screens=(), ops=(), adrs=(), controls=(), est="M", files=(), tests=(), slice_="") -> dict:
        t = {"id": idn, "title": title, "type": ttype, "blockedBy": list(blocked), "jobs": list(jobs), "screens": list(screens), "operations": list(ops), "adrs": list(adrs),
             "controls": list(controls), "estimate": est, "files": list(files), "tests": list(tests), "slice": slice_}
        tickets.append(t)
        return t
    T("T-000", "Repo scaffold, toolchain, CI", "scaffold", [], adrs=["0001"], controls=["SEC-SC-01", "SEC-SC-06", "SEC-CFG-05"], est="M",
      files=["package.json", "apps/web/", "apps/api/", "packages/db/", ".github/workflows/ci.yml", "docker-compose.yml", ".env.example"],
      tests=["Given a clean clone, When `npm ci && npm run build` runs, Then it exits 0 on Windows and Linux",
             f"Given the scaffold, When `{web_stack.get('typecheck_cmd', 'npx tsc --noEmit')}` and `{api_stack.get('test_cmd', 'npx vitest run')}` run, Then both exit 0 with zero tests failing",
             "Given CI, When a PR opens, Then typecheck, lint, unit, a11y and semgrep jobs run and are required",
             "Given docker compose up, When the api starts, Then /health returns ok and the db accepts connections"],
      slice_=f"Monorepo from stacks.csv: web `{web_stack.get('scaffold_cmd', '')}`; api `{api_stack.get('scaffold_cmd', '')}`; prisma init; lint, typecheck, vitest, playwright+axe wired; docker compose with postgres; .env.example listing every variable; CI workflow. No CODEOWNERS.")
    T("T-001", _title(pack, "auth"), "feature", ["T-000"], adrs=["0002"], ops=[o for o in ops_by_job.get("read", []) if o.startswith("staff") or o.startswith("role")],
      controls=["SEC-AUTH-05", "SEC-AUTH-06", "SEC-AUTH-11", "SEC-SESS-01", "SEC-SESS-07", "SEC-ACC-01"], est="L",
      files=["apps/api/src/people/auth.ts", "apps/api/src/people/devices.ts", "apps/web/app/(auth)/pin/page.tsx", "packages/db/prisma/schema.prisma"],
      tests=["Given an enrolled device token, When a request carries it, Then branch scope is set and unknown tokens get 401",
             "Given a staff PIN, When 3 wrong entries occur, Then the PIN locks for 60 s and an audit event is written",
             "Given a void over threshold, When a manager enters a PIN, Then the approver id is stored on the audit event",
             "Given a PIN verified offline, When sync runs, Then the event is marked pending-audit"],
      slice_="Device enrolment endpoint and token middleware; Argon2id PIN hashing with local hash cache; manager override modal wired to audit; sessions table.")
    T("T-002", _title(pack, "tenancy"), "feature", ["T-001"], adrs=["0003"], controls=["SEC-ACC-02", "SEC-ACC-05", "SEC-ACC-08"], est="M",
      files=["packages/db/prisma/migrations/", "apps/api/src/people/branch.ts", "apps/api/src/middleware/scope.ts"],
      tests=["Given two branches, When a device of branch A lists orders, Then only branch A rows return",
             "Given an owner session, When the branch switcher selects B, Then reads and writes target B",
             "Given the app db role, When it attempts to bypass RLS, Then Postgres denies"],
      slice_="branch_id on every operational table; RLS policies; scope middleware; owner branch switcher.")
    T("T-003", _title(pack, "schema"), "feature", ["T-002"], adrs=["0004"], controls=["SEC-DATA-07", "SEC-IN-04"], est="M",
      files=["packages/db/prisma/schema.prisma", "packages/db/prisma/migrations/", "packages/db/seed.ts"],
      tests=["Given prisma/schema.prisma, When `npx prisma validate` and `migrate dev` run, Then both succeed on an empty database",
             f"Given the seed, When it runs twice, Then it is idempotent and creates one branch, roles, a {F.term(pack, 'catalog', 'catalog')} and tax rules for the region",
             "Given the audit table, When an UPDATE is attempted with the app role, Then it is denied"],
      slice_="Migrations from the generated schema with check constraints from invariants; seed for the decided region; append-only grants on audit and receipts.")
    T("T-004", _title(pack, "tokens"), "feature", ["T-000"], adrs=["0009"], controls=["SEC-API-08"], est="M",
      files=["apps/web/app/layout.tsx", "apps/web/styles/tokens.css", "packages/ui/", "design-system/"],
      tests=["Given tailwind.tokens.css, When the shell renders, Then computed styles use the token variables and tabular numerals",
             "Given the language switch, When ar is selected, Then dir=rtl is set, layout mirrors and the numpad stays LTR",
             "Given the axe scan, When the shell renders in both directions, Then zero serious violations"],
      slice_="Tokens applied; app shell with nav pattern from MASTER.md; RTL switch; base components (button, input, dialog, toast, numpad, banner-offline) from components.csv.")
    if offline_ctx:
      T("T-005", _title(pack, "offline"), "feature", ["T-003", "T-004"], adrs=["0005"], ops=["sync_push", "sync_pull"], controls=["SEC-API-11", "SEC-OFF-01", "SEC-OFF-03", "SEC-BL-08", "SEC-BL-11"], est="L",
      files=["apps/web/src/offline/store.ts", "apps/web/src/offline/outbox.ts", "apps/api/src/sync/push.ts", "apps/api/src/sync/pull.ts"],
      tests=["Given the device offline, When an order is created, Then it is stored locally with a client UUID and a monotonic seq",
             "Given 500 queued events, When the connection returns, Then the queue drains within 60 s and every event is acked once",
             "Given the same event replayed, When push runs, Then the server returns the first result and creates no duplicate",
             "Given two devices editing one order, When both sync, Then last-writer-wins per field and payments append"],
      slice_="pglite store, outbox, push/pull endpoints with seq validation, receipt block allocation, conflict rules from ADR 0005.")
    # feature tickets per must-have job in entity order
    order = _entity_order(domain)
    job_index = {j["id"]: i for i, j in enumerate(pack.get("jobs") or [])}

    def job_rank(jid: str) -> tuple[int, int, int]:
        j = job_by_id.get(jid, {})
        ent = j.get("entity")
        return (int(j.get("priority", 5)), order.index(ent) if ent in order else len(order), job_index.get(jid, 999))
    # jobs[].merge_into (pack 1.8): a merged job rides on its target's ticket (screens, operations, tests folded in)
    merged: dict[str, list[str]] = {}
    for jid, j in job_by_id.items():
        tgt = j.get("merge_into")
        if tgt and tgt in job_by_id and jid in jobs_in_scope:
            merged.setdefault(tgt, []).append(jid)
    absorbed = {m for ms in merged.values() for m in ms}
    must_jobs = [j for j in jobs_in_scope if job_by_id.get(j, {}).get("must") and j not in absorbed]
    should_jobs = [j for j in jobs_in_scope if j in job_by_id and not job_by_id[j].get("must") and j not in absorbed]
    n = 6
    job_ticket: dict[str, str] = {}
    for jid in sorted(must_jobs, key=job_rank):
        j = job_by_id[jid]
        ent = j.get("entity") if j.get("entity") != "none" else None
        ops = ops_by_job.get(jid, [])
        scr = screens_by_job.get(jid, [])
        ctx = entity_ctx.get(ent, "ordering") if ent else "reporting"
        invs = inv_by_entity.get(ent, [])[:2] if ent else []
        money = _money_job(jid, pack)
        ctrls = (["SEC-BL-01", "SEC-LOG-02", "SEC-ACC-01"] + (["SEC-SESS-07", "SEC-API-01", "SEC-BL-05"] if money else []))[:6]
        tests = [f"Given the {scr[0] if scr else jid} screen, When {jid.replace('-', ' ')} completes, Then the {ent or 'result'} state and totals match the domain invariants" if ent else f"Given the {scr[0] if scr else jid} screen, When {jid.replace('-', ' ')} runs, Then the result matches the PRD job",
                 f"Given offline mode, When {jid.replace('-', ' ')} runs, Then the write lands in the outbox and syncs without duplicates" if ctx in offline_ctx else f"Given a {(pack.get('personas') or ['operator'])[0]} role, When {jid.replace('-', ' ')} is attempted without permission, Then the api returns 403 and logs authz.denied",
                 f"Given the screen in ar, When it renders, Then layout mirrors and the axe scan reports zero serious violations"]
        for inv in invs:
            tests.append(f"Given any sequence of actions, When the invariant '{inv[:90]}' is checked, Then it holds")
        blocked = ["T-005" if offline_ctx and ctx in (offline_ctx | {"payments"}) else "T-003", "T-004"]
        for dep_ent in (order[: order.index(ent)] if ent in order else []):
            for other, tid in job_ticket.items():
                if job_by_id[other].get("entity") == dep_ent and tid not in blocked:
                    blocked.append(tid)
        blocked = blocked[:4]
        tid = f"T-{n:03d}"
        T(tid, f"{jid.replace('-', ' ').capitalize()} ({', '.join(scr) or 'api only'})", "feature", blocked, jobs=[jid], screens=scr, ops=ops, adrs=["0002"] if money else [],
          controls=ctrls, est="L" if money or len(ops) > 3 else "M",
          files=[f"apps/api/src/{ctx}/{_slug(jid)}.ts", f"apps/api/src/{ctx}/{_slug(jid)}.test.ts"] + [f"apps/web/app/{s}/page.tsx" for s in scr] + ([f"packages/db/prisma/schema.prisma"] if ent else []),
          tests=tests, slice_=f"Vertical slice for job `{jid}`: operations {', '.join(ops) or 'none'}; screens {', '.join(scr) or 'none'}; copy from copy.csv; a11y scan; screenshot.")
        job_ticket[jid] = tid
        for mj in merged.get(jid, []):
            mt = tickets[-1]
            mt["jobs"].append(mj)
            mt["screens"] += [s for s in screens_by_job.get(mj, []) if s not in mt["screens"]]
            mt["operations"] += [o for o in ops_by_job.get(mj, []) if o not in mt["operations"]]
            mt["tests"].append(f"Given the merged job {mj}, When {mj.replace('-', ' ')} runs on the same screen, Then its operations respond and its screen states render")
            mt["title"] = mt["title"].split(" (", 1)[0] + f" + {mj.replace('-', ' ')} ({', '.join(mt['screens']) or 'api only'})"
            mt["slice"] += f" Merged job `{mj}`: operations {', '.join(ops_by_job.get(mj, [])) or 'none'}."
            job_ticket[mj] = tid
        n += 1
    # should-have jobs merge into the nearest must ticket when count would exceed 60; otherwise own ticket
    for jid in sorted(should_jobs, key=job_rank):
        j = job_by_id[jid]
        scr = screens_by_job.get(jid, [])
        ops = ops_by_job.get(jid, [])
        parent = next((t for t in reversed(tickets) if t["type"] == "feature" and t["jobs"] and job_by_id.get(t["jobs"][0], {}).get("entity") == j.get("entity")), None) if j.get("entity") else None
        if parent and n + len(should_jobs) > 55:
            parent["jobs"].append(jid); parent["screens"] += [s for s in scr if s not in parent["screens"]]; parent["operations"] += ops
            parent["tests"].append(f"Given the should-have job {jid}, When enabled, Then its operations respond and its screen states render")
            continue
        tid = f"T-{n:03d}"
        T(tid, f"{jid.replace('-', ' ').capitalize()} (should-have)", "feature", [job_ticket.get(next((m for m in must_jobs if job_by_id[m].get('entity') == j.get('entity')), ""), "T-005" if offline_ctx else "T-003"), "T-004"],
          jobs=[jid], screens=scr, ops=ops, controls=["SEC-ACC-01", "SEC-LOG-02"], est="M",
          files=[f"apps/api/src/{entity_ctx.get(j.get('entity'), 'ordering')}/{_slug(jid)}.ts"] + [f"apps/web/app/{s}/page.tsx" for s in scr],
          tests=[f"Given the job is enabled, When {jid.replace('-', ' ')} runs, Then its operations respond per openapi.yaml", "Given the job is disabled by decision, When the screen is requested, Then it is hidden from navigation", "Given the screen, When it renders in ar, Then axe reports zero serious violations"],
          slice_=f"Should-have slice for `{jid}`.")
        job_ticket[jid] = tid
        n += 1
    # integrations
    for cat, providers in (pack.get("integrations") or {}).items():
        chosen = None
        for d in ledger.get("decisions", []):
            mt = d.get("maps_to") or ""
            if (mt.startswith(f"integrations.{cat}") or mt in (f"{cat}.provider", f"{cat}.vendor") or (cat == "payments" and mt in ("payments.provider", "funding.methods"))) and d["value"] not in (False, None, "", "cash-only", "none", "manual") and isinstance(d["value"], str):
                chosen = d["value"]
        if not chosen and cat == "einvoicing":
            chosen = {"AE": "ae-fta", "SA": "sa-zatca", "PK": "pk-fbr", "EG": "eg-eta"}.get(_region(ledger, pack))
        webhook = f"webhook_{cat}" if f"/webhooks/{cat}/{{provider}}" in (spec.get("paths") or {}) else None
        if not chosen and webhook and isinstance(providers, list) and providers:
            chosen = str(providers[0])  # generalisation fix (P10): the API emitted a webhook for this category, so a ticket must own it
        if not chosen:
            continue
        tid = f"T-{n:03d}"
        T(tid, f"Integration: {cat} adapter ({chosen})", "integration", (["T-005"] if offline_ctx else ["T-004"]) + ([job_ticket.get("take-payment")] if cat == "payments" and job_ticket.get("take-payment") else []),
          ops=[webhook] if webhook else [], adrs=["0006"], controls=["SEC-API-04", "SEC-API-05", "SEC-CRY-06", "SEC-API-06"] + (["SEC-PAY-01", "SEC-PAY-02", "SEC-PAY-03"] if cat == "payments" else []), est="L",
          files=[f"apps/api/src/integrations/{cat}/{_slug(str(chosen))}.ts", f"apps/api/src/integrations/{cat}/adapter.ts", f"apps/api/src/webhooks/{cat}.ts"],
          tests=[f"Given a sandbox {chosen} account, When the adapter runs its contract test, Then every method returns the expected shape",
                 f"Given a signed {cat} webhook, When it arrives twice, Then it is applied once and the second returns the stored receipt",
                 f"Given an unsigned or tampered {cat} webhook, When it arrives, Then it is rejected with 401 and logged",
                 f"Given the provider times out, When the adapter is called, Then the circuit opens after 3 failures and the UI offers a fallback"],
          slice_=f"{cat} adapter interface plus {chosen} module, webhook endpoint with idempotency on (provider, event_id), sandbox contract test, wizard note for live keys.")
        n += 1
    # compliance tickets for unowned planned controls (grouped by family)
    owned = {c for t in tickets for c in t["controls"]}
    ctrl_by_id = {r["id"]: r for r in _rows("security-controls")}
    unowned = [c for c in comp.get("controls") or [] if c.get("status") == "planned" and c["id"] not in owned]
    groups: dict[str, list[dict]] = {}
    for c in unowned:
        fam = ctrl_by_id.get(c["id"], {}).get("family", "compliance")
        groups.setdefault(fam, []).append(c)
    for fam, items in sorted(groups.items()):
        tid = f"T-{n:03d}"
        T(tid, f"Compliance: {fam} controls ({len(items)})", "compliance", ["T-003"], controls=[c["id"] for c in items], est="M" if len(items) < 8 else "L",
          files=["apps/api/src/security/", "docs/compliance/", ".foundry/compliance.yaml"],
          tests=[f"Given control {items[0]['id']}, When its verify method ({ctrl_by_id.get(items[0]['id'], {}).get('verify', 'review')}) runs, Then evidence is attached in compliance.yaml",
                 f"Given every control in this ticket, When the evidence plan is executed, Then status moves from planned to done with a link",
                 f"Given a regression, When the {fam} tests run in CI, Then a failing control blocks merge"],
          slice_=f"Implement and evidence {len(items)} {fam} controls: " + ", ".join(c["id"] for c in items[:12]) + ("…" if len(items) > 12 else ""))
        for c in items:
            c["owner"] = tid
        n += 1
    # release
    T("T-900", "Release: deploy, observability, runbook", "release", [t["id"] for t in tickets if t["type"] in ("feature", "integration")][-6:] + ["T-000"], adrs=["0007", "0008"], controls=["SEC-CFG-01", "SEC-CFG-02", "SEC-CFG-04", "SEC-LOG-01", "SEC-DATA-06"], est="L",
      files=["Dockerfile", "fly.toml", "docs/runbook.md", "CHANGELOG.md"],
      tests=["Given the container image, When deployed to staging, Then /health is ok and the smoke e2e passes on the deployed URL",
             "Given structured logs, When a request fails, Then the request id links web, api and provider logs",
             "Given the runbook, When a new operator follows it, Then deploy, rollback and backup restore complete without help"],
      slice_="Container build, staging and production environments per ADR 0007, error tracking and metrics per ADR 0008, runbook, changelog.")
    # write owners back to compliance.yaml
    if (project / ".foundry" / "compliance.yaml").exists():
        for c in comp.get("controls") or []:
            if not c.get("owner"):
                c["owner"] = next((t["id"] for t in tickets if c["id"] in t["controls"]), None)
        (project / ".foundry" / "compliance.yaml").write_text(_dump_compliance(comp), encoding="utf-8", newline="\n")
    return tickets


def run_tickets_skeleton(project: Path, root: Path) -> int:
    tickets = tickets_skeleton(project, root)
    out = project / ".foundry" / "tickets"
    out.mkdir(parents=True, exist_ok=True)
    # Re-runs re-number job tickets when priorities change; purge stale generated files (status.yaml files are kept).
    for stale in out.glob("T-*.md"):
        stale.unlink()
    for old in out.glob("T-*.md"):
        old.unlink()
    for t in tickets:
        (out / f"{t['id']}-{_slug(t['title'])[:40]}.md").write_text(_ticket_md(t), encoding="utf-8", newline="\n")
    _regulated_wizard(project, root)
    print(f"tickets-skeleton: {len(tickets)} tickets -> .foundry/tickets/ ({sum(1 for t in tickets if t['type'] == 'feature')} feature, {sum(1 for t in tickets if t['type'] == 'integration')} integration, {sum(1 for t in tickets if t['type'] == 'compliance')} compliance)")
    return 0


def _regulated_wizard(project: Path, root: Path) -> None:
    """Schema 1.9 `regulated: true`: scaffold the regulator-licence wizard once; `gate release` stays red until a human
    runs `release confirm` after it."""
    import foundry_ops as O
    if not O.pack_regulated(project, root) or (project / ".foundry" / "wizard" / "regulator-licence.md").exists():
        return
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    region = _region(ledger, pack)
    reg = (pack.get("regional") or {}).get(region) or {}
    regulator = str(reg.get("regulator") or "the regulator for your jurisdiction")
    from types import SimpleNamespace
    a = SimpleNamespace(action="scaffold", slug="regulator-licence", ticket="T-000",
                        why=f"{pack.get('name', 'this domain')} is a regulated activity: {regulator} must license or register the operator before real users trade, deposit or withdraw. Foundry cannot obtain a licence; it ships every regulated flow behind FEATURE_REGULATED_LIVE=false until a human confirms.",
                        validate="python scripts/foundry.py wizard status",
                        var=["REGULATOR_NAME:Regulator that issued the licence or registration:^.{2,80}$", "LICENCE_REF:Licence or registration reference:^.{3,64}$", "LICENCE_EXPIRY:Licence expiry (YYYY-MM-DD):^\\d{4}-\\d{2}-\\d{2}$", "COMPLIANCE_OFFICER_EMAIL:Compliance officer contact:^[^@\\s]+@[^@\\s]+$"],
                        step=[f"Confirm with {regulator} which licence category covers the decided asset classes and custody model (see .foundry/compliance.yaml).", "Obtain the licence or registration, or a written no-objection for a sandbox pilot.", "Appoint a compliance officer and record the contact below.", "Paste each value when the script prompts; then run `python scripts/foundry.py release confirm --by <your name>`."])
    O.run_wizard(a, project)
    print("tickets-skeleton: regulated pack → wizard regulator-licence scaffolded; `gate release` needs `release confirm --by <name>`")


def load_tickets(project: Path) -> list[dict]:
    out = []
    for p in sorted((project / ".foundry" / "tickets").glob("T-*.md")):
        fm, _ = _fm(p)
        fm["_file"] = p.name
        out.append(fm)
    return out


def topo(tickets: list[dict]) -> tuple[list[str], list[str]]:
    """Return (order, errors)."""
    ids = {t["id"] for t in tickets}
    deps = {t["id"]: [b for b in t.get("blockedBy") or []] for t in tickets}
    errs = [f"{t['id']} blocked by unknown {b}" for t in tickets for b in deps[t["id"]] if b not in ids]
    order: list[str] = []
    state: dict[str, int] = {}
    def visit(n: str, path: list[str]):
        if state.get(n) == 2:
            return
        if state.get(n) == 1:
            errs.append("cycle: " + " -> ".join(path + [n]))
            return
        state[n] = 1
        for d in deps.get(n, []):
            if d in ids:
                visit(d, path + [n])
        state[n] = 2
        order.append(n)
    for t in sorted(tickets, key=lambda t: t["id"]):
        visit(t["id"], [])
    return order, errs


def gate_tickets(project: Path, root: Path) -> list[str]:
    import foundry_phases as P
    errs = gate_security(project, root)
    if errs:
        return errs
    tdir = project / ".foundry" / "tickets"
    if not tdir.exists() or not list(tdir.glob("T-*.md")):
        return [".foundry/tickets/ has no tickets"]
    tickets = load_tickets(project)
    order, terrs = topo(tickets)
    errs += terrs
    if len(tickets) > 60:
        errs.append(f"{len(tickets)} tickets; max 60")
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    jobs_in_scope, _ = P._in_scope_ids(project, pack)
    job_by_id = {j["id"]: j for j in pack.get("jobs") or []}
    covered_jobs = {j for t in tickets for j in t.get("jobs") or []}
    for jid in jobs_in_scope:
        if job_by_id.get(jid, {}).get("must") and jid not in covered_jobs:
            errs.append(f"must-have job {jid} not covered by a ticket")
    spec = F.parse_yaml((project / "openapi.yaml").read_text(encoding="utf-8"))
    covered_ops = {o for t in tickets for o in t.get("operations") or []}
    for path, methods in (spec.get("paths") or {}).items():
        if str(path).startswith("/admin"):
            continue
        for m, op in (methods or {}).items():
            if m in ("get", "post", "patch", "put", "delete"):
                xf = op.get("x-foundry") or {}
                if xf.get("job") in ("read", "create", "update", "archive"):
                    continue  # CRUD is covered by the entity's job ticket via screens data bindings
                if op["operationId"] not in covered_ops:
                    errs.append(f"public operation {op['operationId']} not covered by a ticket")
    covered_screens = {s for t in tickets for s in t.get("screens") or []}
    for p in (project / ".foundry" / "screens").glob("*.md"):
        if p.stem not in covered_screens:
            errs.append(f"screen {p.stem} not covered by a ticket")
    comp = F.parse_yaml((project / ".foundry" / "compliance.yaml").read_text(encoding="utf-8"))
    for c in comp.get("controls") or []:
        if c.get("status") == "planned" and not c.get("owner"):
            errs.append(f"planned control {c['id']} has no owning ticket")
    for t in tickets:
        if len(t.get("acceptance_tests") or []) < 3:
            errs.append(f"{t['id']} has fewer than 3 acceptance tests")
    t0 = next((t for t in tickets if t["id"] == "T-000"), None)
    if t0 is None or t0.get("blockedBy"):
        errs.append("T-000 missing or has blockers")
    return errs


def run_tickets_next(project: Path, n: int, done: set[str] | None = None) -> int:
    tickets = load_tickets(project)
    order, errs = topo(tickets)
    if errs:
        for e in errs:
            print(f"tickets: {e}")
        return 1
    done = done or set()
    by_id = {t["id"]: t for t in tickets}
    ready = [tid for tid in order if tid not in done and all(b in done for b in by_id[tid].get("blockedBy") or [])]
    for tid in ready[:n]:
        t = by_id[tid]
        print(f"{tid}  {t['title']}  [{t['type']}, {t['estimate']}]  blockedBy: {', '.join(t.get('blockedBy') or []) or '-'}")
    return 0


GATES = {"security": gate_security, "tickets": gate_tickets}
