import { test, expect } from "@playwright/test";

const selectAll = process.platform === "darwin" ? "Meta+a" : "Control+a";

test.describe("SQL Healthcare Practice smoke", () => {
  test("lesson 1 happy path", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "SQL Healthcare Practice" })).toBeVisible();
    await page.getByTestId("run-button").click();
    await expect(page.getByTestId("results-table")).toBeVisible({ timeout: 15000 });
  });

  test("typo shows error feedback with line", async ({ page }) => {
    await page.goto("/");
    await page.locator(".cm-content").click();
    await page.keyboard.press(selectAll);
    await page.keyboard.type("SELECT name\nFRMO hospitals");
    await page.getByTestId("run-button").click();
    await expect(page.getByTestId("feedback-error")).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(/Line 2/)).toBeVisible();
    await expect(page.getByText(/FROM/)).toBeVisible();
  });

  test("dialect toggle works", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("dialect-select").selectOption("mysql");
    await page.getByTestId("run-button").click();
    await expect(page.getByTestId("results-table")).toBeVisible({ timeout: 15000 });
  });
});
