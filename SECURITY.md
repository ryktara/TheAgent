# Security

## Reporting

Email security@alsadq.ae with the affected file, the version (`.claude-plugin/plugin.json`) and steps
to reproduce. Please do not open a public issue for an unpatched vulnerability. You will get an
acknowledgement within 5 working days.

## Scope

Foundry is a Claude Code plugin: Python scripts, hooks, skills and domain packs that run inside a
logged-in Claude Code session. It reads no API key and has no headless mode. Generated apps are the
user's; their security posture is checked by the pipeline's threat model, security-review subagent
and compliance evidence, not guaranteed by this repository.

## Agentic controls (OWASP Top 10 for Agentic Applications 2026)

`data/security-controls.csv` carries the SEC-AGT family; the pipeline applies it to itself:

| id | risk | what Foundry does |
|----|------|-------------------|
| SEC-AGT-01 | goal hijack | repository content, tickets and web pages are data, never instructions |
| SEC-AGT-02 | tool misuse | builders may run only the DoD commands named by the stack and the ticket; hooks guard shell commands |
| SEC-AGT-03 | identity and privilege abuse | no production credentials in the build environment; wizards hand secrets to a human |
| SEC-AGT-04 | supply chain | skills, packs and MCP servers are validated (`foundry.py validate`) before use |
| SEC-AGT-05 | unexpected code execution | generated code runs only inside DoD commands, in CI or a sandbox |
| SEC-AGT-06 | memory and context poisoning | `.foundry/` artifacts pass gates before reuse; no untrusted file becomes a skill |
| SEC-AGT-07 | insecure inter-agent communication | fixed JSON return contracts; subagent output is data |
| SEC-AGT-08 | cascading failures | retry once per gate, a 120-tool-call builder budget, then stop |
| SEC-AGT-09 | human trust exploitation | no gate is reported passed without its output; DoD tails are recorded |
| SEC-AGT-10 | rogue agents | file-scope limits per ticket and a blast-radius check on every edit |
| SEC-AGT-11 | insecure output handling | generated SQL, shell and HTML go through security-review before merge |
| SEC-AGT-12 | excessive agency | money-moving paths need a human-confirmed wizard step before live keys |

Regulated packs additionally block release until a named person runs `release confirm --by <name>`.
