# Build Plan: Software Development Factory

Implements [`requirements/software-development-factory.md`](../../requirements/software-development-factory.md)
as a standalone LangGraph project. TDD: red scaffold first, then green.

## Graph design

State graph modeling the plan → implement → review → verify loop.

### State (`state.py`)

```
task: str                       # the brief / ticket / bug
repo_context: dict              # language, conventions, paths
plan: Plan | None               # steps + files to touch
approvals: dict[str, bool]      # {"plan": bool}
diff: str | None                # proposed changes
tests: list[str]                # added/updated test files
test_results: TestRun | None    # build/lint/test outcome
review: Review | None           # {status: approved|changes, comments}
pr_url: str | None
iteration: int                  # review-loop counter (bounds retries)
```

### Nodes (one agent role each, `nodes/`)

| Node | Role | Output keys |
| --- | --- | --- |
| `planner` | Decompose task into a plan + files | `plan` |
| `plan_gate` | `interrupt` for human approval on large changes | `approvals["plan"]` |
| `implementer` | Write code matching conventions | `diff` |
| `test_engineer` | Add/update tests (fail-before, pass-after) | `tests` |
| `reviewer` | Correctness/quality pass on the diff | `review` |
| `verifier` | Run build/lint/tests; run app where feasible | `test_results` |
| `integrator` | Open draft PR with summary, plan, evidence | `pr_url` |

### Edges / routing (`graph.py`, `guardrails.py`)

```
START → planner → plan_gate → implementer → test_engineer → reviewer
reviewer  --changes_requested--> implementer        (loop, bounded by iteration)
reviewer  --approved-----------> verifier
verifier  --failed-------------> implementer         (loop)
verifier  --passed-------------> integrator → END
```

- `plan_gate` is a hard interrupt; `integrator` is unreachable until
  `approvals["plan"]` is true (FR3, guardrail).
- `requires_human_review(state)` forces a security-review detour for
  auth/crypto/data changes.

## Failing tests (red)

`python/tests/`
- `test_state.py` — state schema accepts a valid task; rejects missing `task`.
- `test_graph.py` (RED until graph wired):
  - graph compiles and exposes the 7 nodes;
  - `reviewer` with `changes` routes back to `implementer`;
  - `verifier` failure routes back to `implementer`;
  - `integrator` is not reached when `approvals["plan"]` is false (interrupt);
  - `iteration` bound stops infinite review loops.
- `test_nodes.py` (RED until nodes implemented): each node, given minimal input
  state, returns its declared output key(s). Stubs raise `NotImplementedError`.

`typescript/test/`
- `schema.test.ts` — `Plan`/`Review`/`TestRun` zod schemas round-trip the Python
  JSON contract; reject malformed payloads.
- `client.test.ts` — CLI parses a task arg and calls the graph endpoint with the
  right shape (stub client throws → RED).

## Green milestones

1. Wire `build_graph()` + routing → structure/routing/interrupt tests pass.
2. Implement `planner`, then `implementer`/`test_engineer`, then `reviewer`,
   `verifier`, `integrator` → node tests pass one by one.
3. Replace stub repo/CI/GitHub calls with real adapters behind interfaces;
   keep the merge gate human-owned (FR7).

## Integrations

GitHub (draft PRs, comments), CI provider, issue tracker, isolated build/test
sandbox. All behind interfaces so tests use fakes.
