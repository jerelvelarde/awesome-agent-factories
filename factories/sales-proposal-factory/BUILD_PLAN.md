# Build Plan: Sales Proposal Factory

Implements [`requirements/sales-proposal-factory.md`](../../requirements/sales-proposal-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green.

**Produces:** new proposals — tailored, priced, compliance-checked.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the proposal workspace (virtual filesystem), and two
approval gates (HITL interrupts) come from `deepagents`.

```
build_agent() -> create_deep_agent(
    model        = <Claude model>,
    system_prompt= "Turn prospect context into a tailored, accurate proposal.
                    Price only from the catalog; never send without human
                    approval, and escalate out-of-policy pricing.",
    tools        = [crm_lookup, price_catalog, write_file, render_doc,
                    send_proposal, crm_write],
    subagents    = [account_researcher, solution_architect, pricing_agent,
                    proposal_writer, compliance_reviewer, personalizer],
)
```

### Sub-agents (`subagents.py`)

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `account_researcher` | Enrich + summarize prospect from CRM/notes | `crm_lookup` |
| `solution_architect` | Map needs → offerings + outcomes | filesystem |
| `pricing_agent` | Build line items/total within discount rules | `price_catalog` |
| `proposal_writer` | Draft proposal from template | `write_file` |
| `compliance_reviewer` | Accuracy + legal/approved-language check | filesystem |
| `personalizer` | Tailor + render final document | `render_doc` |

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`).
- Prospect summary, solution map, pricing, and draft live in the **virtual
  filesystem**.
- The deliverable is a **rendered proposal**, then a **CRM write-back**.

### Approval gates (`gates.py`)

- HITL interrupt **before `send_proposal`** — human owns the send boundary (FR7).
- Conditional HITL interrupt **before pricing is accepted when out of policy**
  (FR4): the `price_catalog` tool flags out-of-policy totals and pauses for
  approval; in-policy pricing proceeds.
- Pricing-reconciliation guard: line items must sum to the total.

## UI (CopilotKit)

- `useCoAgent` streams the todo list and current sub-agent (research → solution →
  price → write → compliance → personalize) live.
- `useCoAgentStateRender` renders the solution map, the itemized pricing, and
  compliance flags as they update.
- The out-of-policy pricing and `send_proposal` interrupts render
  **approve/deny** cards before proceeding.

## Failing tests (red)

`agent/tests/`
- `test_agent.py` (RED until wired): `build_agent()` returns a deep agent with
  the six named sub-agents and expected tools.
- `test_tools.py` (RED): `crm_lookup`/`price_catalog`/`send_proposal`/… honor
  signatures; stubs raise `NotImplementedError`. `price_catalog` only emits
  catalog line items and reconciles lines to total.
- `test_gates.py` (RED): out-of-policy pricing interrupts before acceptance;
  in-policy pricing does not; the agent interrupts **before** `send_proposal`.

`ui/test/`
- `agent-state.test.ts` — zod schema for `{todos, prospect, solutionMap,
  pricing, compliance, document}` round-trips; rejects a line item not in the
  catalog.
- `hitl.test.ts` — approval cards render on the pricing and `send_proposal`
  interrupts (stub → RED).

## Green milestones

1. Assemble `build_agent()` + gate config → agent/gate tests pass with stubs.
2. Implement tools, then role prompts (`account_researcher` →
   `solution_architect`/`pricing_agent` → `proposal_writer`/`compliance_reviewer`
   → `personalizer`) → tool/behavior tests pass.
3. Wire CopilotKit to live state; connect real CRM/CPQ/doc-gen/e-sign adapters
   behind tool interfaces; keep pricing and send gates human-owned.

## Integrations

CRM (Salesforce/HubSpot), CPQ/pricing, document generation (PDF/DOCX/Slides),
e-signature, approval workflows — all behind tool interfaces so tests use fakes.
