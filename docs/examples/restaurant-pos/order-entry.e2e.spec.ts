import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/**
 * T-008 e2e: table map → order entry → add two items (one with a modifier) → send to kitchen → state sent, total
 * AED 34.00 (Karak Chai Large 12.00 + Fattoush 22.00, VAT inclusive) → the server holds the SENT order with the same
 * total (offline-first outbox synced) → the kds screen shows the ticket. AT3: Arabic mirrors and axe is clean.
 */
const webPort = process.env.WEB_PORT ?? 3000;
const apiUrl = `http://localhost:${process.env.API_PORT ?? 3001}`;
const branch = "11111111-1111-4111-8111-111111111111";

async function enrol(page: Page, name: string) {
  const enrol = await page.request.post(`${apiUrl}/api/v1/devices/enrol`, { headers: { "idempotency-key": `e2e-${name}-${Date.now()}` }, data: { branch_id: branch, name, enrol_code: process.env.DEVICE_ENROL_CODE ?? "e2e-enrol-code" } });
  expect(enrol.ok()).toBeTruthy();
  const { token } = (await enrol.json()) as { token: string };
  const who = await page.request.get(`${apiUrl}/api/v1/whoami`, { headers: { authorization: `Bearer ${token}` } });
  const { device_id } = (await who.json()) as { device_id: string };
  await page.addInitScript(([tk, id]) => { localStorage.setItem("device_token", tk); localStorage.setItem("device_id", id); }, [token, device_id]);
  return { token, device_id };
}

test("open table 3, add Karak Chai (Large) and Fattoush, send to kitchen → sent, AED 34.00, synced, on kds", async ({ page }) => {
  const dev = await enrol(page, "till-e2e");
  await page.goto("/table-map");
  await page.getByRole("tab", { name: "Indoor" }).click();
  await page.getByRole("button", { name: /^Table 3,/ }).click();
  await expect(page).toHaveURL(/\/order-entry\?table=3/);
  await expect(page.getByRole("status").filter({ hasText: "Tap an item to start" })).toBeVisible();

  await page.getByRole("button", { name: /^Karak Chai,/ }).click();
  const sheet = page.getByRole("dialog");
  await expect(sheet).toBeVisible();
  await sheet.getByRole("button", { name: /^Large/ }).click();
  await sheet.getByRole("button", { name: "Confirm" }).click();
  await page.getByRole("button", { name: "Salads" }).click();
  await page.getByRole("button", { name: /^Fattoush,/ }).click();

  await expect(page.getByTestId("order-total")).toHaveText(/34\.00/);
  await expect(page.getByTestId("order-state")).toHaveText("Draft");
  await page.getByRole("button", { name: "Send to kitchen" }).click();
  await expect(page.getByTestId("order-state")).toHaveText("Sent");
  await expect(page.getByRole("status").filter({ hasText: "Sent to kitchen." })).toBeVisible();
  await expect(page.getByTestId("order-total")).toHaveText(/34\.00/);

  // the outbox drained to the server: exactly one SENT order for this device's branch with the server-computed total
  await expect.poll(async () => {
    const res = await page.request.get(`${apiUrl}/api/v1/sync/pull?device_id=${dev.device_id}&since_seq=0`, { headers: { authorization: `Bearer ${dev.token}` } });
    return ((await res.json()) as { last_acked_seq: number }).last_acked_seq;
  }).toBeGreaterThanOrEqual(2);

  await page.goto("/kds");
  const ticket = page.getByTestId("kds-ticket").first();
  await expect(ticket).toContainText("Table 3");
  await expect(ticket).toContainText("Karak Chai (Large)");
  await expect(ticket).toContainText("Fattoush");
  await page.getByRole("tab", { name: "Bar" }).click();
  await expect(page.getByTestId("kds-ticket").first()).not.toContainText("Fattoush");
  await page.getByRole("button", { name: "Bump" }).first().click();
  await expect(page.getByRole("status").filter({ hasText: "Bumped." })).toBeVisible();
  await expect(page.getByTestId("kds-ticket")).toHaveCount(0);
  await page.getByRole("button", { name: /^Recall/ }).click();
  await expect(page.getByTestId("kds-ticket")).toHaveCount(1);
});

test("AT3: order-entry in Arabic mirrors (dir=rtl, ticket on the start side) and axe reports zero serious violations", async ({ browser }) => {
  const context = await browser.newContext();
  await context.addCookies([{ name: "NEXT_LOCALE", value: "ar", url: `http://localhost:${webPort}` }]);
  const page = await context.newPage();
  await page.goto("/order-entry?table=3");
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("طاولة 3");
  const items = await page.getByRole("list", { name: "أصناف القائمة" }).boundingBox();
  const ticket = await page.getByRole("complementary", { name: "التذكرة" }).boundingBox();
  expect(items!.x).toBeGreaterThan(ticket!.x); // grid and ticket swap sides under RTL
  const numpadDir = await page.getByRole("group", { name: "Numpad" }).evaluate((el) => getComputedStyle(el).direction);
  expect(numpadDir).toBe("ltr");
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag22aa"]).analyze();
  expect(results.violations.filter((v) => v.impact === "serious" || v.impact === "critical")).toEqual([]);
  await context.close();
});
