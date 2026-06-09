# Build Plan: Software Development Factory

Implements [`requirements/software-development-factory.md`](../../requirements/software-development-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green.

**Produces:** new software — a reviewed, tested draft pull request.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the code workspace (virtual filesystem), and approval
gates (HITL interrupts) come from `deepagents`.

```
build_agent() -> create_deep_agent(
    model        = <Claude model>,
    system_prompt= "Ship a reviewed, tested change for the given task. Plan
                    first; never open a PR without passing tests and human
                    approval of the plan.",
    tools        = [read_repo, write_file, run_tests, run_lint, open_pr],
    subagents    = [planner, implementer, test_engineer, reviewer,
                    verifier, integrator],
)
```

### Sub-agents (`subagents.py`)

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `planner` | Decompose task into a plan + files to touch | filesystem |
| `implementer` | Write code matching conventions | `read_repo`, `write_file` |
| `test_engineer` | Add/update tests (fail-before, pass-after) | `write_file`, `run_tests` |
| `reviewer` | Correctness/quality pass on the diff | filesystem |
| `verifier` | Run build/lint/tests; run app where feasible | `run_tests`, `run_lint` |
| `integrator` | Open the draft PR with summary + plan + evidence | `open_pr` |

### Dynamic sub-agent management

Beyond the seed roles above, the factory can **create and manage its own
sub-agents at runtime** (like Claude Code subagents). A `SubAgentRegistry`
(`registry.py`) holds managed harness specs, and management tools
(`management.py`: `create_subagent`, `list_subagents`, `update_subagent`,
`delete_subagent`) are given to the orchestrator so it can author a new
specialized sub-agent — e.g. a `migration_specialist` — when a task needs a role
it does not yet have. Specs persist via a backend across runs.

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`).
- The change (diff, new files, tests) lives in the **virtual filesystem**.
- The deliverable is a **draft PR** opened by `open_pr`.

### Approval gates (`gates.py`)

- HITL interrupt **before `open_pr`** — human owns the merge boundary (FR3, FR7).
- Optional interrupt before large refactors (security review detour for
  auth/crypto/data changes).

## UI (CopilotKit)

- `useCoAgent` streams the todo list and current sub-agent so the user watches
  plan → implement → review → verify live.
- `useCoAgentStateRender` renders the diff and test results as they land.
- The `open_pr` interrupt renders an **approve/deny** card before the PR opens.

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

1. Assemble `build_agent()` + gate config → agent/gate tests pass with stubs.
2. Implement tools, then role prompts (`planner` → `implementer`/`test_engineer`
   → `reviewer`/`verifier` → `integrator`) → tool/behavior tests pass.
3. Wire CopilotKit to live state; connect real GitHub/CI adapters behind the
   tool interfaces; keep the PR/merge gate human-owned.

## Integrations

GitHub (draft PRs, comments), CI provider, issue tracker, isolated build/test
sandbox — all behind tool interfaces so tests use fakes.
