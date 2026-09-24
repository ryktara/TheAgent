# Compliance evidence plan

| Control | Source | Evidence by | Status |
|---------|--------|-------------|--------|
| `C-ALL-01` | pack compliance.md | owner review of apps/api/src/payments/ (no PAN fields) + semgrep ruleset | planned |
| `C-ALL-02` | pack compliance.md | apps/api/src/receipts/numbering.test.ts | planned |
| `C-ALL-03` | pack compliance.md | apps/api/src/audit/audit-events.test.ts | planned |
| `C-ALL-04` | pack compliance.md | apps/api/src/tax/vat-sa.test.ts | planned |
| `C-ALL-05` | pack compliance.md | apps/api/src/reports/export.e2e.test.ts + retention config review | planned |
| `C-ALL-06` | pack compliance.md | apps/api/src/labels/label-price.test.ts | planned |
| `C-ALL-07` | pack compliance.md | apps/api/src/receipts/receipt-policy.fixture.test.ts | planned |
| `C-ALL-08` | pack compliance.md | apps/api/src/promotions/promo-vs-label.test.ts + apps/api/src/auth/pin-lockout.test.ts | planned |
| `C-ALL-09` | pack compliance.md | apps/api/src/customers/pdpl-export-delete.test.ts | planned |
| `C-ALL-10` | pack compliance.md | docs/runbooks/backup-restore.md + restore drill record | planned |
| `C-SA-01` | pack compliance.md | apps/api/src/einvoice/zatca-qr.test.ts | planned |
| `C-SA-02` | pack compliance.md | apps/api/src/einvoice/fatoora-sandbox.int.test.ts | planned |
| `C-SA-03` | pack compliance.md | apps/api/src/returns/refund-amount.test.ts | planned |
| `C-SA-04` | pack compliance.md | apps/api/src/receipts/bilingual-receipt.fixture.test.ts | planned |
| `SEC-AUTH-01` | ASVS-5.0 V6.2 | apps/api/src/security/auth/sec-auth-01.test.ts | planned |
| `SEC-AUTH-02` | ASVS-5.0 V6.2 | apps/api/src/security/auth/sec-auth-02.test.ts | planned |
| `SEC-AUTH-03` | ASVS-5.0 V6.2 | owner review: docs/security/auth.md#sec-auth-03 | planned |
| `SEC-AUTH-04` | ASVS-5.0 V6.3 | apps/api/src/security/auth/sec-auth-04.test.ts | planned |
| `SEC-AUTH-05` | foundry | apps/api/src/security/auth/sec-auth-05.test.ts | planned |
| `SEC-AUTH-06` | ASVS-5.0 V6.4 | apps/api/src/security/auth/sec-auth-06.test.ts | planned |
| `SEC-AUTH-07` | ASVS-5.0 V6.3 | apps/api/src/security/auth/sec-auth-07.test.ts | planned |
| `SEC-AUTH-08` | ASVS-5.0 V6.4 | apps/api/src/security/auth/sec-auth-08.test.ts | planned |
| `SEC-AUTH-09` | ASVS-5.0 V6.3 | apps/api/src/security/auth/sec-auth-09.test.ts | planned |
| `SEC-AUTH-11` | foundry | apps/api/src/security/auth/sec-auth-11.test.ts | planned |
| `SEC-AUTH-12` | foundry | owner review: docs/security/auth.md#sec-auth-12 | planned |
| `SEC-AUTH-13` | ASVS-5.0 V6.4 | owner review: docs/security/auth.md#sec-auth-13 | planned |
| `SEC-AUTH-14` | ASVS-5.0 V6.4 | owner review: docs/security/auth.md#sec-auth-14 | planned |
| `SEC-SESS-01` | ASVS-5.0 V7.2 | owner review: docs/security/sess.md#sec-sess-01 | planned |
| `SEC-SESS-02` | ASVS-5.0 V7.4 | apps/api/src/security/sess/sec-sess-02.test.ts | planned |
| `SEC-SESS-03` | ASVS-5.0 V7.3 | apps/api/src/security/sess/sec-sess-03.test.ts | planned |
| `SEC-SESS-04` | ASVS-5.0 V7.3 | apps/api/src/security/sess/sec-sess-04.test.ts | planned |
| `SEC-SESS-05` | ASVS-5.0 V7.3 | apps/api/src/security/sess/sec-sess-05.test.ts | planned |
| `SEC-SESS-06` | foundry | apps/api/src/security/sess/sec-sess-06.test.ts | planned |
| `SEC-SESS-07` | ASVS-5.0 V7.5 | apps/api/src/security/sess/sec-sess-07.test.ts | planned |
| `SEC-SESS-08` | ASVS-5.0 V7.4 | semgrep ruleset + npm audit in CI | planned |
| `SEC-ACC-01` | ASVS-5.0 V8.1 | apps/api/src/security/acc/sec-acc-01.test.ts | planned |
| `SEC-ACC-02` | OWASP-API-Top10-2023 API1 | apps/api/src/security/acc/sec-acc-02.test.ts | planned |
| `SEC-ACC-03` | OWASP-API-Top10-2023 API5 | apps/api/src/security/acc/sec-acc-03.test.ts | planned |
| `SEC-ACC-04` | OWASP-API-Top10-2023 API3 | apps/api/src/security/acc/sec-acc-04.test.ts | planned |
| `SEC-ACC-06` | foundry | apps/api/src/security/acc/sec-acc-06.test.ts | planned |
| `SEC-ACC-07` | ASVS-5.0 V8.1 | owner review: docs/security/acc.md#sec-acc-07 | planned |
| `SEC-ACC-09` | ASVS-5.0 V16 | apps/api/src/security/acc/sec-acc-09.test.ts | planned |
| `SEC-ACC-10` | ASVS-5.0 V8.1 | owner review: docs/security/acc.md#sec-acc-10 | planned |
| `SEC-IN-01` | ASVS-5.0 V2.1 | apps/api/src/security/in/sec-in-01.test.ts | planned |
| `SEC-IN-02` | ASVS-5.0 V2.1 | apps/api/src/security/in/sec-in-02.test.ts | planned |
| `SEC-IN-03` | ASVS-5.0 V1.2 | semgrep ruleset + npm audit in CI | planned |
| `SEC-IN-04` | ASVS-5.0 V1.2 | semgrep ruleset + npm audit in CI | planned |
| `SEC-IN-07` | foundry | apps/api/src/security/in/sec-in-07.test.ts | planned |
| `SEC-IN-08` | foundry | apps/api/src/security/in/sec-in-08.test.ts | planned |
| `SEC-IN-09` | ASVS-5.0 V1.5 | semgrep ruleset + npm audit in CI | planned |
| `SEC-IN-10` | ASVS-5.0 V2.1 | apps/api/src/security/in/sec-in-10.test.ts | planned |
| `SEC-CRY-01` | ASVS-5.0 V12 | semgrep ruleset + npm audit in CI | planned |
| `SEC-CRY-02` | ASVS-5.0 V11 | owner review: docs/security/cry.md#sec-cry-02 | planned |
| `SEC-CRY-03` | ASVS-5.0 V13 | semgrep ruleset + npm audit in CI | planned |
| `SEC-CRY-04` | ASVS-5.0 V11 | semgrep ruleset + npm audit in CI | planned |
| `SEC-CRY-06` | ASVS-5.0 V11 | apps/api/src/security/cry/sec-cry-06.test.ts | planned |
| `SEC-CRY-07` | foundry | owner review: docs/security/cry.md#sec-cry-07 | planned |
| `SEC-DATA-01` | PCI-DSS-4.0 req 3 | semgrep ruleset + npm audit in CI | planned |
| `SEC-DATA-02` | PCI-DSS-4.0 req 3 | owner review: docs/security/data.md#sec-data-02 | planned |
| `SEC-DATA-03` | ASVS-5.0 V14 | owner review: docs/security/data.md#sec-data-03 | planned |
| `SEC-DATA-04` | ASVS-5.0 V14 | apps/api/src/security/data/sec-data-04.test.ts | planned |
| `SEC-DATA-05` | foundry | apps/api/src/security/data/sec-data-05.test.ts | planned |
| `SEC-DATA-06` | ASVS-5.0 V14 | owner review: docs/security/data.md#sec-data-06 | planned |
| `SEC-DATA-07` | foundry | apps/api/src/security/data/sec-data-07.test.ts | planned |
| `SEC-DATA-08` | ASVS-5.0 V16 | semgrep ruleset + npm audit in CI | planned |
| `SEC-DATA-09` | foundry | owner review: docs/security/data.md#sec-data-09 | planned |
| `SEC-DATA-10` | foundry | apps/api/src/security/data/sec-data-10.test.ts | planned |
| `SEC-LOG-01` | ASVS-5.0 V16 | owner review: docs/security/log.md#sec-log-01 | planned |
| `SEC-LOG-02` | ASVS-5.0 V16 | apps/api/src/security/log/sec-log-02.test.ts | planned |
| `SEC-LOG-03` | ASVS-5.0 V16 | apps/api/src/security/log/sec-log-03.test.ts | planned |
| `SEC-LOG-04` | ASVS-5.0 V16 | apps/api/src/security/log/sec-log-04.test.ts | planned |
| `SEC-LOG-05` | ASVS-5.0 V16 | semgrep ruleset + npm audit in CI | planned |
| `SEC-LOG-06` | foundry | owner review: docs/security/log.md#sec-log-06 | planned |
| `SEC-LOG-07` | foundry | owner review: docs/security/log.md#sec-log-07 | planned |
| `SEC-LOG-08` | ASVS-5.0 V16 | owner review: docs/security/log.md#sec-log-08 | planned |
| `SEC-API-01` | foundry | apps/api/src/security/api/sec-api-01.test.ts | planned |
| `SEC-API-02` | OWASP-API-Top10-2023 API4 | apps/api/src/security/api/sec-api-02.test.ts | planned |
| `SEC-API-03` | OWASP-API-Top10-2023 API3 | apps/api/src/security/api/sec-api-03.test.ts | planned |
| `SEC-API-04` | OWASP-API-Top10-2023 API10 | apps/api/src/security/api/sec-api-04.test.ts | planned |
| `SEC-API-05` | OWASP-API-Top10-2023 API10 | apps/api/src/security/api/sec-api-05.test.ts | planned |
| `SEC-API-06` | OWASP-API-Top10-2023 API7 | semgrep ruleset + npm audit in CI | planned |
| `SEC-API-07` | ASVS-5.0 V3 | apps/api/src/security/api/sec-api-07.test.ts | planned |
| `SEC-API-08` | ASVS-5.0 V3 | apps/api/src/security/api/sec-api-08.test.ts | planned |
| `SEC-API-09` | foundry | owner review: docs/security/api.md#sec-api-09 | planned |
| `SEC-API-10` | foundry | apps/api/src/security/api/sec-api-10.test.ts | planned |
| `SEC-API-11` | foundry | apps/api/src/security/api/sec-api-11.test.ts | planned |
| `SEC-API-12` | OWASP-API-Top10-2023 API10 | apps/api/src/security/api/sec-api-12.test.ts | planned |
| `SEC-API-13` | OWASP-API-Top10-2023 API6 | apps/api/src/security/api/sec-api-13.test.ts | planned |
| `SEC-CFG-01` | ASVS-5.0 V13 | owner review: docs/security/cfg.md#sec-cfg-01 | planned |
| `SEC-CFG-02` | ASVS-5.0 V13 | apps/api/src/security/cfg/sec-cfg-02.test.ts | planned |
| `SEC-CFG-03` | ASVS-5.0 V15 | semgrep ruleset + npm audit in CI | planned |
| `SEC-CFG-04` | ASVS-5.0 V13 | owner review: docs/security/cfg.md#sec-cfg-04 | planned |
| `SEC-CFG-05` | ASVS-5.0 V13 | semgrep ruleset + npm audit in CI | planned |
| `SEC-CFG-06` | ASVS-5.0 V13 | apps/api/src/security/cfg/sec-cfg-06.test.ts | planned |
| `SEC-CFG-07` | foundry | apps/api/src/security/cfg/sec-cfg-07.test.ts | planned |
| `SEC-CFG-08` | foundry | owner review: docs/security/cfg.md#sec-cfg-08 | planned |
| `SEC-SC-01` | ASVS-5.0 V15 | semgrep ruleset + npm audit in CI | planned |
| `SEC-SC-02` | ASVS-5.0 V15 | owner review: docs/security/sc.md#sec-sc-02 | planned |
| `SEC-SC-03` | ASVS-5.0 V15 | semgrep ruleset + npm audit in CI | planned |
| `SEC-SC-04` | foundry | semgrep ruleset + npm audit in CI | planned |
| `SEC-SC-05` | ASVS-5.0 V15 | owner review: docs/security/sc.md#sec-sc-05 | planned |
| `SEC-SC-06` | foundry | apps/api/src/security/sc/sec-sc-06.test.ts | planned |
| `SEC-BL-01` | ASVS-5.0 V2.3 | apps/api/src/security/bl/sec-bl-01.test.ts | planned |
| `SEC-BL-02` | foundry | apps/api/src/security/bl/sec-bl-02.test.ts | planned |
| `SEC-BL-03` | foundry | apps/api/src/security/bl/sec-bl-03.test.ts | planned |
| `SEC-BL-04` | foundry | apps/api/src/security/bl/sec-bl-04.test.ts | planned |
| `SEC-BL-05` | foundry | apps/api/src/security/bl/sec-bl-05.test.ts | planned |
| `SEC-BL-06` | foundry | apps/api/src/security/bl/sec-bl-06.test.ts | planned |
| `SEC-BL-07` | foundry | apps/api/src/security/bl/sec-bl-07.test.ts | planned |
| `SEC-BL-08` | foundry | apps/api/src/security/bl/sec-bl-08.test.ts | planned |
| `SEC-BL-09` | foundry | apps/api/src/security/bl/sec-bl-09.test.ts | planned |
| `SEC-BL-10` | foundry | apps/api/src/security/bl/sec-bl-10.test.ts | planned |
| `SEC-BL-11` | foundry | apps/api/src/security/bl/sec-bl-11.test.ts | planned |
| `SEC-BL-12` | foundry | apps/api/src/security/bl/sec-bl-12.test.ts | planned |
| `SEC-BL-13` | foundry | apps/api/src/security/bl/sec-bl-13.test.ts | planned |
| `SEC-BL-14` | foundry | apps/api/src/security/bl/sec-bl-14.test.ts | planned |
| `SEC-PAY-01` | PCI-DSS-4.0 SAQ A | owner review: docs/security/pay.md#sec-pay-01 | planned |
| `SEC-PAY-02` | PCI-DSS-4.0 req 9 | owner review: docs/security/pay.md#sec-pay-02 | planned |
| `SEC-PAY-03` | PCI-DSS-4.0 req 8 | semgrep ruleset + npm audit in CI | planned |
| `SEC-PAY-04` | foundry | apps/api/src/security/pay/sec-pay-04.test.ts | planned |
| `SEC-PAY-05` | foundry | apps/api/src/security/pay/sec-pay-05.test.ts | planned |
| `SEC-PAY-07` | foundry | apps/api/src/security/pay/sec-pay-07.test.ts | planned |
| `SEC-AGT-01` | OWASP-Agentic-Top10-2026 ASI01 | owner review: docs/security/agt.md#sec-agt-01 | planned |
| `SEC-AGT-02` | OWASP-Agentic-Top10-2026 ASI02 | owner review: docs/security/agt.md#sec-agt-02 | planned |
| `SEC-AGT-03` | OWASP-Agentic-Top10-2026 ASI03 | owner review: docs/security/agt.md#sec-agt-03 | planned |
| `SEC-AGT-04` | OWASP-Agentic-Top10-2026 ASI04 | semgrep ruleset + npm audit in CI | planned |
| `SEC-AGT-05` | OWASP-Agentic-Top10-2026 ASI05 | owner review: docs/security/agt.md#sec-agt-05 | planned |
| `SEC-AGT-06` | OWASP-Agentic-Top10-2026 ASI06 | owner review: docs/security/agt.md#sec-agt-06 | planned |
| `SEC-AGT-07` | OWASP-Agentic-Top10-2026 ASI07 | owner review: docs/security/agt.md#sec-agt-07 | planned |
| `SEC-AGT-08` | OWASP-Agentic-Top10-2026 ASI08 | owner review: docs/security/agt.md#sec-agt-08 | planned |
| `SEC-AGT-09` | OWASP-Agentic-Top10-2026 ASI09 | owner review: docs/security/agt.md#sec-agt-09 | planned |
| `SEC-AGT-10` | OWASP-Agentic-Top10-2026 ASI10 | owner review: docs/security/agt.md#sec-agt-10 | planned |
| `SEC-AGT-11` | OWASP-Agentic-Top10-2026 ASI05 | owner review: docs/security/agt.md#sec-agt-11 | planned |
| `SEC-AGT-12` | OWASP-Agentic-Top10-2026 ASI03 | owner review: docs/security/agt.md#sec-agt-12 | planned |
| `SEC-OFF-01` | foundry | apps/api/src/security/off/sec-off-01.test.ts | planned |
| `SEC-OFF-02` | foundry | apps/api/src/security/off/sec-off-02.test.ts | planned |
| `SEC-OFF-03` | foundry | apps/api/src/security/off/sec-off-03.test.ts | planned |
| `SEC-OFF-04` | foundry | apps/api/src/security/off/sec-off-04.test.ts | planned |
| `SEC-OFF-05` | foundry | apps/api/src/security/off/sec-off-05.test.ts | planned |
| `SEC-FIS-01` | foundry | apps/api/src/security/fis/sec-fis-01.test.ts | planned |
| `SEC-FIS-04` | foundry | owner review: docs/security/fis.md#sec-fis-04 | planned |
| `SEC-IN2-01` | ASVS-5.0 V1.1 | apps/api/src/security/in2/sec-in2-01.test.ts | planned |
| `SEC-IN2-02` | ASVS-5.0 V4 | apps/api/src/security/in2/sec-in2-02.test.ts | planned |
| `SEC-IN2-03` | ASVS-5.0 V1.2 | apps/api/src/security/in2/sec-in2-03.test.ts | planned |
| `SEC-IN2-05` | foundry | apps/api/src/security/in2/sec-in2-05.test.ts | planned |
| `SEC-IN2-06` | ASVS-5.0 V2.1 | apps/api/src/security/in2/sec-in2-06.test.ts | planned |
| `SEC-IN2-07` | ASVS-5.0 V2.1 | apps/api/src/security/in2/sec-in2-07.test.ts | planned |
| `SEC-IN2-08` | ASVS-5.0 V2.3 | apps/api/src/security/in2/sec-in2-08.test.ts | planned |
| `SEC-SESS2-01` | ASVS-5.0 V7.4 | owner review: docs/security/sess2.md#sec-sess2-01 | planned |
| `SEC-SESS2-02` | foundry | apps/api/src/security/sess2/sec-sess2-02.test.ts | planned |
| `SEC-SESS2-03` | foundry | apps/api/src/security/sess2/sec-sess2-03.test.ts | planned |
| `SEC-SESS2-04` | ASVS-5.0 V7.2 | apps/api/src/security/sess2/sec-sess2-04.test.ts | planned |
| `SEC-ACC2-01` | OWASP-API-Top10-2023 API1 | apps/api/src/security/acc2/sec-acc2-01.test.ts | planned |
| `SEC-ACC2-02` | ASVS-5.0 V8.1 | apps/api/src/security/acc2/sec-acc2-02.test.ts | planned |
| `SEC-ACC2-03` | OWASP-API-Top10-2023 API1 | apps/api/src/security/acc2/sec-acc2-03.test.ts | planned |
| `SEC-ACC2-04` | ASVS-5.0 V8.1 | apps/api/src/security/acc2/sec-acc2-04.test.ts | planned |
| `SEC-ACC2-05` | ASVS-5.0 V8.1 | apps/api/src/security/acc2/sec-acc2-05.test.ts | planned |
| `SEC-ACC2-06` | ASVS-5.0 V8.1 | apps/api/src/security/acc2/sec-acc2-06.test.ts | planned |
| `SEC-CRY2-01` | ASVS-5.0 V11 | owner review: docs/security/cry2.md#sec-cry2-01 | planned |
| `SEC-CRY2-02` | foundry | owner review: docs/security/cry2.md#sec-cry2-02 | planned |
| `SEC-CRY2-04` | ASVS-5.0 V9 | apps/api/src/security/cry2/sec-cry2-04.test.ts | planned |
| `SEC-CRY2-05` | ASVS-5.0 V12 | owner review: docs/security/cry2.md#sec-cry2-05 | planned |
| `SEC-DATA2-01` | ASVS-5.0 V14 | apps/api/src/security/data2/sec-data2-01.test.ts | planned |
| `SEC-DATA2-02` | ASVS-5.0 V14 | owner review: docs/security/data2.md#sec-data2-02 | planned |
| `SEC-DATA2-03` | ASVS-5.0 V14 | semgrep ruleset + npm audit in CI | planned |
| `SEC-DATA2-04` | ASVS-5.0 V14 | apps/api/src/security/data2/sec-data2-04.test.ts | planned |
| `SEC-DATA2-05` | ASVS-5.0 V14 | owner review: docs/security/data2.md#sec-data2-05 | planned |
| `SEC-LOG2-01` | foundry | owner review: docs/security/log2.md#sec-log2-01 | planned |
| `SEC-LOG2-02` | foundry | apps/api/src/security/log2/sec-log2-02.test.ts | planned |
| `SEC-LOG2-03` | foundry | owner review: docs/security/log2.md#sec-log2-03 | planned |
| `SEC-LOG2-04` | foundry | owner review: docs/security/log2.md#sec-log2-04 | planned |
| `SEC-API2-02` | foundry | apps/api/src/security/api2/sec-api2-02.test.ts | planned |
| `SEC-API2-03` | OWASP-API-Top10-2023 API4 | apps/api/src/security/api2/sec-api2-03.test.ts | planned |
| `SEC-API2-04` | ASVS-5.0 V13 | apps/api/src/security/api2/sec-api2-04.test.ts | planned |
| `SEC-API2-05` | ASVS-5.0 V4 | apps/api/src/security/api2/sec-api2-05.test.ts | planned |
| `SEC-CFG2-01` | foundry | apps/api/src/security/cfg2/sec-cfg2-01.test.ts | planned |
| `SEC-CFG2-02` | foundry | owner review: docs/security/cfg2.md#sec-cfg2-02 | planned |
| `SEC-CFG2-03` | PCI-DSS-4.0 req 6 | owner review: docs/security/cfg2.md#sec-cfg2-03 | planned |
| `SEC-CFG2-04` | ASVS-5.0 V13 | owner review: docs/security/cfg2.md#sec-cfg2-04 | planned |
| `SEC-BL2-01` | foundry | apps/api/src/security/bl2/sec-bl2-01.test.ts | planned |
| `SEC-BL2-02` | foundry | apps/api/src/security/bl2/sec-bl2-02.test.ts | planned |
| `SEC-BL2-03` | foundry | apps/api/src/security/bl2/sec-bl2-03.test.ts | planned |
| `SEC-BL2-04` | foundry | apps/api/src/security/bl2/sec-bl2-04.test.ts | planned |
| `SEC-BL2-05` | foundry | apps/api/src/security/bl2/sec-bl2-05.test.ts | planned |
| `SEC-BL2-06` | foundry | apps/api/src/security/bl2/sec-bl2-06.test.ts | planned |
