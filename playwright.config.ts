import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 45000,
  use: {
    baseURL: "http://localhost:5173",
  },
  webServer: [
    {
      command: "cd backend && python3 -m uvicorn main:app --port 8000",
      url: "http://localhost:8000/api/health",
      reuseExistingServer: true,
      timeout: 60000,
    },
    {
      command: "cd frontend && npm run dev",
      url: "http://localhost:5173",
      reuseExistingServer: true,
      timeout: 60000,
    },
  ],
});
