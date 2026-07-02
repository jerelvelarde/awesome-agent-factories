# Software Development Factory

A blueprint for an agent factory that produces **new software** — a reviewed,
tested draft pull request — from a feature request or ticket.

See [`BUILD_PLAN.md`](BUILD_PLAN.md) for the design and
[`../../requirements/software-development-factory.md`](../../requirements/software-development-factory.md)
for the requirements.

## What it produces

A working branch and a **draft pull request** with a change summary, the plan,
test evidence, and follow-up notes — built by a supervised pipeline of
role-specialized agents (planner, implementer, test engineer, reviewer,
verifier, integrator) with a human approval gate before the PR opens.

## Reference stack

- **Harness & orchestration:** [`deepagents`](https://github.com/langchain-ai/deepagents)
  on LangGraph — planning, a virtual filesystem for the code workspace,
  sub-agent context isolation, and human-in-the-loop interrupts.
- **UI:** [CopilotKit](https://github.com/CopilotKit/CopilotKit) (AG-UI) —
  renders the plan, sub-agent activity, the diff, and the approval gate.

## Status

This repository hosts the **open blueprint** (requirements + build plan). The
implementation is maintained separately; this directory is intentionally
blueprint-only, matching the other reference factories.
