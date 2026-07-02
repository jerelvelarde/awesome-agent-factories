# Build Plan: Software Development Factory

Implements [`requirements/software-development-factory.md`](../../requirements/software-development-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green. Design reflects the researched best practices in
[`.chalk/improvements.md`](../../.chalk/improvements.md) (pin an exact
`deepagents` version — the API tracks the current 0.5 middleware model).

**Produces:** new software — a reviewed, tested draft pull request.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the code workspace (virtual filesystem), and approval
gates (HITL interrupts) come from `deepagents`. `create_deep_agent(...)` returns
a standard compiled LangGraph graph, so checkpointers, stores, streaming, and
tracing all apply directly.

```
build_agent(checkpointer, store) -> create_deep_agent(
    model         = "anthropic:claude-sonnet-4-6",  # provider-prefixed; tier per sub-agent
    system_prompt = "Ship a reviewed, tested change for the given task. Plan
                     first; never open a PR without passing tests and human
                     approval of the plan.",
    tools         = [read_repo, write_file, run_tests, run_lint, open_pr],
    subagents     = [planner, implementer, test_engineer, reviewer,
                     verifier, integrator],
    interrupt_on  = {"open_pr": {"allowed_decisions": ["approve", "edit", "reject"]}},
    checkpointer  = checkpointer,   # REQUIRED for HITL pause/resume
    store         = store,          # long-term memory + managed sub-agent specs
)
```

### Sub-agents (`subagents.py`)

Each sub-agent is a spec `{name, description, system_prompt, tools, model?}`
(note the key is **`system_prompt`**, not `prompt`; specs do not inherit the
parent's prompt/tools, so each is explicit and includes an output-format limit
so summaries stay small).

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `planner` | Decompose task into a plan + files to touch | filesystem |
| `implementer` | Write code matching conventions | `read_repo`, `write_file` |
| `test_engineer` | Add/update tests (fail-before, pass-after) | `write_file`, `run_tests` |
| `reviewer` | Correctness/quality pass on the diff | filesystem |
| `verifier` | Run build/lint/tests; run app where feasible | `run_tests`, `run_lint` |
| `integrator` | Open the draft PR with summary + plan + evidence | `open_pr` |

Give each sub-agent only the tools it needs (over-provisioning worsens routing),
and write action-oriented `description`s — the orchestrator routes on them.
Model-tier per role: a cheap/fast model for `planner`/routing, a frontier model
for `implementer`/`reviewer`.

### Dynamic sub-agent management

Runtime delegation is **mostly built in**: deepagents auto-injects a `task` tool
(context-isolated sub-agent calls) and a default `general-purpose` sub-agent, and
`AsyncSubAgent` (+ the Agent Protocol) covers independent/parallel runs. The
genuinely additive part is **authoring and persisting new specs across runs** —
deepagents has no spec store. So the `SubAgentRegistry` (`registry.py`) +
management tools (`management.py`: `create_subagent`, `list_subagents`,
`update_subagent`, `delete_subagent`) persist specs in the LangGraph **`BaseStore`**
and the supervisor is **rebuilt at process start** from stored specs (a compiled
graph's sub-agent set is fixed — "runtime creation" = persist now, rebind on next
construction). The registry is bound per `build_agent()` call for run isolation.

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`, exposed as state
  `todos`).
- The change (diff, new files, tests) lives in the **virtual filesystem** (state
  `files`), backed by a `StoreBackend` so it survives across runs.
- The deliverable is a **draft PR** opened by `open_pr`.

### Persistence & durability

`MemorySaver` is dev-only. In production use **`PostgresSaver`/`AsyncPostgresSaver`**
(connection pool, `.setup()` once) for crash recovery + horizontal scaling, and a
persistent **`BaseStore`** for long-term memory, the `StoreBackend` artifact, and
managed sub-agent specs. Anthropic/Bedrock prompt caching is automatic on stable
system prompts.

### Approval gates (`gates.py`)

- HITL via the declarative **`interrupt_on`** map (not a hand-rolled node):
  `open_pr` pauses for human approval — the merge boundary (FR3, FR7). A
  checkpointer is required; resume with `Command(resume={"decisions": [...]})` on
  the same `thread_id`. Use **`reject`** (not `respond`) to deny a side-effecting
  tool.
- Optional conditional interrupt via a `when` predicate on the `ToolCallRequest`
  — e.g. a security-review detour when the diff touches auth/crypto/data.

## Quality & hardening

The scaffold pins structure; these make it trustworthy (add once wiring is green):

- **Eval:** deterministic checks on the typed artifact first (diff applies, tests
  actually ran, no false greens), then LLM-as-judge (single rubric call) for
  subjective quality. Build a ~20-case golden dataset and eval the **trajectory**
  (tool choice/order), gating in CI via LangSmith or promptfoo.
- **Observability:** OTel GenAI conventions (spans `invoke_agent`/`chat`/
  `execute_tool`, per-role token/cost) via LangSmith or Langfuse.
- **Reliability:** the `reviewer`/`verifier` act as a **critic before the human
  gate** (ideally a different model so failures don't correlate); hard per-run
  token/iteration/wall-clock ceilings (LangGraph recursion limit).
- **Domain hardening — false-green tests / reward hacking** (the dominant 2026
  risk for a TDD factory): run and verify tests in an **isolated, network-
  restricted sandbox**; keep canonical test files **protected so the code-writing
  agent can't mutate them**; the `verifier` owns grading independently and treats
  "tests pass" as necessary-not-sufficient (run the app where feasible). Never let
  the agent that writes code own the grading harness.

## UI (CopilotKit)

- Render the plan/diff off deepagents state — `state.todos` (plan) and
  `state.files` (diff, test output) — via `useCoAgent` (v1) / `useAgent` (v2).
  Keep the shared state schema as **one Zod schema** and `.parse` inbound state so
  TS↔Python drift fails loudly; subclass `CopilotKitState` on the Python side.
- The `open_pr` approval gate renders an approve/edit/deny card via
  **`useHumanInTheLoop`** (v2) or `useInterrupt` when the graph interrupts. Both
  need a checkpointer + stable `threadId`.
- Wiring: Next.js `/api/copilotkit` → `CopilotRuntime` with `LangGraphHttpAgent`;
  Python builds the graph with `CopilotKitMiddleware` and exposes it via
  `add_langgraph_fastapi_endpoint` (`ag-ui-langgraph`); `langgraph.json` gains an
  `"http"` app entry. `/api/copilotkit` is the auth boundary. Note the CopilotKit
  **v2** API (Dec 2025) is the forward path; v1 hooks still work.

## Failing tests (red)

`agent/tests/`
- `test_agent.py` (RED until wired): `build_agent()` returns a deep agent
  configured with the six named sub-agents and the expected tools.
- `test_tools.py` (RED): each tool (`run_tests`, `open_pr`, …) honors its
  signature; stubs raise `NotImplementedError`.
- `test_gates.py` (RED): invoking the agent interrupts **before** `open_pr` and
  does not open a PR without approval.
- `test_registry.py`: seeding + read access pass; `create`/`delete` of a managed
  sub-agent are RED until implemented.
- `test_management.py` (RED): `create_subagent`/`list_subagents`/… return/manage
  specs.

`ui/test/`
- `agent-state.test.ts` — zod schema for `{todos, diff, testResults, prUrl}`
  round-trips the Python state; rejects malformed payloads.
- `hitl.test.ts` — the approval card renders when the agent emits the `open_pr`
  interrupt (stub UI → RED).

## Green milestones

1. Assemble `build_agent()` + `interrupt_on`/checkpointer config → agent/gate
   tests pass with stubs.
2. Implement tools, then role prompts (`planner` → `implementer`/`test_engineer`
   → `reviewer`/`verifier` → `integrator`) → tool/behavior tests pass.
3. Add the quality layer (eval dataset + CI gate, tracing, run ceilings, sandboxed
   test verification).
4. Wire CopilotKit to live state; connect real GitHub/CI adapters behind the
   tool interfaces; keep the PR/merge gate human-owned.

## Integrations

GitHub (draft PRs, comments), CI provider, issue tracker, isolated build/test
sandbox — all behind tool interfaces so tests use fakes.
