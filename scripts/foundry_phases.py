"""Foundry phases 4-6: domain model, architecture + ADRs, data model, API contract.

Imported by foundry.py; Python 3.11+ stdlib only. Every skeleton output passes its gate
without model refinement; the model only adds.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import foundry as F

CONTEXTS = ["ordering", "kitchen", "payments", "menu", "inventory", "people", "reporting", "sync"]
CONTEXT_HINTS = {
    "ordering": ["Order", "OrderLine", "Table", "Course", "Reservation", "Record", "Tenant"],
    "kitchen": ["KitchenTicket"],
    "payments": ["Payment", "Tender", "Refund", "Receipt", "Discount", "TaxRule", "Transaction"],
    "menu": ["MenuItem", "Variant", "Modifier", "ModifierGroup", "Product", "Instrument"],
    "inventory": ["InventoryItem", "Recipe", "StockMovement", "Sale", "Return", "Position"],
    "people": ["Branch", "Staff", "Role", "Customer", "User", "Account"],
    "reporting": ["AuditEvent", "Notification"],
    "sync": ["SyncEvent"],
}
BRANCH_STATES = {"void", "voided", "refunded", "cancelled", "rejected", "failed", "declined", "no-show", "recalled",
                 "hidden", "discontinued", "suspended", "blocked", "disabled", "retired", "expired", "sold-out",
                 "comped", "held", "dirty", "conflict", "closed", "seasonal", "restricted", "halted", "delisted", "reprinted"}
ADR_IDS = ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0009"]
TRUST_BOUNDARIES = ["internet<->edge", "edge<->api", "api<->db", "api<->payment-provider", "terminal<->local-print-bridge", "device<->offline-store", "api<->delivery-platform"]


# ----------------------------------------------------------------------------- helpers
def _kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _plural(kebab: str) -> str:
    if kebab.endswith("y") and kebab[-2] not in "aeiou":
        return kebab[:-1] + "ies"
    if kebab.endswith(("s", "x", "ch", "sh")):
        return kebab + "es"
    return kebab + "s"


def _camel_state(state: str) -> str:
    return "".join(w.capitalize() for w in re.split(r"[-_ ]", state))


def _context_for(entity: str) -> str:
    for ctx, names in CONTEXT_HINTS.items():
        if entity in names:
            return ctx
    return "ordering"


def _read_prd_sections(project: Path) -> dict[str, str]:
    p = project / ".foundry" / "prd.md"
    if not p.exists():
        return {}
    _, _, body = F.split_frontmatter(p.read_text(encoding="utf-8"))
    return F._prd_sections(body)


def _in_scope_ids(project: Path, pack: dict) -> tuple[list[str], list[str]]:
    """(job ids from PRD §3, feature ids from PRD §4); falls back to the pack."""
    sec = _read_prd_sections(project)
    jobs = re.findall(r"^\|\s*`([a-z0-9-]+)`", sec.get("3", ""), re.M) or [j["id"] for j in pack.get("jobs") or []]
    feats = re.findall(r"^- `([a-z0-9-]+)`", sec.get("4", ""), re.M) or list(pack.get("must_have") or [])
    return jobs, feats


def _region(ledger: dict, pack: dict) -> str:
    for d in ledger.get("decisions", []):
        if d.get("maps_to") == "region.country" or d["id"] == "region":
            return str(d["value"])
    return next(iter(pack.get("regional") or {"AE": {}}))


def _minor_units(ledger: dict, pack: dict) -> int:
    reg = (pack.get("regional") or {}).get(_region(ledger, pack)) or {}
    return int(reg.get("minor_units", 2))


def _stack_id(pack: dict) -> str:
    sd = pack.get("stack_default") or {}
    return str(sd.get("web-pos") or sd.get("web") or "nextjs-pwa")


# ----------------------------------------------------------------------------- doctor
def _version(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20, shell=(sys.platform == "win32"))
        text = (out.stdout or out.stderr).strip().splitlines()
        return text[0].strip() if text else None
    except (OSError, subprocess.SubprocessError):
        return None


def _semver(text: str | None) -> tuple[int, ...]:
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text or "")
    return tuple(int(x) for x in m.groups(default="0")) if m else (0,)


def run_doctor() -> int:
    rows: list[tuple[str, str, str, bool]] = []
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    rows.append(("python", py, "ok" if sys.version_info >= (3, 11) else "need 3.11+", True))
    node = _version(["node", "--version"])
    rows.append(("node", node or "missing", "ok" if _semver(node) >= (20,) else "need 20+ (https://nodejs.org)", True))
    npm = _version(["npm", "--version"])
    pnpm = _version(["pnpm", "--version"])
    rows.append(("npm/pnpm", f"npm {npm or '-'} / pnpm {pnpm or '-'}", "ok" if npm or pnpm else "missing", False))
    rows.append(("npx", "present" if shutil.which("npx") else "missing", "ok" if shutil.which("npx") else "comes with npm", False))
    git = _version(["git", "--version"])
    rows.append(("git", git or "missing", "ok" if git else "install git", True))
    cbm = shutil.which("codebase-memory-mcp")
    rows.append(("codebase-memory-mcp", cbm or "missing", "ok" if cbm else
                 "optional until P7; Windows: powershell -c \"irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 | iex\"", False))
    docker = _version(["docker", "--version"])
    rows.append(("docker", docker or "missing", "ok" if docker else "optional (local postgres via compose)", False))
    print(f"{'tool':<22} {'found':<40} {'status'}")
    print("-" * 100)
    hard_fail = False
    for name, found, status, hard in rows:
        print(f"{name:<22} {found[:40]:<40} {status}")
        if hard and status != "ok":
            hard_fail = True
    print("\ndoctor: " + ("FAIL (python, node or git missing)" if hard_fail else "ok"))
    return 1 if hard_fail else 0


def cbm_present() -> bool:
    return shutil.which("codebase-memory-mcp") is not None


# ----------------------------------------------------------------------------- query
def run_query(root: Path, name: str, filters: dict[str, str], n: int, as_json: bool) -> int:
    p = root / "data" / (name if name.endswith(".csv") else f"{name}.csv")
    if not p.exists():
        print(f"query: {p} not found")
        return 1
    with p.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for col, val in filters.items():
        if rows and col not in rows[0]:
            print(f"query: unknown column '{col}'; columns: {', '.join(rows[0].keys())}")
            return 1
        rows = [r for r in rows if r.get(col, "") == val or val.lower() in r.get(col, "").lower()]
    total = len(rows)
    rows = rows[:n]
    if as_json:
        print(json.dumps({"rows": rows, "total": total}, indent=2))
        return 0
    if not rows:
        print("query: 0 rows")
        return 0
    cols = list(rows[0].keys())
    widths = {c: min(40, max(len(c), *(len(r[c]) for r in rows))) for c in cols}
    print(" | ".join(c.ljust(widths[c]) for c in cols))
    print("-+-".join("-" * widths[c] for c in cols))
    for r in rows:
        print(" | ".join(r[c][: widths[c]].ljust(widths[c]) for c in cols))
    if total > n:
        print(f"... {total - n} more rows (use --n)")
    return 0


# ----------------------------------------------------------------------------- phase 4: domain
def domain_skeleton(pack: dict, ledger: dict, project: Path) -> tuple[dict, str]:
    jobs, feats = _in_scope_ids(project, pack)
    personas = pack.get("personas") or ["staff"]
    job_by_id = {j["id"]: j for j in pack.get("jobs") or []}
    inv_text = pack.get("invariants") or []

    def actor_for(entity: str) -> str:
        ek = _kebab(entity).split("-")
        for jid in jobs:
            j = job_by_id.get(jid)
            if not j:
                continue
            words = set(jid.split("-")) | {w for s in j.get("screens") or [] for w in s.split("-")}
            if set(ek) & words:
                return j.get("persona") or personas[0]
        return personas[0]

    entities = []
    events = []
    for name, spec in (pack.get("entities") or {}).items():
        states = list(spec.get("states") or [])
        fields = list(spec.get("fields") or [])
        actor = actor_for(name)
        chain = [s for s in states if s not in BRANCH_STATES]
        branches = [s for s in states if s in BRANCH_STATES]
        transitions = []
        for a, b in zip(chain, chain[1:]):
            transitions.append({"from": a, "to": b, "by": actor, "guard": ""})
        origin = chain[1] if len(chain) > 1 else (chain[0] if chain else "*")
        for b in branches:
            transitions.append({"from": origin, "to": b, "by": "manager" if "manager" in personas else actor, "guard": "reason recorded"})
        if not transitions and states:
            transitions.append({"from": "*", "to": states[0], "by": actor, "guard": ""})
        invs = [i for i in inv_text if re.search(rf"\b{re.escape(name)}s?\b", i)]
        if not invs:
            invs = [f"{name} has exactly one state at a time"]
        ctx = _context_for(name)
        entities.append({"name": name, "fields": fields, "states": states, "transitions": transitions, "invariants": invs, "owned_by": ctx})
        for t in transitions:
            ev = f"{name}{_camel_state(t['to'])}"
            consumers = ["reporting"]
            if ctx == "ordering" and t["to"] in ("sent", "fired", "in-progress"):
                consumers.append("kitchen")
            if ctx in ("ordering", "payments"):
                consumers.append("sync")
            events.append({"name": ev, "entity": name, "transition": f"{t['from']}->{t['to']}", "producer": ctx, "consumers": [c for c in consumers if c != ctx] or ["reporting"]})
    domain = {"pack": pack["slug"], "decisions_hash": F.decisions_hash(ledger), "contexts": CONTEXTS, "entities": entities, "events": events}
    return domain, context_md(pack, ledger, project, domain, jobs, feats)


def _glossary_rows(pack: dict, root: Path) -> list[dict]:
    p = root / "packs" / pack["slug"] / (pack.get("reference") or {}).get("glossary", "reference/glossary.csv")
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def context_md(pack: dict, ledger: dict, project: Path, domain: dict, jobs: list[str], feats: list[str]) -> str:
    sec = _read_prd_sections(project)
    title = re.search(r"^# PRD — (.+)$", (project / ".foundry" / "prd.md").read_text(encoding="utf-8"), re.M) if (project / ".foundry" / "prd.md").exists() else None
    name = title.group(1).strip() if title else pack["name"]
    purpose = " ".join(l for l in sec.get("1", "").splitlines() if l.strip() and not l.startswith("<!--")).split(". ")[0].strip()
    purpose = (purpose + ".") if purpose and not purpose.endswith(".") else purpose or f"{pack['name']} built by Foundry."
    entity_names = [e["name"] for e in domain["entities"]]
    scope_tokens = {w for i in jobs + feats for w in i.split("-")} | {F._stem(w) for e in entity_names for w in F._norm(_kebab(e)).split()}
    rows = _glossary_rows(pack, F.ROOT)
    kept = []
    for r in rows:
        term_tokens = {F._stem(w) for w in F._norm(r["term"]).split()}
        alias_tokens = {F._stem(w) for w in F._norm(r.get("aliases", "")).split()}
        if term_tokens & scope_tokens or alias_tokens & scope_tokens or r["term"] in entity_names:
            kept.append(r)
    covered_terms = {r["term"].lower() for r in kept}
    out = [f"# {name} — CONTEXT", "", purpose, "", "Ubiquitous language for this project. Every noun in the PRD, the domain model and the code uses",
           "the term in this file; aliases are accepted in conversation and normalised in artifacts.", "",
           "## Entities", "", "| Entity | Context | States |", "|--------|---------|--------|"]
    for e in domain["entities"]:
        out.append(f"| {e['name']} | {e['owned_by']} | {', '.join(e['states']) or '-'} |")
    out += ["", "## Glossary", "", "| Term | Definition | Aliases |", "|------|------------|---------|"]
    for r in kept:
        out.append(f"| {r['term']} | {r['definition']} | {r.get('aliases', '')} |")
    out += ["", "## Feature vocabulary", "", "| Id | Meaning |", "|----|---------|"]
    for fid in feats:
        if fid.lower() not in covered_terms:
            out.append(f"| `{fid}` | {fid.replace('-', ' ')} (PRD §4) |")
    out += ["", "## Job vocabulary", "", "| Id | Meaning |", "|----|---------|"]
    for jid in jobs:
        out.append(f"| `{jid}` | {jid.replace('-', ' ')} (PRD §3) |")
    out += ["", "## Decisions vocabulary", "", "| Decision | Canonical word | Source |", "|----------|----------------|--------|"]
    for d in ledger.get("decisions", []):
        word = (d.get("maps_to") or d["id"]).replace(".", " ").replace("_", " ").replace("-", " ")
        out.append(f"| {d['id']} | {word} = {F._yq(d['value']).strip(chr(34))} | {d['source']} |")
    out += ["", "## Project-specific terms", "", "<!-- model: add up to 10 terms the pack glossary lacks, same table shape -->", "", "| Term | Definition | Aliases |", "|------|------------|---------|", ""]
    return "\n".join(out)


def _dump_domain(domain: dict) -> str:
    out = [f"pack: {F._yq(domain['pack'])}", f"decisions_hash: {F._yq(domain['decisions_hash'])}", f"contexts: {F._yq(domain['contexts'])}", "entities:"]
    for e in domain["entities"]:
        out.append(f"  - name: {F._yq(e['name'])}")
        out.append(f"    owned_by: {F._yq(e['owned_by'])}")
        out.append(f"    fields: {F._yq(e['fields'])}")
        out.append(f"    states: {F._yq(e['states'])}")
        out.append(f"    invariants: {F._yq(e['invariants'])}")
        out.append("    transitions:" if e["transitions"] else "    transitions: []")
        for t in e["transitions"]:
            out.append(f"      - {F._yq(t)}")
    out.append("events:")
    for ev in domain["events"]:
        out.append(f"  - {F._yq(ev)}")
    return "\n".join(out) + "\n"


def run_domain_skeleton(project: Path, root: Path) -> int:
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    domain, ctx = domain_skeleton(pack, ledger, project)
    (project / ".foundry" / "domain.yaml").write_text(_dump_domain(domain), encoding="utf-8", newline="\n")
    (project / "CONTEXT.md").write_text(ctx, encoding="utf-8", newline="\n")
    print(f"domain-skeleton: {len(domain['entities'])} entities, {sum(len(e['transitions']) for e in domain['entities'])} transitions, {len(domain['events'])} events -> .foundry/domain.yaml, CONTEXT.md")
    return 0


def gate_domain(project: Path, root: Path) -> list[str]:
    errs = F.gate_prd(project, root)
    if errs:
        return errs
    dp = project / ".foundry" / "domain.yaml"
    cp = project / "CONTEXT.md"
    if not dp.exists() or not cp.exists():
        return [f"{dp if not dp.exists() else cp} missing"]
    try:
        domain = F.parse_yaml(dp.read_text(encoding="utf-8"))
    except F.YamlError as e:
        return [f"domain.yaml: {e}"]
    errs = [f"domain.yaml: {m}" for m in F.validate_schema(domain, F.load_schema("domain.schema.json", root / "schemas"))]
    if errs:
        return errs
    ctx_text = cp.read_text(encoding="utf-8").lower()
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    jobs, feats = _in_scope_ids(project, pack)
    entity_names = {e["name"] for e in domain["entities"]}
    glossary_terms = {m.group(1).strip().lower() for m in re.finditer(r"^\|\s*`?([^|`]+)`?\s*\|", ctx_text, re.M)}
    for noun in jobs + feats:
        if noun.lower() not in glossary_terms and noun.lower() not in ctx_text:
            errs.append(f"PRD noun '{noun}' resolves to no glossary term or entity in CONTEXT.md")
    personas = set(pack.get("personas") or [])
    for e in domain["entities"]:
        if not e["invariants"]:
            errs.append(f"entity {e['name']} has no invariant")
        if not e["transitions"]:
            errs.append(f"entity {e['name']} has no transition")
        for t in e["transitions"]:
            if t["by"] not in personas and t["by"] != "system":
                errs.append(f"entity {e['name']} transition {t['from']}->{t['to']} actor '{t['by']}' is not a persona")
    for ev in domain["events"]:
        if not ev.get("consumers") and not ev.get("external"):
            errs.append(f"event {ev['name']} has no consumer and is not external")
        if ev.get("entity") and ev["entity"] not in entity_names:
            errs.append(f"event {ev['name']} names unknown entity {ev['entity']}")
    return errs


# ----------------------------------------------------------------------------- phase 5: architecture
def _decision(ledger: dict, qid: str) -> dict | None:
    return next((d for d in ledger.get("decisions", []) if d["id"] == qid), None)


def _ref(ledger: dict, *ids: str) -> tuple[list[str], str]:
    refs = [f"D:{i}" for i in ids if _decision(ledger, i)]
    return refs, (" ".join(f"[{r}]" for r in refs) if refs else "(pack-default)")


def _adr(idn: str, title: str, refs: list[str], context: str, decision: str, alternatives: list[tuple[str, str]], consequences: list[str], revisit: str) -> str:
    out = ["---", f"id: {F._yq(idn)}", f"title: {F._yq(title)}", "status: accepted", f"decision_refs: {F._yq(refs)}", f"date: {F._yq(F._now()[:10])}", "---", "",
           f"# ADR {idn}: {title}", "", "## Context", "", context, "", "## Decision", "", decision, "", "## Alternatives", "",
           "| Alternative | Rejected because |", "|-------------|------------------|"]
    out += [f"| {a} | {b} |" for a, b in alternatives]
    out += ["", "## Consequences", ""] + [f"- {c}" for c in consequences] + ["", "## Revisit when", "", revisit, ""]
    return "\n".join(out)


def arch_skeleton(pack: dict, ledger: dict, domain: dict | None) -> tuple[dict[str, str], str]:
    sd = pack.get("stack_default") or {}
    nfr = pack.get("nfr_defaults") or {}
    region = _region(ledger, pack)
    reg = (pack.get("regional") or {}).get(region) or {}
    off = _decision(ledger, "offline")
    offline = bool(off["value"]) if off else str(nfr.get("offline", "optional")) == "required"
    br = _decision(ledger, "branches")
    multi = bool(br and str(br["value"]) == "multi")
    pay = _decision(ledger, "payments")
    pay_name = str(pay["value"]) if pay else "provider"
    stack_id = _stack_id(pack)
    langs = reg.get("receipt_lang") or reg.get("languages") or ["en"]
    adrs: dict[str, str] = {}
    r, c = _ref(ledger, "offline", "platform")
    adrs["0001"] = _adr("0001", "Stack", r,
        f"Pack default stack: {', '.join(f'{k} {v}' for k, v in sd.items())}. Hardware breadth (tablets, Windows terminals, kitchen screens) and offline needs {c} decide the web layer.",
        f"Web/POS: {stack_id}. API: {sd.get('api', 'hono-node')}. Database: {sd.get('db', 'postgres')}. Offline store: {sd.get('offline', 'pglite-event-sourced-sync')}. Realtime: {sd.get('realtime', 'websocket')}. Mobile companion: {sd.get('mobile-waiter') or sd.get('mobile', 'expo')}. Printing: {sd.get('printing', 'escpos-local-bridge')}. Commands per layer come from data/stacks.csv.",
        [("Native apps only (Expo everywhere)", "no Windows POS terminal path; slower hardware iteration"), ("NestJS API", "heavier DI framework for a small team; hono covers the routing and middleware needed")],
        ["One TypeScript language across web, api, bridge and mobile", "PWA install on tablets; store submission only for the companion app", "stacks.csv is the source of truth for scaffold, test, typecheck, lint and a11y commands"],
        "A native-only device (kiosk hardware without a browser) enters scope, or team size passes 8 engineers.")
    r, c = _ref(ledger, "service-model", "branches")
    adrs["0002"] = _adr("0002", "Auth and sessions", r,
        f"Two actor classes: devices (POS terminals, KDS screens, print bridge) and staff (PIN, roles). Guarded actions need a manager override. Personas: {', '.join(pack.get('personas') or [])} {c}.",
        "Device auth: each terminal enrolled once with a long-lived device token bound to a branch; rotated on re-enrol. Staff auth: 4–6 digit PIN hashed with Argon2id per branch, 3-strike 60 s lockout, verified offline against the local hash. Manager override: PIN of a staff whose role carries the permission, recorded as approver on the audit event. Owner and back-office web: email + password with optional TOTP. Sessions: device token (30 d absolute) plus staff session (shift-bound); server tokens are httpOnly cookies for web and bearer for devices.",
        [("Per-staff passwords on the POS", "too slow at the till; PINs are the industry norm"), ("Shared terminal login without staff identity", "no per-actor audit trail; fails the audit control")],
        ["Every mutating request carries device id and staff id", "Offline PIN verification works from the local hash cache", "Role matrix lives in the people context and syncs to devices"],
        "SSO for back-office users is requested, or a regulator requires biometric staff sign-in.")
    r, c = _ref(ledger, "branches", "central-menu-sync")
    adrs["0003"] = _adr("0003", "Tenancy and branches", r,
        f"Branches decision: {'multi-branch' if multi else 'single branch'} {c}. Every financial record is scoped to a branch; receipts, floats and tax rules are per branch.",
        f"Single organisation (tenant) per deployment with branch_id on every operational table; Postgres row-level security keyed by branch for device roles, organisation-wide for owner roles. {'Central menu published to branches with per-branch price overrides.' if multi else 'Schema is multi-branch ready; a second branch is a data row, not a migration.'} No cross-organisation tenancy in this release.",
        [("Multi-tenant SaaS from day one", "adds RLS complexity and billing before the first customer runs"), ("Database per branch", "reporting across branches becomes ETL; sync harder")],
        ["Branch switcher only for owner roles", "Consolidated reports are simple SQL", "Adding organisations later means adding tenant_id above branch_id"],
        "A second organisation must share the deployment, or a branch must run on its own server.")
    r, c = _ref(ledger, "region")
    adrs["0004"] = _adr("0004", "Data store and migrations", r,
        f"Money in {reg.get('currency', 'AED')} with {reg.get('minor_units', 2)} minor units; {reg.get('rounding', 'rounding once per order')} {c}. Audit and fiscal records are append-only.",
        f"Postgres 16 as the system of record. ORM {sd.get('orm', 'prisma')} with migrations committed under prisma/ and applied by the command in stacks.csv. Money columns Decimal(12,{reg.get('minor_units', 2)}); ids uuid v7; created_at/updated_at on every table; soft delete only where an invariant demands history; audit_events and receipts append-only via grants. Backups daily, restore drill quarterly.",
        [("SQLite on the server", "single-writer; multi-terminal branches and reporting need concurrency"), ("MongoDB", "invariants are relational; RLS and constraints are the gate")],
        ["Schema skeleton generated from domain.yaml", "Every entity state is a Postgres enum", "Indexes on (branch_id, created_at) by default"],
        "Write volume exceeds one Postgres primary, or a regulator demands a certified fiscal store.")
    r, c = _ref(ledger, "offline")
    adrs["0005"] = _adr("0005", "Offline and sync", r,
        f"Offline required: {offline} {c}. Terminals keep taking orders when the internet drops; recovery target {nfr.get('sync_recovery_s', 60)} s after reconnect.",
        "Event-sourced outbox on the device: every write is a SyncEvent (device_id, monotonic seq, entity, payload). Orders carry a client UUID; receipt numbers come from a per-device block reserved per branch so numbering stays gapless. On reconnect events replay in seq order and are acked individually. Conflicts: last-writer-wins per field, Payments append-only, voids beat edits; unresolvable conflicts surface on the sync-status screen. Server pushes menu and table state over websocket; devices pull on reconnect.",
        [("CRDT document per order", "harder to audit and to reason about for money; the outbox rule set from workflows.md is enough"), ("Online-only with a queue", "fails the offline gate")],
        ["Device store is pglite (same SQL dialect as the server)", "Sync endpoints /sync/push and /sync/pull with per-device sequence", "Receipt block allocation is a server call made while online"],
        "Two devices must edit the same order offline for long periods, or fiscal rules forbid device-side numbering.")
    r, c = _ref(ledger, "payments", "delivery", "kds")
    adrs["0006"] = _adr("0006", "Integrations boundary", r,
        f"Payments via {pay_name}; delivery platforms {'on' if (_decision(ledger, 'delivery') or {}).get('value') else 'off'}; printing through a local bridge {c}. Card data never enters the POS.",
        "One adapter interface per integration category (PaymentAdapter, DeliveryAdapter, PrinterAdapter, AccountingAdapter, FiscalAdapter) behind the api; providers are modules selected by branch settings. Inbound webhooks are idempotent on (provider, event_id) with a stored receipt; outbound calls carry an idempotency key derived from the order or payment id. Terminal payments are semi-integrated: the api pushes the amount, the terminal returns approval code and last four; the POS stores only those.",
        [("Direct provider SDK calls from the POS UI", "spreads secrets and PCI scope to devices"), ("Middleware aggregator for delivery", "adds a vendor and a failure point; direct partner APIs exist")],
        ["Provider secrets live only in the api environment", "Every adapter ships a sandbox test", "Tablet-fallback mode covers a platform outage"],
        "A provider only offers a device-side SDK, or a fourth delivery platform is added.")
    r, c = _ref(ledger, "branches")
    adrs["0007"] = _adr("0007", "Deployment and environments", r,
        f"Small team, {'several' if multi else 'one'} branch(es), no SRE. Local development must run on Windows without WSL {c}.",
        "Local: docker compose with postgres and the api; web via the framework dev server; the print bridge runs natively. Production default: one VPS or Fly.io app per organisation with managed Postgres, TLS at the edge, nightly backups. Environments: local, staging, production; secrets injected by the platform; preview environment per PR is added in P7 when CI exists.",
        [("Kubernetes", "operational cost far above a single-organisation deployment"), ("Serverless functions", "websocket fan-out and long-lived sync connections fit poorly")],
        ["Same container image for staging and production", "Deploy is one command in the runbook", "Wizard covers DNS, secrets and provider onboarding"],
        "More than 100 branches, multi-region residency, or a second organisation.")
    r, c = _ref(ledger, "offline")
    adrs["0008"] = _adr("0008", "Observability", r,
        f"Operational app with offline devices: failures surface late unless every request and sync event is traceable {c}.",
        "Structured JSON logs with request id, device id, staff id and branch id on every line; error tracking with source maps for web, api and bridge; metrics for sync queue depth, ticket age and payment latency; health endpoint per container; alerts on fiscal reporting backlog (SA 20 h) and sync lag over 5 min.",
        [("Console logs only", "no correlation across device, api and provider"), ("Full tracing platform on day one", "cost and setup exceed the first release; add when p95 targets are missed")],
        ["Request id propagates from device to provider calls", "Sync-status screen reads the same metrics", "Log retention 30 days, audit table forever"],
        "p95 targets are missed and logs cannot explain why.")
    r, c = _ref(ledger, "region")
    adrs["0009"] = _adr("0009", "Internationalisation and RTL", r,
        f"Region {region}; receipt languages {', '.join(map(str, langs))} {c}. Arabic and Urdu need right-to-left layouts and bilingual receipts.",
        "ICU message catalogs per language; logical CSS properties throughout; full mirroring for RTL except numerals, prices, numpads, QR codes and floor coordinates; menu items carry name per language; receipts render both blocks with identical totals; locale-aware number and date formatting with Western numerals by default and Arabic-Indic per branch setting.",
        [("English-only first release", "receipt language is a legal requirement in the region"), ("Machine-translated UI", "operational terms need reviewed translations")],
        ["Every screen spec carries an RTL note", "Pseudo-localisation test in CI", "Fonts with Naskh/Nastaliq fallback"],
        "A language outside en, ar, ur is required.")
    arch = architecture_md(pack, ledger, domain, stack_id, multi, offline, pay_name)
    return adrs, arch


def architecture_md(pack: dict, ledger: dict, domain: dict | None, stack_id: str, multi: bool, offline: bool, pay_name: str) -> str:
    sd = pack.get("stack_default") or {}
    tb = TRUST_BOUNDARIES if (_decision(ledger, "delivery") or {}).get("value") else TRUST_BOUNDARIES[:6]
    out = ["---", f"pack: {F._yq(pack['slug'])}", f"stack_id: {F._yq(stack_id)}", f"adr_ids: {F._yq(ADR_IDS)}", f"trust_boundaries: {F._yq(tb)}", f"decisions_hash: {F._yq(F.decisions_hash(ledger))}", "---", "",
           f"# Architecture — {pack['name']}", "", "ADRs under .foundry/adr/. Containers follow C4 level 2.", "",
           "## Containers", "", "| Name | Tech | Responsibility | Talks to |", "|------|------|----------------|----------|",
           f"| pos-web | {stack_id} | Cashier, waiter and manager screens; offline store; print jobs | api, print-bridge, offline-store |",
           f"| kds-web | {stack_id} | Kitchen display per station | api (websocket) |",
           f"| mobile-waiter | {sd.get('mobile-waiter') or sd.get('mobile', 'expo')} | Handheld order taking | api |",
           f"| api | {sd.get('api', 'hono-node')} | Domain services, authz, sync, adapters, webhooks | db, payment-provider, delivery-platform, accounting, fiscal |",
           f"| db | {sd.get('db', 'postgres')} | System of record with RLS | - |",
           f"| offline-store | {sd.get('offline', 'pglite')} | Device-local data and outbox | pos-web |",
           "| print-bridge | node escpos | LAN service driving printers and cash drawer | printers |",
           "| realtime | websocket | Ticket and table state fan-out per branch | pos-web, kds-web |", "",
           "## Trust boundaries", ""]
    desc = {"internet<->edge": "public clients to TLS edge; rate limits, WAF", "edge<->api": "authenticated device or staff session; request ids",
            "api<->db": "RLS by branch; app role has no DDL", "api<->payment-provider": "outbound only; secrets in api env; idempotency keys",
            "terminal<->local-print-bridge": "LAN, bridge token, print payloads only", "device<->offline-store": "device-local; encrypted at rest on tablets",
            "api<->delivery-platform": "inbound webhooks verified by signature; idempotent on event id"}
    out += [f"- **{b}**: {desc[b]}" for b in tb]
    out += ["", "## Data flows (riskiest workflows)", "",
            f"1. **Payment**: pos-web → api `POST /payments` (idempotency key) → {pay_name} terminal/gateway → approval code → api writes Payment captured, audit event → realtime → receipt job → print-bridge. Card data never crosses the pos-web or api boundary.",
            "2. **Refund**: manager PIN on pos-web → api `POST /refunds` with approver → provider refund → Refund processed, audit event → receipt; cash refunds open the drawer via print-bridge.",
            "3. **Offline sync**: pos-web writes to offline-store outbox → on reconnect `POST /sync/push` in seq order → api applies conflict rules (LWW per field, payments append-only) → `GET /sync/pull` returns server changes and receipt blocks → conflicts to sync-status.",
            "", "## Scaling and limits", "",
            f"- Concurrent terminals per branch: {(pack.get('nfr_defaults') or {}).get('concurrent_terminals_min', 3)} minimum; websocket rooms per branch.",
            "- One Postgres primary handles 100 branches at typical POS volume (hundreds of orders per branch per day).",
            "- Sync push batches of 500 events; queue drains within 60 s on reconnect.",
            "- Fiscal reporting queue is independent so a regulator outage never blocks ordering.", "",
            "## Cost estimate", "", "| Branches | Compute | Database | Other | Monthly (USD, order of magnitude) |", "|---------:|---------|----------|-------|-----------------------------------|",
            "| 1 | 1 small VM or Fly app | managed Postgres small | error tracking free tier | 40–80 |",
            "| 10 | 2 VMs | managed Postgres medium + backups | error tracking, uptime | 200–400 |",
            "| 100 | autoscaled api ×4, realtime ×2 | Postgres large + replica | observability, CDN | 1500–3000 |", ""]
    return "\n".join(out)


def run_arch_skeleton(project: Path, root: Path) -> int:
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    dp = project / ".foundry" / "domain.yaml"
    domain = F.parse_yaml(dp.read_text(encoding="utf-8")) if dp.exists() else None
    adrs, arch = arch_skeleton(pack, ledger, domain)
    adr_dir = project / ".foundry" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)
    slugs = {"0001": "stack", "0002": "auth-sessions", "0003": "tenancy-branches", "0004": "data-store-migrations", "0005": "offline-sync",
             "0006": "integrations-boundary", "0007": "deployment-environments", "0008": "observability", "0009": "i18n-rtl"}
    for idn, text in adrs.items():
        (adr_dir / f"{idn}-{slugs[idn]}.md").write_text(text, encoding="utf-8", newline="\n")
    (project / ".foundry" / "architecture.md").write_text(arch, encoding="utf-8", newline="\n")
    print(f"arch-skeleton: {len(adrs)} ADRs -> .foundry/adr/, architecture.md ({'CBM present' if cbm_present() else 'CBM absent, manage_adr skipped'})")
    return 0


def gate_architecture(project: Path, root: Path) -> list[str]:
    errs = gate_domain(project, root)
    if errs:
        return errs
    adr_dir = project / ".foundry" / "adr"
    schema = F.load_schema("adr.schema.json", root / "schemas")
    found: dict[str, Path] = {}
    for p in sorted(adr_dir.glob("*.md")) if adr_dir.exists() else []:
        m = re.match(r"^(\d{4})-", p.name)
        if m:
            found[m.group(1)] = p
    for idn in ADR_IDS:
        p = found.get(idn)
        if p is None:
            errs.append(f"ADR {idn} missing under .foundry/adr/")
            continue
        text = p.read_text(encoding="utf-8")
        try:
            fm_text, _, body = F.split_frontmatter(text)
            fm = F.parse_yaml(fm_text)
        except F.YamlError as e:
            errs.append(f"{p.name}: frontmatter {e}")
            continue
        errs += [f"{p.name}: {m}" for m in F.validate_schema(fm, schema)]
        if fm.get("status") != "accepted":
            errs.append(f"{p.name}: status is {fm.get('status')}, not accepted")
        if not fm.get("decision_refs") and "pack-default" not in body:
            errs.append(f"{p.name}: cites no [D:] and does not say pack-default")
        if len(text.splitlines()) > 60:
            errs.append(f"{p.name}: {len(text.splitlines())} lines; max 60")
    ap = project / ".foundry" / "architecture.md"
    if not ap.exists():
        return errs + [f"{ap} missing"]
    try:
        fm_text, _, body = F.split_frontmatter(ap.read_text(encoding="utf-8"))
        fm = F.parse_yaml(fm_text)
    except F.YamlError as e:
        return errs + [f"architecture.md: frontmatter {e}"]
    errs += [f"architecture.md: {m}" for m in F.validate_schema(fm, F.load_schema("architecture-frontmatter.schema.json", root / "schemas"))]
    tb_section = body.split("## Trust boundaries", 1)[1].split("\n## ", 1)[0] if "## Trust boundaries" in body else ""
    if len(re.findall(r"^- \*\*", tb_section, re.M)) < 5:
        errs.append("architecture.md: fewer than 5 trust boundaries listed")
    with (root / "data" / "stacks.csv").open(encoding="utf-8", newline="") as fh:
        ids = {r["stack_id"] for r in csv.DictReader(fh)}
    if fm.get("stack_id") not in ids:
        errs.append(f"architecture.md: stack_id '{fm.get('stack_id')}' not in data/stacks.csv")
    return errs


# ----------------------------------------------------------------------------- phase 6: data model
def _prisma_type(field: str, entity_names: set[str], minor: int) -> tuple[str, str | None]:
    """Return (prisma type, related entity or None)."""
    f = field.lower()
    if f == "id":
        return "String @id @default(uuid()) @db.Uuid", None
    if f.endswith("_id"):
        base = f[:-3]
        target = next((e for e in entity_names if _snake(e) == base), None)
        return ("String @db.Uuid", target)
    if f.endswith("_ids") or f in ("permissions", "components", "lines", "branch_ids"):
        return "Json", None
    if f.endswith("_at"):
        return "DateTime?", None
    if f in ("qty", "count", "seq", "device_seq", "covers", "number", "sequence", "seats", "max_qty", "min_select", "max_select", "yield", "age_seconds", "party_size", "x", "y"):
        return "Int", None
    if any(k in f for k in ("price", "total", "amount", "delta", "balance", "float", "variance", "cost", "rate", "pct", "on_hand", "par_level", "subtotal", "tax", "charge", "points", "opening", "closing", "expected")):
        return f"Decimal @db.Decimal(12, {minor})", None
    if f.startswith("is_") or f in ("opens_drawer", "required", "inclusive", "must", "requires_pin"):
        return "Boolean @default(false)", None
    if f in ("payload", "fiscal_qr", "modifiers", "notes"):
        return "Json" if f == "payload" else "String?", None
    return "String", None


def schema_skeleton(domain: dict, pack: dict, ledger: dict, orm: str = "prisma") -> str:
    minor = _minor_units(ledger, pack)
    names = {e["name"] for e in domain["entities"]}
    if orm == "drizzle":
        return _drizzle_schema(domain, minor, names)
    out = ["// Generated by foundry.py schema-skeleton from .foundry/domain.yaml. Refine, do not hand-write from scratch.",
           "generator client {", "  provider = \"prisma-client-js\"", "}", "", "datasource db {", "  provider = \"postgresql\"", "  url      = env(\"DATABASE_URL\")", "}", ""]
    for e in domain["entities"]:
        if e["states"]:
            out.append(f"enum {e['name']}State {{")
            out += [f"  {re.sub(r'[^A-Za-z0-9]', '_', s).upper()}" for s in e["states"]]
            out += ["}", ""]
    relations: dict[str, list[str]] = {n: [] for n in names}
    for e in domain["entities"]:
        for f in e["fields"]:
            _, target = _prisma_type(f, names, minor)
            if target and target != e["name"]:
                relations[target].append(e["name"])
    for e in domain["entities"]:
        name = e["name"]
        out.append(f"model {name} {{")
        out.append("  id         String   @id @default(uuid()) @db.Uuid")
        fields_seen = {"id"}
        for f in e["fields"]:
            if f in fields_seen:
                continue
            fields_seen.add(f)
            ptype, target = _prisma_type(f, names, minor)
            out.append(f"  {f:<10} {ptype}")
            if target and target != name:
                out.append(f"  {_snake(target):<10} {target} @relation(fields: [{f}], references: [id])")
        if e["states"]:
            out.append(f"  state      {name}State @default({re.sub(r'[^A-Za-z0-9]', '_', e['states'][0]).upper()})")
        if "branch_id" not in fields_seen and name not in ("Branch", "Role", "Tenant", "User") and "Branch" in names:
            out.append("  branch_id  String?  @db.Uuid")
        out.append("  created_at DateTime @default(now())")
        out.append("  updated_at DateTime @updatedAt")
        if e["owned_by"] in ("ordering", "payments", "people"):
            out.append("  deleted_at DateTime?")
        for child in relations.get(name, []):
            out.append(f"  {_snake(child)}s {child}[]")
        idx = "[branch_id, created_at]" if ("branch_id" in fields_seen or ("Branch" in names and name not in ("Branch", "Role", "Tenant", "User"))) else "[created_at]"
        out.append(f"  @@index({idx})")
        out.append(f"  @@map(\"{_snake(name)}s\")")
        out += ["}", ""]
    return "\n".join(out)


def _drizzle_schema(domain: dict, minor: int, names: set[str]) -> str:
    out = ["// Generated by foundry.py schema-skeleton --orm drizzle from .foundry/domain.yaml",
           "import { pgTable, pgEnum, uuid, text, integer, numeric, boolean, timestamp, jsonb, index } from \"drizzle-orm/pg-core\";", ""]
    for e in domain["entities"]:
        if e["states"]:
            out.append(f"export const {_snake(e['name'])}State = pgEnum(\"{_snake(e['name'])}_state\", [{', '.join(F._yq(s) for s in e['states'])}]);")
    out.append("")
    for e in domain["entities"]:
        t = _snake(e["name"]) + "s"
        out.append(f"export const {t} = pgTable(\"{t}\", {{")
        out.append("  id: uuid(\"id\").primaryKey().defaultRandom(),")
        for f in e["fields"]:
            if f == "id":
                continue
            ptype, _ = _prisma_type(f, names, minor)
            if ptype.startswith("String") and "Uuid" in ptype:
                col = f"uuid(\"{f}\")"
            elif ptype.startswith("Int"):
                col = f"integer(\"{f}\")"
            elif ptype.startswith("Decimal"):
                col = f"numeric(\"{f}\", {{ precision: 12, scale: {minor} }})"
            elif ptype.startswith("Boolean"):
                col = f"boolean(\"{f}\").default(false)"
            elif ptype.startswith("DateTime"):
                col = f"timestamp(\"{f}\")"
            elif ptype == "Json":
                col = f"jsonb(\"{f}\")"
            else:
                col = f"text(\"{f}\")"
            out.append(f"  {f}: {col},")
        if e["states"]:
            out.append(f"  state: {_snake(e['name'])}State(\"state\").notNull(),")
        out.append("  createdAt: timestamp(\"created_at\").defaultNow().notNull(),")
        out.append("  updatedAt: timestamp(\"updated_at\").defaultNow().notNull(),")
        out.append(f"}}, (t) => [index(\"{t}_created_idx\").on(t.createdAt)]);")
        out.append("")
    return "\n".join(out)


def run_schema_skeleton(project: Path, root: Path, orm: str) -> int:
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    domain = F.parse_yaml((project / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
    text = schema_skeleton(domain, pack, ledger, orm)
    if orm == "prisma":
        out = project / "prisma" / "schema.prisma"
    else:
        out = project / "db" / "schema.ts"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    mig = project / "migrations" / "README.md"
    mig.parent.mkdir(parents=True, exist_ok=True)
    with (root / "data" / "stacks.csv").open(encoding="utf-8", newline="") as fh:
        row = next((r for r in csv.DictReader(fh) if r["stack_id"] == orm), None)
    mig.write_text(f"# Migrations\n\nORM: {orm}. Schema: `{out.relative_to(project).as_posix()}`.\n\nValidate: `{row['test_cmd'] if row else ''}`\n\nMigrate: {row['notes'] if row else 'see stacks.csv'}\n\nRule: one migration per ticket; never edit an applied migration; money columns keep Decimal(12,{_minor_units(ledger, pack)}).\n", encoding="utf-8", newline="\n")
    print(f"schema-skeleton: {len(domain['entities'])} models -> {out.relative_to(project).as_posix()}, migrations/README.md")
    return 0


def _npx_available(pkg_bin: str) -> bool:
    if not shutil.which("npx"):
        return False
    try:
        r = subprocess.run(["npx", "--no-install", pkg_bin, "--version"], capture_output=True, text=True, timeout=60, shell=(sys.platform == "win32"))
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def gate_data(project: Path, root: Path) -> list[str]:
    errs = gate_architecture(project, root)
    if errs:
        return errs
    domain = F.parse_yaml((project / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
    prisma = project / "prisma" / "schema.prisma"
    drizzle = project / "db" / "schema.ts"
    if prisma.exists():
        text = prisma.read_text(encoding="utf-8")
        models = set(re.findall(r"^model (\w+) \{", text, re.M))
        enums = set(re.findall(r"^enum (\w+) \{", text, re.M))
        for e in domain["entities"]:
            if e["name"] not in models:
                errs.append(f"schema.prisma: no model for entity {e['name']}")
            if e["states"] and f"{e['name']}State" not in enums:
                errs.append(f"schema.prisma: no enum {e['name']}State")
        if text.count("{") != text.count("}"):
            errs.append("schema.prisma: unbalanced braces")
        if not errs and _npx_available("prisma"):
            r = subprocess.run(["npx", "--no-install", "prisma", "validate", "--schema", str(prisma)], capture_output=True, text=True, timeout=120, shell=(sys.platform == "win32"))
            if r.returncode != 0:
                errs.append("npx prisma validate failed: " + (r.stderr or r.stdout).strip().splitlines()[-1][:200])
    elif drizzle.exists():
        text = drizzle.read_text(encoding="utf-8")
        for e in domain["entities"]:
            if f"export const {_snake(e['name'])}s = pgTable" not in text:
                errs.append(f"schema.ts: no table for entity {e['name']}")
    else:
        errs.append("no prisma/schema.prisma or db/schema.ts")
    return errs


# ----------------------------------------------------------------------------- phase 6: API
ERROR_SCHEMA = {"type": "object", "required": ["code", "message"], "properties": {"code": {"type": "string"}, "message": {"type": "string"}, "request_id": {"type": "string"}, "details": {"type": "array", "items": {"type": "object"}}}}


def _job_op(job: dict, entity_for_job: str | None) -> tuple[str, str]:
    """(path, operationId) for a job operation."""
    jid = job["id"]
    if entity_for_job:
        base = _plural(_kebab(entity_for_job))
        return f"/{base}/{{id}}/{jid}", f"{_snake(entity_for_job)}_{jid.replace('-', '_')}"
    return f"/jobs/{jid}", f"job_{jid.replace('-', '_')}"


def _entity_for_job(jid: str, entity_names: list[str]) -> str | None:
    toks = set(jid.split("-"))
    hints = {"order": "Order", "orders": "Order", "kds": "KitchenTicket", "bump": "KitchenTicket", "kitchen": "KitchenTicket", "payment": "Payment", "refund": "Refund",
             "receipt": "Receipt", "shift": "Shift", "menu": "MenuItem", "table": "Table", "tables": "Table", "floor": "Table", "reservations": "Reservation",
             "inventory": "InventoryItem", "purchasing": "InventoryItem", "delivery": "Order", "reports": "Order", "staff": "Staff", "branch": "Branch",
             "loyalty": "Customer", "offline": "SyncEvent", "sync": "SyncEvent", "discount": "Discount", "tips": "Payment", "split": "Order", "merge": "Table",
             "hold": "OrderLine", "void": "OrderLine", "comp": "OrderLine", "modify": "OrderLine", "send": "Order", "take": "Order", "end": "Shift", "day": "Shift",
             "print": "Receipt", "record": "Record", "records": "Record", "sign": "User", "administer": "Role", "audit": "AuditEvent", "overview": "Record", "run": "Record",
             "onboard": "Account", "fund": "Transaction", "trade": "Order", "monitor": "Position", "comply": "Account", "sell": "Sale", "stock": "Variant", "return": "Return", "close": "Shift"}
    for t in jid.split("-"):
        if t in hints and hints[t] in entity_names:
            return hints[t]
    for e in entity_names:
        if set(F._norm(_kebab(e)).split()) & toks:
            return e
    return None


def api_skeleton(domain: dict, pack: dict, ledger: dict) -> tuple[dict, dict]:
    names = [e["name"] for e in domain["entities"]]
    personas = pack.get("personas") or ["staff"]
    admin = "owner" if "owner" in personas else personas[-1]
    paths: dict[str, Any] = {}
    schemas: dict[str, Any] = {"Error": ERROR_SCHEMA, "Page": {"type": "object", "properties": {"next_cursor": {"type": ["string", "null"]}}}}
    resp_err = {"description": "Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}

    def responses(ok: str = "200", ref: str | None = None, etag: bool = False) -> dict:
        r: dict[str, Any] = {ok: {"description": "OK"}, "400": resp_err, "401": resp_err, "403": resp_err, "404": resp_err, "409": resp_err}
        if ref:
            r[ok]["content"] = {"application/json": {"schema": {"$ref": f"#/components/schemas/{ref}"}}}
        if etag:
            r[ok]["headers"] = {"ETag": {"schema": {"type": "string"}}}
        return r

    minor = _minor_units(ledger, pack)
    for e in domain["entities"]:
        props: dict[str, Any] = {"id": {"type": "string", "format": "uuid"}}
        for f in e["fields"]:
            t, _ = _prisma_type(f, set(names), minor)
            props[f] = {"type": "string", "format": "uuid"} if "Uuid" in t else {"type": "integer"} if t.startswith("Int") else {"type": "string", "pattern": "^-?[0-9]+(\\.[0-9]+)?$", "description": f"decimal, {minor} minor units"} if t.startswith("Decimal") else {"type": "boolean"} if t.startswith("Boolean") else {"type": "string", "format": "date-time"} if t.startswith("DateTime") else {"type": "object"} if t == "Json" else {"type": "string"}
        if e["states"]:
            props["state"] = {"type": "string", "enum": e["states"]}
        props["created_at"] = {"type": "string", "format": "date-time"}
        props["updated_at"] = {"type": "string", "format": "date-time"}
        schemas[e["name"]] = {"type": "object", "properties": props}
        schemas[f"{e['name']}Page"] = {"type": "object", "properties": {"items": {"type": "array", "items": {"$ref": f"#/components/schemas/{e['name']}"}}, "next_cursor": {"type": ["string", "null"]}}}
        base = f"/{_plural(_kebab(e['name']))}"
        sn = _snake(e["name"])
        offline = e["owned_by"] in ("ordering", "kitchen", "menu")
        actor = next((t["by"] for t in e["transitions"]), personas[0])
        xf = lambda job, authz, idem, audit: {"job": job, "personas": [actor, admin] if actor != admin else [admin], "authz": authz, "idempotent": idem, "offline_capable": offline, "audit": audit}
        paths[base] = {
            "get": {"operationId": f"{sn}_list", "summary": f"List {e['name']}", "parameters": [{"name": "cursor", "in": "query", "schema": {"type": "string"}}, {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 25, "maximum": 200}}, {"name": "branch_id", "in": "query", "schema": {"type": "string", "format": "uuid"}}],
                    "responses": responses("200", f"{e['name']}Page"), "x-foundry": xf("read", f"role in [{actor}, {admin}] and branch scope", True, False)},
            "post": {"operationId": f"{sn}_create", "summary": f"Create {e['name']}", "parameters": [{"name": "Idempotency-Key", "in": "header", "required": True, "schema": {"type": "string"}}],
                     "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{e['name']}"}}}},
                     "responses": responses("201", e["name"], etag=True), "x-foundry": xf("create", f"role in [{actor}, {admin}] and branch scope", True, True)},
        }
        paths[f"{base}/{{id}}"] = {
            "get": {"operationId": f"{sn}_get", "summary": f"Get {e['name']}", "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string", "format": "uuid"}}],
                    "responses": responses("200", e["name"], etag=True), "x-foundry": xf("read", f"role in [{actor}, {admin}] and same branch", True, False)},
            "patch": {"operationId": f"{sn}_update", "summary": f"Update {e['name']}", "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string", "format": "uuid"}}, {"name": "If-Match", "in": "header", "required": True, "schema": {"type": "string"}}],
                      "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{e['name']}"}}}},
                      "responses": responses("200", e["name"], etag=True), "x-foundry": xf("update", f"role in [{actor}, {admin}] and same branch; state guards per domain.yaml", True, True)},
            "delete": {"operationId": f"{sn}_archive", "summary": f"Archive {e['name']}", "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string", "format": "uuid"}}],
                       "responses": responses("204"), "x-foundry": xf("archive", f"role == {admin}", True, True)},
        }
    job_ops = 0
    for j in pack.get("jobs") or []:
        ent = _entity_for_job(j["id"], names)
        path, opid = _job_op(j, ent)
        params = [{"name": "id", "in": "path", "required": True, "schema": {"type": "string", "format": "uuid"}}] if "{id}" in path else []
        params.append({"name": "Idempotency-Key", "in": "header", "required": True, "schema": {"type": "string"}})
        paths.setdefault(path, {})["post"] = {"operationId": opid, "summary": j["id"].replace("-", " "), "parameters": params,
                                              "requestBody": {"required": False, "content": {"application/json": {"schema": {"type": "object"}}}},
                                              "responses": responses("200", ent) if ent else responses("200"),
                                              "x-foundry": {"job": j["id"], "personas": [j.get("persona") or personas[0]], "authz": f"role == {j.get('persona') or personas[0]} or role == {admin}; branch scope; manager PIN when the job guards it",
                                                            "idempotent": True, "offline_capable": bool(ent and _context_for(ent) in ("ordering", "kitchen", "menu")), "audit": True}}
        job_ops += 1
    sync_ok = {"200": {"description": "OK", "content": {"application/json": {"schema": {"type": "object"}}}}, "400": resp_err, "401": resp_err, "409": resp_err}
    paths["/sync/push"] = {"post": {"operationId": "sync_push", "summary": "Push device outbox events in sequence order", "parameters": [{"name": "Idempotency-Key", "in": "header", "required": True, "schema": {"type": "string"}}],
                                    "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object", "properties": {"device_id": {"type": "string"}, "events": {"type": "array", "items": {"type": "object", "properties": {"seq": {"type": "integer"}, "entity": {"type": "string"}, "payload": {"type": "object"}}}}}}}}},
                                    "responses": sync_ok, "x-foundry": {"job": "offline-sync", "personas": ["cashier"], "authz": "device token; branch of the device", "idempotent": True, "offline_capable": False, "audit": True}}}
    paths["/sync/pull"] = {"get": {"operationId": "sync_pull", "summary": "Pull server changes since a device sequence", "parameters": [{"name": "since_seq", "in": "query", "schema": {"type": "integer"}}, {"name": "device_id", "in": "query", "required": True, "schema": {"type": "string"}}],
                                   "responses": sync_ok, "x-foundry": {"job": "offline-sync", "personas": ["cashier"], "authz": "device token; branch of the device", "idempotent": True, "offline_capable": False, "audit": False}}}
    for cat, providers in (pack.get("integrations") or {}).items():
        if cat in ("payments", "delivery", "einvoicing"):
            paths[f"/webhooks/{cat}/{{provider}}"] = {"post": {"operationId": f"webhook_{cat}", "summary": f"Inbound {cat} webhook", "parameters": [{"name": "provider", "in": "path", "required": True, "schema": {"type": "string", "enum": [p for p in providers if p not in ("cash", "tablet-fallback")]}}],
                                                              "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object"}}}}, "responses": sync_ok,
                                                              "x-foundry": {"job": f"{cat}-webhook", "personas": ["system"], "authz": "provider signature verified; idempotent on (provider, event_id)", "idempotent": True, "offline_capable": False, "audit": True}}}
    spec = {"openapi": "3.1.0", "info": {"title": f"{pack['name']} API", "version": "0.1.0", "description": f"Generated by foundry.py api-skeleton. Pack {pack['slug']}, ledger {F.decisions_hash(ledger)}."},
            "servers": [{"url": "/api/v1"}], "paths": paths, "components": {"schemas": schemas, "securitySchemes": {"deviceToken": {"type": "http", "scheme": "bearer"}, "staffSession": {"type": "apiKey", "in": "cookie", "name": "session"}}},
            "security": [{"deviceToken": []}, {"staffSession": []}]}
    events = {"pack": pack["slug"], "events": [{"name": ev["name"], "producer": ev["producer"], "payload": f"#/components/schemas/{ev['entity']}", "consumers": ev["consumers"]} for ev in domain["events"]]}
    return spec, events


def dump_block_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for k, v in value.items():
            key = k if re.fullmatch(r"[A-Za-z0-9_./{}\-]+", str(k)) and not str(k).startswith("-") and not str(k).isdigit() else F._yq(str(k))
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{pad}{key}:")
                lines.append(dump_block_yaml(v, indent + 2))
            else:
                lines.append(f"{pad}{key}: {dump_block_yaml(v, indent + 2)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return "[]"
        lines = []
        for item in value:
            if isinstance(item, dict) and item:
                inner = dump_block_yaml(item, indent + 2)
                first, _, rest = inner.partition("\n")
                lines.append(f"{pad}- {first.strip()}" + (("\n" + rest) if rest else ""))
            else:
                lines.append(f"{pad}- {dump_block_yaml(item, indent + 2)}")
        return "\n".join(lines)
    return F._yq(value)


def run_api_skeleton(project: Path, root: Path) -> int:
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    ledger = F.load_ledger(project, sel["chosen"])
    domain = F.parse_yaml((project / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
    spec, events = api_skeleton(domain, pack, ledger)
    (project / "openapi.yaml").write_text(dump_block_yaml(spec) + "\n", encoding="utf-8", newline="\n")
    (project / ".foundry" / "events.yaml").write_text(F.dump_yaml(events), encoding="utf-8", newline="\n")
    ops = sum(1 for p in spec["paths"].values() for m in p if m in ("get", "post", "patch", "delete"))
    print(f"api-skeleton: {len(spec['paths'])} paths, {ops} operations -> openapi.yaml; {len(events['events'])} events -> .foundry/events.yaml")
    return 0


def gate_api(project: Path, root: Path) -> list[str]:
    errs = gate_data(project, root)
    if errs:
        return errs
    op = project / "openapi.yaml"
    ep = project / ".foundry" / "events.yaml"
    if not op.exists():
        return ["openapi.yaml missing"]
    try:
        spec = F.parse_yaml(op.read_text(encoding="utf-8"))
    except F.YamlError as e:
        return [f"openapi.yaml: {e}"]
    if not str(spec.get("openapi", "")).startswith("3.1"):
        errs.append("openapi.yaml: openapi version is not 3.1.x")
    paths = spec.get("paths") or {}
    if not paths:
        errs.append("openapi.yaml: no paths")
    domain = F.parse_yaml((project / ".foundry" / "domain.yaml").read_text(encoding="utf-8"))
    sel = F.load_selection(project)
    pack = F.load_pack(root, sel["chosen"])
    opids: dict[str, int] = {}
    jobs_seen: set[str] = set()
    for path, methods in paths.items():
        for m, op_ in (methods or {}).items():
            if m not in ("get", "post", "put", "patch", "delete"):
                continue
            oid = op_.get("operationId")
            if not oid:
                errs.append(f"{m.upper()} {path}: missing operationId")
            opids[oid] = opids.get(oid, 0) + 1
            xf = op_.get("x-foundry") or {}
            if not xf.get("authz"):
                errs.append(f"{m.upper()} {path}: x-foundry.authz missing")
            if xf.get("job"):
                jobs_seen.add(xf["job"])
            codes = {str(c) for c in (op_.get("responses") or {})}
            if not (codes & {"200", "201", "204"}):
                errs.append(f"{m.upper()} {path}: no 2xx response")
            if not any(c.startswith("4") for c in codes):
                errs.append(f"{m.upper()} {path}: no 4xx response")
    for oid, n in opids.items():
        if n > 1:
            errs.append(f"operationId '{oid}' used {n} times")
    for e in domain["entities"]:
        base = f"/{_plural(_kebab(e['name']))}"
        if not any(str(p).startswith(base) for p in paths):
            errs.append(f"entity {e['name']} has no path under {base}")
    for j in pack.get("jobs") or []:
        if j["id"] not in jobs_seen:
            errs.append(f"job {j['id']} has no operation (x-foundry.job)")
    if not ep.exists():
        errs.append(".foundry/events.yaml missing")
    else:
        try:
            ev = F.parse_yaml(ep.read_text(encoding="utf-8"))
            errs += [f"events.yaml: {m}" for m in F.validate_schema(ev, F.load_schema("events.schema.json", root / "schemas"))]
        except F.YamlError as e:
            errs.append(f"events.yaml: {e}")
    if not errs and _npx_available("redocly"):
        r = subprocess.run(["npx", "--no-install", "redocly", "lint", str(op)], capture_output=True, text=True, timeout=180, shell=(sys.platform == "win32"))
        if r.returncode != 0:
            errs.append("redocly lint failed: " + (r.stderr or r.stdout).strip().splitlines()[-1][:200])
    return errs


GATES = {"domain": gate_domain, "architecture": gate_architecture, "data": gate_data, "api": gate_api}
