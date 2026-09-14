import { describe, it, expect, vi, afterEach } from "vitest";
import { createSession, getSession } from "./client";

describe("api client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("createSession posts to /sessions and returns parsed json", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ session_id: 1, status: "running" }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await createSession("https://example.com/repo.git", "fix bug");

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/sessions"),
      expect.objectContaining({ method: "POST" })
    );
    expect(result).toEqual({ session_id: 1, status: "running" });
  });

  it("getSession fetches session detail by id", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ session_id: 1, status: "running", messages: [] }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await getSession(1);

    expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining("/sessions/1"));
    expect(result.status).toBe("running");
  });
});
