# Requirements: Software Development Factory

## 1. Overview

The Software Development Factory is an agent factory that turns a feature
request or product brief into working, reviewed, and tested software through a
coordinated team of specialized AI agents. It models a small engineering org —
planning, implementation, review, and verification — so a single human request
can produce a mergeable pull request with minimal manual orchestration.

## 2. Goals & Non-Goals

### Goals
- Convert a natural-language brief or ticket into a working, tested change.
- Enforce a plan → implement → review → verify loop on every unit of work.
- Produce artifacts a human can audit: a plan, a diff, tests, and a summary.
- Keep a human in the loop at defined approval gates.

### Non-Goals
- Fully autonomous production deploys without human approval.
- Replacing the human reviewer of record for security-sensitive changes.
- Greenfield product strategy or business prioritization.

## 3. Users & Personas

| Persona | Need |
| --- | --- |
| Individual developer | Offload scoped tasks and bug fixes end to end. |
| Tech lead | Parallelize backlog work while keeping review control. |
| Product owner | File a brief and receive a reviewable PR with a summary. |

## 4. Inputs

- A task description: ticket, brief, bug report, or failing test.
- Repository access (read/write to a working branch).
- Project context: language, framework, conventions, CLAUDE.md / docs.
- Constraints: target branch, definition of done, coding standards.

## 5. Agent Architecture

A supervised pipeline of role-specialized agents:

1. **Planner** — decomposes the brief into a step-by-step plan, identifies
   files to touch, and flags architectural trade-offs. Output gated for human
   approval on large changes.
2. **Implementer** — writes code matching existing conventions, in small,
   reviewable increments.
3. **Test Engineer** — writes or updates unit/integration tests and ensures
   they fail before and pass after the change.
4. **Reviewer** — performs a correctness and quality pass on the diff;
   requests changes back to the Implementer until clean.
5. **Verifier** — runs the build, linters, and tests; runs the app where
   feasible to confirm behavior, not just green tests.
6. **Integrator** — opens a draft PR with a summary, plan, and test evidence.

A **Supervisor/Orchestrator** routes work between agents, enforces the loop,
manages retries, and escalates to the human at approval gates.

## 6. Outputs / Deliverables

- A working branch with incremental commits.
- A draft pull request including: change summary, the plan, test results, and
  any follow-up notes.
- Passing build, lint, and test runs (or a clear report of what failed).

## 7. Functional Requirements

- FR1: Accept a task from a ticket, chat message, or PR comment.
- FR2: Produce an explicit plan before writing code.
- FR3: Require human approval before large or architecturally significant work.
- FR4: Write code that matches the repository's existing style and idioms.
- FR5: Add or update tests for every behavioral change.
- FR6: Run build/lint/tests and report results faithfully (no false greens).
- FR7: Open a draft PR; never push to a protected branch directly.
- FR8: Respond to review comments and CI failures iteratively.

## 8. Non-Functional Requirements

- Auditability: every change traces back to a plan and a human-readable diff.
- Safety: scoped repo permissions; no secret exfiltration; no destructive ops
  without confirmation.
- Reproducibility: runs from a clean checkout; environment captured in setup.
- Cost/latency: configurable model tiers per agent role.

## 9. Integrations

GitHub/GitLab, CI providers, issue trackers, package registries, and an
isolated execution sandbox for build/test.

## 10. Guardrails & Quality

- Hard gate: human approval required to merge.
- No edits to files the agent didn't create that contradict their stated
  purpose without surfacing the conflict.
- Security review step for auth, crypto, or data-handling changes.

## 11. Success Metrics

- % of tasks reaching a mergeable PR without human code edits.
- Review iterations per PR (lower is better).
- Escaped-defect rate post-merge.
- Time from brief to draft PR.

## 12. Open Questions

- Default model tier per role and escalation policy.
- How much repo context to load vs. retrieve on demand.
- Policy for multi-repo / cross-service changes.
