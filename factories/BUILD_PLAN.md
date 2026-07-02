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
    model        = <Claude model>,            # provider-prefixed; tier per sub-agent
    system_prompt= <factory's job + guardrails>,
    tools        = [<domain tools>],          # GitHub / CMS / CRM, etc.
    subagents    = [<one per role from the requirement doc>],
    interrupt_on = {<approval tool>: {"allowed_decisions": ["approve", "edit", "reject"]}},
    checkpointer = <checkpointer>,            # REQUIRED for HITL pause/resume
    store        = <BaseStore>,               # long-term memory + managed sub-agent specs
)
```

- **Sub-agents** map 1:1 to the requirement-doc roles (planner, reviewer,
  fact-checker, pricing-agent, …). Each is `{name, description, system_prompt,
  tools, model?}` (the key is `system_prompt`, not `prompt`; specs don't inherit
  the parent). Give each only the tools it needs; model-tier per role.
- **Dynamic sub-agent management.** Runtime delegation is *mostly built in* — the
  auto-injected `task` tool (context-isolated calls), a default `general-purpose`
  sub-agent, and `AsyncSubAgent` (+ the Agent Protocol) for independent runs. The
  additive part is authoring/persisting **new specs across runs**: the
  `SubAgentRegistry` + management tools (`create_subagent`, `list_subagents`,
  `update_subagent`, `delete_subagent`) persist specs in the LangGraph `BaseStore`
  and the supervisor is **rebuilt at process start** from them (a compiled graph's
  sub-agent set is fixed). The registry is bound per `build_agent()` for isolation.
- **Artifact** (the "thing") is written to the deep agent's filesystem (state
  `files`, backed by a `StoreBackend` so it survives runs) — a diff, a draft, a
  proposal — and surfaced in the UI.
- **Approval gates** are declarative **`interrupt_on`** tool interrupts (e.g.
  before `open_pr` / `publish` / `send_proposal`) with `allowed_decisions` and
  optional `when` predicates; a checkpointer is required and CopilotKit renders
  the approve/edit/reject step. Use `reject` (not `respond`) to deny a
  side-effecting tool.
- **Persistence & quality (production).** Swap `MemorySaver` for
  `PostgresSaver`/`AsyncPostgresSaver` + a persistent `BaseStore`. Add the quality
  layer each factory's BUILD_PLAN details: deterministic artifact validation +
  LLM-as-judge on a ~20-case golden dataset (CI gate via LangSmith/promptfoo),
  OTel/LangSmith tracing with per-role cost, hard token/iteration/wall-clock
  ceilings, and a verifier/critic before each human gate. See
  [`.chalk/improvements.md`](../.chalk/improvements.md).

## Standard project layout (applied to all three, standalone)

```
factories/<factory-name>/
  README.md
  BUILD_PLAN.md
  agent/                         # Python — the deep-agent factory
    pyproject.toml               # deepagents, langgraph, pytest, ruff
    langgraph.json               # exposes the agent to CopilotKit via AG-UI
    src/<pkg>/agent.py           # build_agent() -> create_deep_agent(...)
    src/<pkg>/subagents.py       # seed role sub-agent configs
    src/<pkg>/registry.py        # SubAgentRegistry — managed sub-agents
    src/<pkg>/management.py      # create/list/update/delete_subagent tools
    src/<pkg>/tools.py           # domain tools (stubs: NotImplementedError)
    src/<pkg>/gates.py           # HITL interrupt config for approval tools
    tests/test_agent.py          # agent wired with expected sub-agents/tools (RED)
    tests/test_tools.py          # per-tool contract (RED)
    tests/test_gates.py          # interrupts fire at the right tools (RED)
    tests/test_registry.py       # seed + create/manage sub-agents (RED)
    tests/test_management.py      # sub-agent management tools (RED)
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
- CI (lands with the implementation) matrix-runs each project's Python + TS tests.
- Model tier configurable per sub-agent (env-driven), defaulting to current
  Claude models.
