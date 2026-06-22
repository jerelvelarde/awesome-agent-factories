import { describe, it, expect } from "vitest";
import { AgentState } from "../src/agent-state";

describe("AgentState schema", () => {
  it("round-trips a valid state", () => {
    const state = {
      todos: [{ content: "plan the change", status: "completed" as const }],
      diff: "--- a\n+++ b",
      testResults: { passed: 3, failed: 0 },
      managedSubagents: [
        { name: "migration_specialist", description: "Handles migrations.", tools: ["read_repo"] },
      ],
      prUrl: "https://github.com/o/r/pull/1",
    };
    expect(AgentState.parse(state)).toEqual(state);
  });

  it("rejects a malformed state", () => {
    expect(() => AgentState.parse({ todos: "nope" })).toThrow();
  });
});
