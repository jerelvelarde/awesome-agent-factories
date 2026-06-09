# Build Plan: Three Agent Factories

Builds the three factories specified in [`requirements/`](../requirements) as
**three standalone deep-agent projects**, using **test-driven development**:
land a failing-test scaffold (red) first, then implement tools/sub-agents until
green.

- [Software Development Factory](software-development-factory/BUILD_PLAN.md)
- [Content Creation Factory](content-creation-factory/BUILD_PLAN.md)
- [Sales Proposal Factory](sales-proposal-factory/BUILD_PLAN.md)

## Stack

| Layer | Technology | Role |
| --- | --- | --- |
| Harness (model + system instructions + tools) | [`deepagents`](https://github.com/langchain-ai/deepagents) on LangGraph | `create_deep_agent(...)` — the agent harness. Not hand-built. |
| Group of agents | deepagents **sub-agents** | one per role, with context isolation |
| Factory | the deep agent + its artifact | produces one typed thing into the virtual filesystem |
| UI | [CopilotKit](https://github.com/CopilotKit/CopilotKit) (AG-UI protocol) | renders plan/todos, sub-agent activity, artifact, and approval gates |
| Language split | Python (agent) / TypeScript (UI) | |

### Why deepagents (not a custom harness, not a hand-wired StateGraph)

A *harness* is base model + system instructions + tools. `deepagents` **is**
that harness, batteries included: a single `create_deep_agent(model, tools,
system_prompt, subagents=[...])` call gives us **planning** (`write_todos`), a
**virtual filesystem** (where the artifact is built), **sub-agent spawning** for
context isolation, and **human-in-the-loop interrupts** for approval gates — all
on the durable LangGraph runtime. The requirement docs' "supervised pipeline of
role-specialized agents with approval gates" is the deep-agent pattern almost
verbatim, so we configure it rather than rebuild it.

### Why CopilotKit for the UI

CopilotKit (maker of the AG-UI protocol, with first-class LangGraph + deep
agents support) subscribes to the agent's shared state via `useCoAgent`, renders
per-step UI via `useCoAgentStateRender`, and turns our approval gates into
human-in-the-loop breakpoints the user confirms in the UI. That's exactly the
"transparency and control at the human boundary" each factory needs before it
ships software / publishes content / sends a proposal.

## How a factory is assembled (same shape for all three)

```
ORCHESTRATOR  = create_deep_agent(
    model        = <Claude model>,
    system_prompt= <factory's job + guardrails>,
    tools        = [<domain tools>],          # GitHub / CMS / CRM, etc.
    subagents    = [<one per role from the requirement doc>],
)
```

- **Sub-agents** map 1:1 to the requirement-doc roles (planner, reviewer,
  fact-checker, pricing-agent, …). Each is `{name, description, prompt, tools}`.
- **Artifact** (the "thing") is written to the deep agent's filesystem — a diff,
  a draft, a proposal — and surfaced in the UI.
- **Approval gates** are tool-level HITL interrupts (e.g. interrupt before the
  `open_pr` / `publish` / `send_proposal` tool) that CopilotKit renders.

## Standard project layout (applied to all three, standalone)

```
factories/<factory-name>/
  README.md
  BUILD_PLAN.md
  agent/                         # Python — the deep-agent factory
    pyproject.toml               # deepagents, langgraph, pytest, ruff
    langgraph.json               # exposes the agent to CopilotKit via AG-UI
    src/<pkg>/agent.py           # build_agent() -> create_deep_agent(...)
    src/<pkg>/subagents.py       # role sub-agent configs
    src/<pkg>/tools.py           # domain tools (stubs: NotImplementedError)
    src/<pkg>/gates.py           # HITL interrupt config for approval tools
    tests/test_agent.py          # agent wired with expected sub-agents/tools (RED)
    tests/test_tools.py          # per-tool contract (RED)
    tests/test_gates.py          # interrupts fire at the right tools (RED)
  ui/                            # TypeScript — the CopilotKit app
    package.json                 # @copilotkit/react-core, react-ui, runtime, next, vitest
    app/                         # Next.js app: <CopilotKit> + useCoAgent
    src/agent-state.ts           # zod schema mirroring the agent state/artifact
    test/agent-state.test.ts     # state schema round-trip (RED)
    test/hitl.test.ts            # approval-gate component renders on interrupt (RED)
```

**Red → green:** tools and sub-agent prompts ship as stubs (`NotImplementedError`
/ placeholder prompts). Tests assert the *contract* — the agent is built with the
expected sub-agents and tools, each tool's signature/behavior, that approval
tools are interrupt-gated, and that the UI state schema round-trips. Wiring tests
go green first; behavioral tool/sub-agent tests go green as each is implemented.

## Phases

1. **Scaffold (red).** All three projects: `build_agent()` with stub tools and
   sub-agent configs, the CopilotKit app shell, and the full failing test
   suites. CI runs `pytest` + `vitest` per project, reporting red.
2. **Wiring green.** Implement `build_agent()` assembly + gate config so
   structure/interrupt tests pass with stub tools.
3. **Tools & sub-agents green.** Implement domain tools and role prompts one at a
   time, each flipping its test green. Software Dev factory end-to-end first,
   then Content, then Sales.
4. **UI + integration.** Wire CopilotKit rendering to live agent state and
   connect real GitHub/CMS/CRM adapters behind tool interfaces.

## Tooling & CI

- Python: `deepagents`, `langgraph`, `langchain`, `pytest`, `ruff` (via `uv`).
- TypeScript: `@copilotkit/*`, `next`, `vitest`, `zod`.
- `.github/workflows/factories.yml` matrix runs each project's Python + TS tests.
- Model tier configurable per sub-agent (env-driven), defaulting to current
  Claude models.
