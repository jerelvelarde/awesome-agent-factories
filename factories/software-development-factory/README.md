# Software Development Factory

A deepagents-based agent factory that produces **new software** — a reviewed,
tested draft pull request. See [`BUILD_PLAN.md`](BUILD_PLAN.md) for the design
and [`../../requirements/software-development-factory.md`](../../requirements/software-development-factory.md)
for the requirements.

## Layout

```
agent/   Python — the deepagents deep agent (harness + orchestration)
ui/      TypeScript — the CopilotKit UI (AG-UI)
```

## Status: red scaffold (TDD)

Tools, sub-agent prompts, gates, and the UI approval card are stubs. The test
suites pin the contract and fail until each piece is implemented (red → green).

The factory can also **create and manage its own sub-agents** at runtime (like
Claude Code subagents) via a `SubAgentRegistry` and management tools, on top of
the seed roles.

### Run the tests

```bash
# Python (agent)
cd agent && pip install -e ".[dev]" && pytest -q

# TypeScript (ui)
cd ui && npm install && npm test
```

Expect failures: that is the intended starting state. Implement a stub, watch
its test go green.
