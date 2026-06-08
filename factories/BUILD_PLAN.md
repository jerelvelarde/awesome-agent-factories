# Build Plan: Three Agent Factories

This plan covers building the three factories specified in [`requirements/`](../requirements)
as **three standalone LangGraph projects**, using **test-driven development**:
we land a failing-test scaffold (red) first, then implement nodes until green.

- [Software Development Factory](software-development-factory/BUILD_PLAN.md)
- [Content Creation Factory](content-creation-factory/BUILD_PLAN.md)
- [Sales Proposal Factory](sales-proposal-factory/BUILD_PLAN.md)

## Decisions

| Decision | Choice |
| --- | --- |
| Orchestration | LangGraph (`StateGraph` per factory) |
| Structure | Three standalone projects under `factories/` — no shared package |
| Languages | Python (orchestration + agents) and TypeScript (typed contract + client/CLI) |
| First deliverable | Failing-test scaffold (red) + a build plan per factory |
| Human oversight | Explicit `interrupt` gates as required by each spec |

## Why this shape

Each requirement doc describes a **supervised pipeline of role-specialized
agents with human approval gates and review loops**. That maps directly onto a
LangGraph `StateGraph`: each agent role becomes a node, the review loops become
conditional edges, and the approval gates become `interrupt` points. TDD lets
us encode the spec (state shape, routing, guardrails) as tests *before* writing
any agent logic, so the graph's contract is pinned down and the build is just
"make red go green."

Python owns orchestration and agent logic (LangGraph's mature runtime).
TypeScript owns the typed I/O contract (zod schemas mirroring the Python state)
and a thin client/CLI — so the factories are consumable from a JS/TS stack and
the input/output shapes are validated on both sides.

## Standard project layout (applied to all three)

```
factories/<factory-name>/
  README.md
  BUILD_PLAN.md
  python/
    pyproject.toml              # pytest, ruff, langgraph, langchain-core, pydantic
    src/<pkg>/state.py          # Pydantic/TypedDict state schema
    src/<pkg>/graph.py          # build_graph() -> compiled StateGraph
    src/<pkg>/nodes/*.py        # one module per agent role (stubs: NotImplementedError)
    src/<pkg>/guardrails.py     # gate/routing predicates
    tests/test_state.py         # state schema contract
    tests/test_graph.py         # graph compiles, routing, interrupts (RED)
    tests/test_nodes.py         # per-node input/output contract (RED)
  typescript/
    package.json                # vitest, zod, tsx
    tsconfig.json
    src/schema.ts               # zod schemas mirroring state I/O
    src/client.ts               # typed client / CLI to invoke the graph
    test/schema.test.ts         # schema round-trip (RED)
    test/client.test.ts         # client/CLI contract (RED)
```

**Red → green mechanism:** nodes and the client are committed as stubs that
raise `NotImplementedError` / `throw new Error("not implemented")`. The tests
assert the real contract (state keys produced, routing taken, gates hit), so
they fail until each node is implemented. Graph-structure tests (compiles,
edges, interrupt points) can go green first; behavioral node tests go green as
agents are filled in.

## Phases

1. **Scaffold (red).** Create all three project skeletons, state schemas, graph
   wiring with stub nodes, zod schemas, and the full failing test suites. CI
   runs `pytest` + `vitest` for each project and reports red.
2. **Graph structure green.** Implement `build_graph()` wiring and routing
   predicates so structural/routing/interrupt tests pass with stub nodes.
3. **Node implementation green.** Fill agent nodes (LLM prompts + tools) one at
   a time, each flipping its node test to green. Start with the Software
   Development Factory end-to-end, then Content, then Sales.
4. **Integration.** Wire real external systems (GitHub/CRM/CMS) behind
   interfaces, with the human approval gates enforced.

## Tooling & CI

- Python: `pytest`, `ruff`, `pydantic`, `langgraph`, `langchain-core`. Managed with `uv`.
- TypeScript: `vitest`, `zod`, `tsx`, `typescript`.
- A `.github/workflows/factories.yml` matrix runs each project's Python and TS
  tests on push/PR. (Also a good home for `awesome-lint` on the README.)
- Model tier is configurable per node (env-driven), defaulting to current Claude
  models for agent roles.

## What lands in the next push

The three per-factory `BUILD_PLAN.md` docs (this PR), then — on approval — the
red scaffold from Phase 1 across all three projects.
