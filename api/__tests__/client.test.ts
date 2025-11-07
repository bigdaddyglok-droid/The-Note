import { afterEach, describe, expect, it, vi } from "vitest";

describe("resolveWebSocketUrl", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.resetModules();
  });

  it("translates http to ws", async () => {
    vi.stubEnv("VITE_BACKEND_URL", "http://localhost:8000");
    const { resolveWebSocketUrl } = await import("../client");
    expect(resolveWebSocketUrl("/ws/test")).toBe("ws://localhost:8000/ws/test");
  });

  it("translates https to wss", async () => {
    vi.stubEnv("VITE_BACKEND_URL", "https://api.example.com");
    const { resolveWebSocketUrl } = await import("../client");
    expect(resolveWebSocketUrl("ws/path")).toBe("wss://api.example.com/ws/path");
  });
});
