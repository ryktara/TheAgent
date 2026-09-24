"""File templates for `foundry.py scaffold --stack nextjs-pwa` (T-000). Placeholders: __APP_NAME__, __PACK__."""

TEMPLATES: dict[str, str] = {}

TEMPLATES["package.json"] = """{
  "name": "__APP_NAME__",
  "private": true,
  "type": "module",
  "packageManager": "pnpm@9.12.0",
  "scripts": {
    "dev": "pnpm -r --parallel run dev",
    "build": "pnpm -r run build",
    "typecheck": "pnpm -r run typecheck",
    "lint": "eslint .",
    "test:unit": "vitest run --project unit",
    "test:integration": "vitest run --project integration",
    "e2e:smoke": "playwright test --grep-invert \\"axe:|shot |dod:|video:\\"",
    "a11y": "playwright test tests/e2e/dod.spec.ts --grep \\"dod: axe\\"",
    "screenshot": "playwright test tests/e2e/dod.spec.ts --grep \\"dod: shot\\"",
    "dod:e2e": "playwright test tests/e2e/dod.spec.ts",
    "prepare": "pnpm --filter @__APP_NAME__/db exec prisma generate",
    "db:migrate": "pnpm --filter @__APP_NAME__/db run migrate",
    "db:seed": "pnpm --filter @__APP_NAME__/db run seed",
    "db:local": "node packages/db/scripts/pg-local.mjs start --dir .pg/dev",
    "db:local:stop": "node packages/db/scripts/pg-local.mjs stop --dir .pg/dev",
    "tokens": "pnpm --filter @__APP_NAME__/ui run tokens"
  },
  "devDependencies": {
    "@axe-core/playwright": "^4.10.1",
    "@eslint/js": "^9.17.0",
    "@playwright/test": "^1.50.0",
    "@__APP_NAME__/db": "workspace:^",
    "@types/node": "^22.10.0",
    "@types/pg": "^8.11.0",
    "embedded-postgres": "17.10.0-beta.17",
    "pg": "^8.13.0",
    "eslint": "^9.17.0",
    "prettier": "^3.4.2",
    "typescript": "^5.7.2",
    "typescript-eslint": "^8.19.0",
    "vitest": "^3.0.0"
  }
}
"""

TEMPLATES["packages/db/scripts/pg-local.mjs"] = '// Local Postgres without Docker (ADR 0007-A).\n// Usage: node packages/db/scripts/pg-local.mjs start|stop|status [--port 54329] [--dir .pg/dev] [--db name] [--detach]\n// Windows note: initdb.exe fails (exit 0xC0000006) when run from the long pnpm path containing \'@\' and \'+\',\n// so the native bin/lib/share tree is copied once to a short cache dir (FOUNDRY_PG_HOME, default C:\\pg17 or ~/.foundry-pg/pg17).\nimport { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";\nimport { spawnSync } from "node:child_process";\nimport pg from "pg";\nimport { createRequire } from "node:module";\nimport { homedir } from "node:os";\nimport { join, resolve } from "node:path";\n\nconst require = createRequire(import.meta.url);\nconst args = process.argv.slice(2);\nconst cmd = args[0] ?? "status";\nconst opt = (name, dflt) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : dflt; };\nlet port = Number(opt("--port", 54329));\nconst dir = resolve(process.cwd(), opt("--dir", ".pg/dev"));\nconst db = opt("--db", "__APP_NAME__");\nconst win = process.platform === "win32";\nconst exe = (n) => (win ? `${n}.exe` : n);\n\nfunction nativeDir() {\n  const pkg = `@embedded-postgres/${process.platform === "win32" ? "windows" : process.platform}-${process.arch}`;\n  // embedded-postgres has an exports map, so resolve its entry point and walk up to the package root.\n  const epEntry = require.resolve("embedded-postgres");\n  const epRoot = epEntry.slice(0, epEntry.lastIndexOf("embedded-postgres") + "embedded-postgres".length);\n  const epRequire = createRequire(join(epRoot, "package.json"));\n  const platEntry = epRequire.resolve(pkg);\n  return join(platEntry.slice(0, platEntry.lastIndexOf("@embedded-postgres") + "@embedded-postgres".length), pkg.split("/")[1], "native");\n}\nfunction pgHome() {\n  const home = process.env.FOUNDRY_PG_HOME ?? (win ? String.raw`C:\\pg17` : join(homedir(), ".foundry-pg", "pg17"));\n  if (!existsSync(join(home, "bin", exe("initdb")))) {\n    mkdirSync(home, { recursive: true });\n    for (const d of ["bin", "lib", "share"]) cpSync(join(nativeDir(), d), join(home, d), { recursive: true });\n  }\n  return home;\n}\nfunction run(bin, argv, opts = {}) {\n  const r = spawnSync(join(pgHome(), "bin", exe(bin)), argv, { encoding: "utf8", ...opts });\n  if (r.status !== 0) throw new Error(`${bin} failed (${r.status}): ${r.stderr || r.stdout}`);\n  return r.stdout;\n}\nconst url = `postgresql://postgres:postgres@127.0.0.1:${port}/${db}`;\n\nif (cmd === "start") {\n  if (!existsSync(join(dir, "PG_VERSION"))) {\n    mkdirSync(dir, { recursive: true });\n    run("initdb", ["-D", dir, "-U", "postgres", "-A", "trust", "-E", "UTF8", "--no-locale"]);\n  }\n  const log = join(dir, "server.log");\n  if (!existsSync(join(dir, "postmaster.pid"))) {\n    // stdio must be detached or spawnSync waits on the daemon\'s inherited handles (Windows).\n    // Windows reserves TCP ranges dynamically (netsh int ipv4 show excludedportrange); when the wanted port cannot bind,\n    // walk up to 30 ports and use the first that starts (the printed DATABASE_URL carries the real port).\n    let started = false, lastErr = null;\n    for (let p = port; p < port + 30 && !started; p++) {\n      try {\n        run("pg_ctl", ["-D", dir, "-o", `-p ${p} -c listen_addresses=127.0.0.1`, "-l", log, "-w", "start"], { stdio: "ignore" });\n        if (p !== port) console.error(`pg-local: port ${port} unavailable, using ${p}`);\n        port = p; started = true;\n      } catch (e) { lastErr = e; }\n    }\n    if (!started) throw lastErr;\n  } else {\n    const pid = readFileSync(join(dir, "postmaster.pid"), "utf8").split(/\\r?\\n/);\n    if (pid[3] && Number(pid[3])) port = Number(pid[3]);  // a running cluster keeps the port it started on\n  }\n  const admin = new pg.Client({ host: "127.0.0.1", port, user: "postgres", database: "postgres" });\n  await admin.connect();\n  const exists = await admin.query("select 1 from pg_database where datname = $1", [db]);\n  if (exists.rowCount === 0) await admin.query(`create database "${db}"`);\n  await admin.end();\n  writeFileSync(join(dir, "DATABASE_URL"), url);\n  console.log(`DATABASE_URL=${url}`);\n} else if (cmd === "stop") {\n  try { run("pg_ctl", ["-D", dir, "-m", "fast", "stop"]); console.log("stopped"); } catch (e) { console.error(String(e.message)); }\n} else {\n  const up = existsSync(join(dir, "postmaster.pid"));\n  console.log(`dir ${dir} port ${port} initialised=${existsSync(join(dir, "PG_VERSION"))} running=${up}`);\n}\n'
TEMPLATES["tests/integration/global-setup.ts"] = '/**\n * Integration global setup: a real Postgres for the integration project.\n * Uses DATABASE_URL when set (CI: docker service). Otherwise starts embedded Postgres (no Docker) through\n * packages/db/scripts/pg-local.mjs, recreates the database, applies migrations, optional packages/db/sql/*.sql\n * and the seed, then exports DATABASE_URL to the workers.\n */\nimport { execSync } from "node:child_process";\nimport { existsSync, readFileSync } from "node:fs";\nimport { resolve } from "node:path";\n\nlet stop: (() => Promise<void>) | undefined;\n\nexport async function setup() {\n  const root = process.cwd();\n  const pgPort = Number(process.env.FOUNDRY_PG_PORT ?? 54330) - 1;  // the dev server keeps FOUNDRY_PG_PORT; integration uses the port below it\n  if (!process.env.DATABASE_URL) {\n    const out = execSync(`node packages/db/scripts/pg-local.mjs start --dir .pg/int --port ${pgPort} --db __APP_NAME___int`, { cwd: root, encoding: "utf8" });\n    const m = /DATABASE_URL=(\\S+)/.exec(out);\n    if (!m) throw new Error(`pg-local start did not print DATABASE_URL: ${out}`);\n    process.env.DATABASE_URL = m[1];\n    stop = async () => { execSync(`node packages/db/scripts/pg-local.mjs stop --dir .pg/int --port ${pgPort}`, { cwd: root, stdio: "ignore" }); };\n  }\n  if (!process.env.CI && !process.env.KEEP_INT_DB) {\n    const { Client: Admin } = await import("pg");\n    const target = new URL(process.env.DATABASE_URL!);\n    const dbName = target.pathname.slice(1);\n    const admin = new Admin({ connectionString: new URL("/postgres", target).toString() });\n    await admin.connect();\n    await admin.query(`DROP DATABASE IF EXISTS "${dbName}" WITH (FORCE)`);\n    await admin.query(`CREATE DATABASE "${dbName}"`);\n    await admin.end();\n  }\n  const env = { ...process.env, DATABASE_URL: process.env.DATABASE_URL };\n  execSync("pnpm --filter @__APP_NAME__/db exec prisma migrate deploy", { cwd: root, env, stdio: "inherit" });\n  const { Client } = await import("pg");\n  const c = new Client({ connectionString: process.env.DATABASE_URL });\n  await c.connect();\n  for (const f of ["rls.sql", "grants.sql"]) {\n    const p = resolve(root, "packages/db/sql", f);\n    if (existsSync(p)) await c.query(readFileSync(p, "utf8"));\n  }\n  await c.end();\n  try {\n    const seed = await import("@__APP_NAME__/db/seed");\n    if (typeof seed.runSeed === "function") await seed.runSeed(process.env.DATABASE_URL!);\n  } catch { /* no seed export yet: T-003 adds it */ }\n  return async () => {\n    if (stop) await stop();\n  };\n}\n'

TEMPLATES["pnpm-workspace.yaml"] = "packages:\n  - apps/*\n  - packages/*\n"
TEMPLATES[".npmrc"] = "auto-install-peers=true\nstrict-peer-dependencies=false\n"
TEMPLATES[".gitignore"] = "node_modules/\n.next/\ndist/\ncoverage/\n.env\n.env.*\n!.env.example\ntest-results/\nplaywright-report/\n*.tsbuildinfo\n.foundry/screenshots/\n"
TEMPLATES[".env.example"] = """# Copy to .env and fill. Never commit .env.
# `pnpm db:local` starts an embedded Postgres on 54330 without Docker (packages/db/scripts/pg-local.mjs); docker-compose.yml offers 5432.
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54330/__APP_NAME__
API_PORT=3001
WEB_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:3001
LOG_LEVEL=info
PAYMENTS_LIVE=false
PRINT_BRIDGE_TOKEN=change-me
"""
TEMPLATES["docker-compose.yml"] = """services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: __APP_NAME__
    ports:
      - "5432:5432"
    volumes:
      - dbdata:/var/lib/postgresql/data
volumes:
  dbdata: {}
"""
TEMPLATES["tsconfig.base.json"] = """{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve"
  }
}
"""
TEMPLATES["tsconfig.json"] = """{
  "extends": "./tsconfig.base.json",
  "compilerOptions": { "types": ["node"] },
  "include": ["tests/**/*.ts", "playwright.config.ts", "vitest.config.ts"]
}
"""
TEMPLATES[".prettierrc"] = "{ \"semi\": true, \"singleQuote\": false, \"printWidth\": 110 }\n"
TEMPLATES["eslint.config.js"] = """import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["**/node_modules/**", "**/.next/**", "**/dist/**", "**/sw.js", "**/next-env.d.ts", "**/generated/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { files: ["**/*.mjs", "**/*.cjs"], languageOptions: { globals: { console: "readonly", process: "readonly", URL: "readonly", Buffer: "readonly", fetch: "readonly" } } },
  {
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_", destructuredArrayIgnorePattern: "^_" }],
      "no-console": ["warn", { allow: ["warn", "error"] }],
    },
  },
);
"""
TEMPLATES["vitest.config.ts"] = """import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    projects: [
      { test: { name: "unit", include: ["apps/**/src/**/*.test.ts", "packages/**/src/**/*.test.ts"], exclude: ["**/*.int.test.ts", "**/node_modules/**"] } },
      // Integration files share one real Postgres (tests/integration/global-setup.ts: DATABASE_URL when set, else embedded
      // Postgres via packages/db/scripts/pg-local.mjs, no Docker needed) and run one file at a time.
      { test: { name: "integration", include: ["apps/**/src/**/*.int.test.ts"], exclude: ["**/node_modules/**"], globalSetup: ["tests/integration/global-setup.ts"], testTimeout: 60_000, hookTimeout: 240_000, fileParallelism: false } },
    ],
  },
});
"""
TEMPLATES["playwright.config.ts"] = """import { defineConfig, devices } from "@playwright/test";

const webPort = Number(process.env.WEB_PORT ?? 3000);
const apiPort = Number(process.env.API_PORT ?? 3001);

export default defineConfig({
  testDir: "tests/e2e",
  timeout: 60_000,
  fullyParallel: false,
  workers: process.env.CI ? 1 : 2,
  retries: 0,
  reporter: [["list"]],
  use: { baseURL: `http://localhost:${webPort}`, trace: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    // Local DoD runs reuse running dev servers (FOUNDRY_DOD); CI always starts fresh ones.
    { command: "pnpm --filter @__APP_NAME__/api run dev", env: { ...process.env, DEVICE_ENROL_CODE: process.env.DEVICE_ENROL_CODE ?? "e2e-enrol-code" }, url: `http://localhost:${apiPort}/health`, reuseExistingServer: !process.env.CI, timeout: 120_000 },
    { command: "pnpm --filter @__APP_NAME__/web run dev", env: { ...process.env, PORT: String(webPort) }, url: `http://localhost:${webPort}/`, reuseExistingServer: !process.env.CI, timeout: 180_000 },
  ],
});
"""
TEMPLATES["tests/e2e/smoke.spec.ts"] = """import { test, expect } from "@playwright/test";

const apiUrl = `http://localhost:${process.env.API_PORT ?? 3001}`;

test("home renders the app shell", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

test("api health is ok", async ({ request }) => {
  const res = await request.get(`${apiUrl}/health`);
  expect(res.ok()).toBeTruthy();
  expect(await res.json()).toEqual({ ok: true });
});
"""
TEMPLATES["tests/e2e/dod.spec.ts"] = """import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { mkdirSync } from "node:fs";

/**
 * DoD screen pass: ONE Playwright run serves axe + screenshots for the routes the ticket declares (FOUNDRY_ROUTES).
 * Per route: light/ltr context runs axe and a screenshot; dark/ltr, light/rtl, dark/rtl take screenshots only.
 * fullPage is off for list-like routes (work queues, reports, lists) to keep the shots and the run short.
 */
const routes = (process.env.FOUNDRY_ROUTES ?? "/").split(",").map((r) => r.trim()).filter(Boolean);
const ticket = process.env.FOUNDRY_TICKET ?? "adhoc";
const dir = `.foundry/screenshots/${ticket}`;
const webPort = process.env.WEB_PORT ?? 3000;
mkdirSync(dir, { recursive: true });
const settle = async (page: import("@playwright/test").Page) => {
  await page.waitForLoadState("networkidle");
  await page.locator('[aria-busy="true"]').first().waitFor({ state: "detached", timeout: 15_000 }).catch(() => undefined);
};
const name = (route: string, theme: string, lang: string) => (route === "/" ? "home" : route.replace(/^\\//, "").replace(/[/?=&]/g, "-")) + `-${theme}-${lang === "ar" ? "rtl" : "ltr"}.png`;
const fullPage = (route: string) => !/__LIST_ROUTES__/.test(route);

for (const route of routes) {
  test(`dod: axe ${route}`, async ({ browser }) => {
    const context = await browser.newContext({ colorScheme: "light", viewport: { width: 1280, height: 800 } });
    const page = await context.newPage();
    await page.goto(route);
    await settle(page);
    const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag22aa"]).analyze();
    const serious = results.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
    expect(serious, JSON.stringify(serious.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.map((n) => n.html.slice(0, 120)) })), null, 2)).toEqual([]);
    await page.screenshot({ path: `${dir}/${name(route, "light", "en")}`, fullPage: fullPage(route) });
    await context.close();
  });
  for (const [theme, lang] of [["dark", "en"], ["light", "ar"], ["dark", "ar"]] as const) {
    test(`dod: shot ${route} ${theme} ${lang}`, async ({ browser }) => {
      const context = await browser.newContext({ colorScheme: theme, viewport: { width: 1280, height: 800 } });
      await context.addCookies([{ name: "NEXT_LOCALE", value: lang, url: `http://localhost:${webPort}` }]);
      const page = await context.newPage();
      await page.goto(route);
      await settle(page);
      await page.screenshot({ path: `${dir}/${name(route, theme, lang)}`, fullPage: fullPage(route) });
      await context.close();
    });
  }
}
"""
TEMPLATES[".github/workflows/ci.yml"] = """name: ci
on: [push, pull_request]
jobs:
  dod:
    runs-on: ubuntu-latest
    services:
      db:
        image: postgres:16-alpine
        env: { POSTGRES_USER: postgres, POSTGRES_PASSWORD: postgres, POSTGRES_DB: __APP_NAME__ }
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm run typecheck
      - run: pnpm run lint
      - run: pnpm run test:unit
      - run: pnpm exec playwright install --with-deps chromium
      - run: pnpm run e2e:smoke
        env: { CI: "1" }
      - run: pnpm run a11y
        env: { CI: "1", FOUNDRY_ROUTES: "/" }
"""
TEMPLATES["README.md"] = """# __APP_NAME__

Generated by Foundry (pack `__PACK__`). Specs live under `.foundry/`; the design system under `design-system/`.

## Run

```
cp .env.example .env
docker compose up -d db
pnpm install
pnpm run db:migrate
pnpm run dev            # web :3000, api :3001
```

## Definition of done (per ticket)

```
python <foundry>/scripts/foundry.py dod --ticket T-xxx
```

Steps: typecheck, lint, unit, integration, e2e-smoke, a11y-axe, screenshot, semgrep, detect_changes_risk, spec-review.
"""

# ---- apps/web
TEMPLATES["apps/web/package.json"] = """{
  "name": "@__APP_NAME__/web",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@__APP_NAME__/ui": "workspace:*",
    "lucide-react": "^0.469.0",
    "next": "^15.1.3",
    "next-intl": "^4.0.2",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.0.0",
    "@types/react": "^19.0.2",
    "@types/react-dom": "^19.0.2",
    "tailwindcss": "^4.0.0",
    "typescript": "^5.7.2"
  }
}
"""
TEMPLATES["apps/web/tsconfig.json"] = """{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] },
    "allowJs": true,
    "incremental": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""
TEMPLATES["apps/web/next-env.d.ts"] = "/// <reference types=\"next\" />\n/// <reference types=\"next/image-types/global\" />\n"
TEMPLATES["apps/web/next.config.ts"] = """import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";
import path from "node:path";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // standalone output is off: pnpm symlinks break its file copy on Windows; the image runs `next start` (see apps/web/Dockerfile).
  outputFileTracingRoot: path.join(__dirname, "../../"),
  transpilePackages: ["@__APP_NAME__/ui"],
  headers: async () => [
    {
      source: "/(.*)",
      headers: [
        { key: "X-Content-Type-Options", value: "nosniff" },
        { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        { key: "X-Frame-Options", value: "DENY" },
      ],
    },
  ],
};

export default withNextIntl(nextConfig);
"""
TEMPLATES["apps/web/postcss.config.mjs"] = "export default { plugins: { \"@tailwindcss/postcss\": {} } };\n"
TEMPLATES["apps/web/components.json"] = """{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": { "config": "", "css": "app/globals.css", "baseColor": "neutral", "cssVariables": true },
  "aliases": { "components": "@/components", "utils": "@/lib/utils", "ui": "@/components/ui" },
  "iconLibrary": "lucide"
}
"""
TEMPLATES["apps/web/app/globals.css"] = """@import "tailwindcss";
@import "../../../design-system/tailwind.tokens.css";
@source "../../../packages/ui/src";

@theme inline {
  --color-primary: var(--color-primary);
  --color-primary-fg: var(--color-primary-fg);
  --color-bg: var(--color-bg);
  --color-surface: var(--color-surface);
  --color-text: var(--color-text);
  --color-text-muted: var(--color-text-muted);
  --color-border: var(--color-border);
  --color-success: var(--color-success);
  --color-warning: var(--color-warning);
  --color-danger: var(--color-danger);
  --color-info: var(--color-info);
}

html, body { background: var(--color-bg); color: var(--color-text); font-variant-numeric: tabular-nums; }
"""
TEMPLATES["apps/web/i18n/request.ts"] = """import { getRequestConfig } from "next-intl/server";
import { cookies } from "next/headers";

export const locales = ["en", "ar"] as const;
export type Locale = (typeof locales)[number];

export default getRequestConfig(async () => {
  const store = await cookies();
  const raw = store.get("NEXT_LOCALE")?.value;
  const locale: Locale = raw === "ar" ? "ar" : "en";
  return { locale, messages: (await import(`../messages/${locale}.json`)).default };
});
"""
TEMPLATES["apps/web/messages/en.json"] = """{ "app": { "title": "__APP_NAME__", "tagline": "Ready to build. Tickets start at T-001.", "health": "API status" } }
"""
TEMPLATES["apps/web/messages/ar.json"] = """{ "app": { "title": "__APP_NAME__", "tagline": "جاهز للبناء. التذاكر تبدأ من T-001.", "health": "حالة الواجهة البرمجية" } }
"""
TEMPLATES["apps/web/app/layout.tsx"] = """import type { Metadata, Viewport } from "next";
import { NextIntlClientProvider } from "next-intl";
import { getLocale, getMessages } from "next-intl/server";
import "./globals.css";

export const metadata: Metadata = { title: "__APP_NAME__", manifest: "/manifest.webmanifest" };
export const viewport: Viewport = { themeColor: "#ffffff", width: "device-width", initialScale: 1 };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const locale = await getLocale();
  const messages = await getMessages();
  const dir = locale === "ar" ? "rtl" : "ltr";
  return (
    <html lang={locale} dir={dir}>
      <body className="min-h-screen antialiased">
        <NextIntlClientProvider messages={messages}>
          <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:m-2 focus:p-2">Skip to content</a>
          <main id="main">{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
"""
TEMPLATES["apps/web/app/page.tsx"] = """import { getTranslations } from "next-intl/server";
import { Button } from "@__APP_NAME__/ui";

export default async function Home() {
  const t = await getTranslations("app");
  return (
    <section className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold">{t("title")}</h1>
      <p className="mt-2 text-[var(--color-text-muted)]">{t("tagline")}</p>
      <div className="mt-6">
        <Button>{t("health")}</Button>
      </div>
    </section>
  );
}
"""
TEMPLATES["apps/web/app/manifest.ts"] = """import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return { name: "__APP_NAME__", short_name: "__APP_NAME__", start_url: "/", display: "standalone", background_color: "#ffffff", theme_color: "#ffffff", icons: [] };
}
"""
TEMPLATES["apps/web/public/sw.js"] = """// Service worker stub: app shell cache. Offline data lives in the pglite store (T-005).
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", () => {});
"""

# ---- apps/api
TEMPLATES["apps/api/package.json"] = """{
  "name": "@__APP_NAME__/api",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "tsx src/index.ts",
    "build": "tsc -p tsconfig.build.json",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@hono/node-server": "^1.13.7",
    "hono": "^4.6.14",
    "pino": "^9.6.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "tsx": "^4.19.2",
    "typescript": "^5.7.2",
    "vitest": "^3.0.0"
  }
}
"""
TEMPLATES["apps/api/tsconfig.json"] = """{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": { "module": "NodeNext", "moduleResolution": "NodeNext", "types": ["node"], "jsx": "react-jsx", "jsxImportSource": "hono/jsx" },
  "include": ["src/**/*.ts"]
}
"""
TEMPLATES["apps/api/tsconfig.build.json"] = """{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": false, "outDir": "dist" }, "exclude": ["src/**/*.test.ts"] }
"""
TEMPLATES["apps/api/src/app.ts"] = """import { Hono } from "hono";
import { cors } from "hono/cors";
import { readFileSync, existsSync } from "node:fs";
import { randomUUID } from "node:crypto";
import { z } from "zod";
import pino from "pino";

export const log = pino({ level: process.env.LOG_LEVEL ?? "info" });

export const ErrorSchema = z.object({ code: z.string(), message: z.string(), request_id: z.string().optional() });
export type ApiError = z.infer<typeof ErrorSchema>;

export function createApp(openapiPath = ".foundry/openapi.yaml") {
  const app = new Hono<{ Variables: { requestId: string } }>();
  app.use("*", async (c, next) => {
    const id = c.req.header("x-request-id") ?? randomUUID();
    c.set("requestId", id);
    c.header("x-request-id", id);
    const start = Date.now();
    await next();
    log.info({ requestId: id, method: c.req.method, path: c.req.path, status: c.res.status, ms: Date.now() - start });
  });
  app.use("/api/*", cors({ origin: process.env.WEB_ORIGIN ?? "http://localhost:3000" }));
  app.get("/health", (c) => c.json({ ok: true }));
  app.get("/openapi.yaml", (c) => {
    if (!existsSync(openapiPath)) return c.json({ code: "not_found", message: "openapi.yaml missing", request_id: c.get("requestId") } satisfies ApiError, 404);
    return c.text(readFileSync(openapiPath, "utf8"), 200, { "content-type": "application/yaml" });
  });
  app.notFound((c) => c.json({ code: "not_found", message: "no such route", request_id: c.get("requestId") } satisfies ApiError, 404));
  app.onError((err, c) => {
    log.error({ requestId: c.get("requestId"), err: err.message });
    return c.json({ code: "internal", message: "unexpected error", request_id: c.get("requestId") } satisfies ApiError, 500);
  });
  return app;
}
"""
TEMPLATES["apps/api/src/index.ts"] = """import { serve } from "@hono/node-server";
import { createApp, log } from "./app.js";

const port = Number(process.env.API_PORT ?? 3001);
serve({ fetch: createApp().fetch, port }, () => log.info({ port }, "api listening"));
"""
TEMPLATES["apps/api/src/app.test.ts"] = """import { describe, it, expect } from "vitest";
import { createApp } from "./app.js";

describe("api shell", () => {
  it("health returns ok with a request id", async () => {
    const app = createApp("does-not-exist.yaml");
    const res = await app.request("/health");
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true });
    expect(res.headers.get("x-request-id")).toBeTruthy();
  });

  it("unknown routes return the error schema", async () => {
    const res = await createApp("does-not-exist.yaml").request("/nope");
    expect(res.status).toBe(404);
    const body = await res.json();
    expect(body.code).toBe("not_found");
    expect(body.request_id).toBeTruthy();
  });
});
"""

# ---- packages/db
TEMPLATES["packages/db/package.json"] = """{
  "name": "@__APP_NAME__/db",
  "private": true,
  "type": "module",
  "scripts": {
    "typecheck": "tsc --noEmit",
    "validate": "prisma validate",
    "generate": "prisma generate",
    "migrate": "prisma migrate dev",
    "seed": "tsx src/seed.ts"
  },
  "dependencies": { "@prisma/client": "^6.1.0" },
  "devDependencies": { "prisma": "^6.1.0", "tsx": "^4.19.2", "typescript": "^5.7.2" }
}
"""
TEMPLATES["packages/db/tsconfig.json"] = """{ "extends": "../../tsconfig.base.json", "compilerOptions": { "module": "NodeNext", "moduleResolution": "NodeNext", "types": ["node"] }, "include": ["src/**/*.ts"] }
"""
TEMPLATES["packages/db/src/seed.ts"] = """// Seed for pack __PACK__: one branch, roles and sample data land in T-003. Idempotent by design.
const summary = { branch: 1, roles: __ROLES__, note: "__SEED_NOTE__" };
console.warn(JSON.stringify({ seed: summary }));
"""
TEMPLATES["packages/db/README.md"] = "# db\n\nPrisma schema copied from `.foundry` by the scaffold. `pnpm run validate`, `pnpm run migrate`, `pnpm run seed`.\n"

# ---- packages/ui
TEMPLATES["packages/ui/package.json"] = """{
  "name": "@__APP_NAME__/ui",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": { "typecheck": "tsc --noEmit", "tokens": "node scripts/build-tokens.mjs" },
  "dependencies": { "class-variance-authority": "^0.7.1", "clsx": "^2.1.1", "lucide-react": "^0.469.0", "react": "^19.0.0", "react-dom": "^19.0.0" },
  "devDependencies": { "@types/react": "^19.0.2", "@types/react-dom": "^19.0.2", "typescript": "^5.7.2" }
}
"""
TEMPLATES["packages/ui/tsconfig.json"] = """{ "extends": "../../tsconfig.base.json", "compilerOptions": { "jsx": "react-jsx" }, "include": ["src/**/*.ts", "src/**/*.tsx"] }
"""
TEMPLATES["packages/ui/scripts/build-tokens.mjs"] = """// tokens.json (W3C design tokens) -> design-system/tailwind.tokens.css
import { readFileSync, writeFileSync } from "node:fs";
const tokens = JSON.parse(readFileSync("design-system/tokens.json", "utf8"));
const lines = [":root {"];
for (const [k, v] of Object.entries(tokens.color.light)) lines.push(`  --color-${k.replace(/_/g, "-")}: ${v.$value};`);
for (const [k, v] of Object.entries(tokens.font.size)) lines.push(`  --text-${k}: ${v.$value};`);
for (const [k, v] of Object.entries(tokens.space)) lines.push(`  --space-${k}: ${v.$value};`);
lines.push(`  --touch-min: ${tokens.touch.min.$value};`, "}");
lines.push('@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {');
for (const [k, v] of Object.entries(tokens.color.dark)) lines.push(`  --color-${k.replace(/_/g, "-")}: ${v.$value};`);
lines.push("} }");
writeFileSync("design-system/tailwind.tokens.css", lines.join("\\n") + "\\n");
console.error("tokens written");
"""
TEMPLATES["packages/ui/src/index.ts"] = """export { Button, buttonVariants } from "./button";
export { IconButton } from "./icon-button";
export { Numpad } from "./numpad";
export { QuantityStepper } from "./quantity-stepper";
export { Dialog } from "./dialog";
export { Toast, ToastViewport, toast } from "./toast";
export { OfflineBanner } from "./offline-banner";
export { DataTable } from "./data-table";
export { cn } from "./cn";
"""
TEMPLATES["packages/ui/src/cn.ts"] = "import { clsx, type ClassValue } from \"clsx\";\nexport const cn = (...inputs: ClassValue[]) => clsx(inputs);\n"
TEMPLATES["packages/ui/src/button.tsx"] = """import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "./cn";

export const buttonVariants = cva(
  "inline-flex min-h-[var(--touch-min)] min-w-[var(--touch-min)] items-center justify-center gap-2 rounded-[var(--radius-r1,6px)] px-4 text-base font-medium transition-colors duration-[var(--duration-fast,100ms)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60",
  {
    variants: {
      variant: {
        primary: "bg-[var(--color-primary)] text-[var(--color-primary-fg)]",
        secondary: "border border-[var(--color-border)] bg-transparent text-[var(--color-text)]",
        ghost: "bg-transparent text-[var(--color-text)]",
        danger: "bg-[var(--color-danger)] text-white",
      },
    },
    defaultVariants: { variant: "primary" },
  },
);

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export function Button({ className, variant, loading, children, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant }), className)} aria-busy={loading || undefined} disabled={props.disabled || loading} {...props}>
      {children}
    </button>
  );
}
"""
TEMPLATES["packages/ui/src/icon-button.tsx"] = """import * as React from "react";
import { cn } from "./cn";

export function IconButton({ label, className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return (
    <button aria-label={label} className={cn("inline-flex min-h-[var(--touch-min)] min-w-[var(--touch-min)] items-center justify-center rounded-[var(--radius-r1,6px)] focus-visible:outline focus-visible:outline-2", className)} {...props}>
      {children}
    </button>
  );
}
"""
TEMPLATES["packages/ui/src/numpad.tsx"] = """"use client";
import * as React from "react";
import { cn } from "./cn";

const KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "00", "0", "⌫"] as const;

export function Numpad({ value, onChange, className }: { value: string; onChange: (v: string) => void; className?: string }) {
  const press = (k: string) => onChange(k === "⌫" ? value.slice(0, -1) : value + k);
  return (
    <div role="group" aria-label="Numpad" dir="ltr" className={cn("grid grid-cols-3 gap-2", className)}>
      {KEYS.map((k) => (
        <button key={k} type="button" onClick={() => press(k)} aria-label={k === "⌫" ? "Backspace" : k}
          className="h-16 min-w-16 rounded-[var(--radius-r1,6px)] border border-[var(--color-border)] text-xl font-medium tabular-nums focus-visible:outline focus-visible:outline-2">
          {k}
        </button>
      ))}
    </div>
  );
}
"""
TEMPLATES["packages/ui/src/quantity-stepper.tsx"] = """"use client";
import * as React from "react";

export function QuantityStepper({ value, min = 1, max = 999, onChange }: { value: number; min?: number; max?: number; onChange: (v: number) => void }) {
  return (
    <div role="spinbutton" aria-valuenow={value} aria-valuemin={min} aria-valuemax={max} tabIndex={0} className="inline-flex items-center gap-2"
      onKeyDown={(e) => { if (e.key === "ArrowUp") onChange(Math.min(max, value + 1)); if (e.key === "ArrowDown") onChange(Math.max(min, value - 1)); }}>
      <button type="button" aria-label="Decrease" className="h-11 w-11 rounded border border-[var(--color-border)]" onClick={() => onChange(Math.max(min, value - 1))}>−</button>
      <span className="min-w-8 text-center tabular-nums">{value}</span>
      <button type="button" aria-label="Increase" className="h-11 w-11 rounded border border-[var(--color-border)]" onClick={() => onChange(Math.min(max, value + 1))}>+</button>
    </div>
  );
}
"""
TEMPLATES["packages/ui/src/dialog.tsx"] = """"use client";
import * as React from "react";

export function Dialog({ open, title, onClose, children }: { open: boolean; title: string; onClose: () => void; children: React.ReactNode }) {
  const ref = React.useRef<HTMLDialogElement>(null);
  React.useEffect(() => { const d = ref.current; if (!d) return; if (open && !d.open) d.showModal(); if (!open && d.open) d.close(); }, [open]);
  return (
    <dialog ref={ref} aria-labelledby="dlg-title" onClose={onClose} className="max-w-[560px] rounded-[var(--radius-r2,12px)] bg-[var(--color-surface)] p-6 text-[var(--color-text)] backdrop:bg-black/40">
      <h2 id="dlg-title" className="text-lg font-semibold">{title}</h2>
      <div className="mt-4">{children}</div>
    </dialog>
  );
}
"""
TEMPLATES["packages/ui/src/toast.tsx"] = """"use client";
import * as React from "react";

/**
 * Toasts stack at the top-end corner (logical: top-right in LTR, top-left in RTL), respect the safe area, keep at most
 * three, and never overlap the action bar. Each toast auto-dismisses; the container is one polite live region.
 */
type Kind = "info" | "success" | "error";
interface Item { id: number; kind: Kind; text: React.ReactNode }
const listeners = new Set<(items: Item[]) => void>();
let items: Item[] = [];
let seq = 0;
const publish = () => listeners.forEach((l) => l([...items]));
export function toast(text: React.ReactNode, kind: Kind = "info", ms = 4000) {
  const id = ++seq;
  items = [...items, { id, kind, text }].slice(-3);
  publish();
  setTimeout(() => { items = items.filter((i) => i.id !== id); publish(); }, ms);
}

export function ToastViewport() {
  const [list, setList] = React.useState<Item[]>([]);
  React.useEffect(() => { listeners.add(setList); return () => { listeners.delete(setList); }; }, []);
  return (
    <div role="region" aria-live="polite" aria-label="Notifications" className="pointer-events-none fixed inset-inline-end-4 z-50 flex w-[min(360px,calc(100vw-2rem))] flex-col gap-2" style={{ top: "max(1rem, env(safe-area-inset-top))" }}>
      {list.map((i) => (
        <div key={i.id} role="status" className="pointer-events-auto rounded-[var(--radius-r1,6px)] px-4 py-3 text-white shadow" style={{ background: i.kind === "success" ? "var(--color-success)" : i.kind === "error" ? "var(--color-danger)" : "var(--color-info)" }}>
          {i.text}
        </div>
      ))}
    </div>
  );
}

/** Inline variant kept for tests and simple pages: renders in flow, not fixed. */
export function Toast({ kind = "info", children }: { kind?: Kind; children: React.ReactNode }) {
  const color = kind === "success" ? "var(--color-success)" : kind === "error" ? "var(--color-danger)" : "var(--color-info)";
  return (
    <div role="status" aria-live="polite" className="rounded-[var(--radius-r1,6px)] px-4 py-3 text-white" style={{ background: color }}>
      {children}
    </div>
  );
}
"""
TEMPLATES["packages/ui/src/offline-banner.tsx"] = """import * as React from "react";

export function OfflineBanner({ queued = 0, online }: { queued?: number; online: boolean }) {
  if (online && queued === 0) return null;
  return (
    <div role="status" aria-live="polite" className="w-full bg-[var(--color-warning)] px-4 py-2 text-sm font-medium text-black">
      {online ? `Syncing ${queued}` : `Offline. ${queued} change${queued === 1 ? "" : "s"} saved on this device.`}
    </div>
  );
}
"""
TEMPLATES["packages/ui/src/data-table.tsx"] = """import * as React from "react";

export interface Column<T> { key: keyof T & string; header: string; align?: "start" | "end"; render?: (row: T) => React.ReactNode }

export function DataTable<T extends { id: string }>({ rows, columns, caption }: { rows: T[]; columns: Column<T>[]; caption: string }) {
  return (
    <table className="w-full border-collapse text-sm">
      <caption className="sr-only">{caption}</caption>
      <thead className="sticky top-0 bg-[var(--color-surface)]">
        <tr>{columns.map((c) => <th key={c.key} scope="col" className={`h-9 px-2 text-${c.align ?? "start"} font-medium`}>{c.header}</th>)}</tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id} className="border-b border-[var(--color-border)]">
            {columns.map((c) => <td key={c.key} className={`h-9 px-2 text-${c.align ?? "start"} tabular-nums`}>{c.render ? c.render(r) : String(r[c.key])}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
"""

# ---- packages/config
TEMPLATES["packages/config/package.json"] = """{ "name": "@__APP_NAME__/config", "private": true, "version": "0.0.0" }
"""
TEMPLATES["packages/config/README.md"] = "# config\n\nShared eslint (root eslint.config.js), tsconfig.base.json and .prettierrc live at the repo root; this package reserves the workspace slot for future shared configs.\n"
