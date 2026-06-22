import { z } from "zod";

/** A single planning step from the deep agent's todo list. */
export const Todo = z.object({
  content: z.string(),
  status: z.enum(["pending", "in_progress", "completed"]),
});

export const TestResults = z.object({
  passed: z.number(),
  failed: z.number(),
  details: z.string().optional(),
});

/** A managed sub-agent the factory created (like a Claude Code subagent). */
export const ManagedSubagent = z.object({
  name: z.string(),
  description: z.string(),
  tools: z.array(z.string()).default([]),
});

/** Shared state the CopilotKit UI subscribes to via useCoAgent. */
export const AgentState = z.object({
  todos: z.array(Todo).default([]),
  diff: z.string().nullable().default(null),
  testResults: TestResults.nullable().default(null),
  managedSubagents: z.array(ManagedSubagent).default([]),
  prUrl: z.string().url().nullable().default(null),
});

export type Todo = z.infer<typeof Todo>;
export type TestResults = z.infer<typeof TestResults>;
export type ManagedSubagent = z.infer<typeof ManagedSubagent>;
export type AgentState = z.infer<typeof AgentState>;
