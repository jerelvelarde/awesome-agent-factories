# Build Plan: Sales Proposal Factory

Implements [`requirements/sales-proposal-factory.md`](../../requirements/sales-proposal-factory.md)
as a standalone LangGraph project. TDD: red scaffold first, then green.

## Graph design

State graph modeling research → solution → price → draft → review with a
pricing approval gate and a send gate.

### State (`state.py`)

```
prospect: Prospect              # company, industry, size, CRM record, notes
needs: list[Need]               # stated requirements / pain points
solution_map: list[Mapping]     # need -> offering + outcome
pricing: Pricing | None         # {lines, total, in_policy: bool}
approvals: dict[str, bool]      # {"pricing": bool, "send": bool}
document: str | None            # rendered proposal
compliance: Compliance | None   # {issues: [...], ok: bool}
crm_writeback: dict | None
iteration: int                  # compliance loop counter
```

### Nodes (one agent role each, `nodes/`)

| Node | Role | Output keys |
| --- | --- | --- |
| `account_researcher` | Enrich + summarize prospect from CRM/notes | `prospect` |
| `solution_architect` | Map needs → offerings + outcomes | `solution_map` |
| `pricing_agent` | Build line items/total within discount rules | `pricing` |
| `pricing_gate` | `interrupt` when pricing is out of policy | `approvals["pricing"]` |
| `proposal_writer` | Draft proposal from template | `document` |
| `compliance_reviewer` | Accuracy + legal/approved-language check | `compliance` |
| `personalizer` | Tailor + format final document | `document` (final) |
| `send_gate` | `interrupt` for human approval before sending | `approvals["send"]` |
| `crm_writer` | Write outcome back to CRM | `crm_writeback` |

### Edges / routing (`graph.py`, `guardrails.py`)

```
START → account_researcher → solution_architect → pricing_agent
pricing_agent --out_of_policy--> pricing_gate → proposal_writer
pricing_agent --in_policy------> proposal_writer
proposal_writer → compliance_reviewer
compliance_reviewer --has_issues--> proposal_writer   (loop, bounded)
compliance_reviewer --ok---------> personalizer → send_gate → crm_writer → END
```

- `pricing_gate` fires only when `pricing.in_policy` is false (FR4, guardrail).
- `send_gate` is a hard interrupt; nothing is sent externally until
  `approvals["send"]` is true (FR7, guardrail).
- `pricing_reconciles(state)` asserts line items sum to total (no math drift).

## Failing tests (red)

`python/tests/`
- `test_state.py` — `Prospect`/`Pricing` validation; reject pricing whose lines
  don't sum to total.
- `test_graph.py` (RED until wired):
  - graph compiles and exposes the 9 nodes;
  - out-of-policy pricing routes through `pricing_gate` (interrupt);
  - in-policy pricing skips the gate;
  - `compliance_reviewer` issues route back to `proposal_writer`;
  - `crm_writer` is unreachable until `approvals["send"]` is true.
- `test_nodes.py` (RED): each node returns its declared output key(s); stubs
  raise `NotImplementedError`. `pricing_agent` only emits catalog line items.

`typescript/test/`
- `schema.test.ts` — `Pricing`/`Mapping` zod schemas round-trip; reject a line
  item not in the catalog.
- `client.test.ts` — CLI accepts a prospect id and invokes the graph (stub → RED).

## Green milestones

1. Wire `build_graph()` + routing → structure/routing/gate tests pass.
2. Implement `account_researcher`, then `solution_architect`/`pricing_agent`,
   then `proposal_writer`, `compliance_reviewer`, `personalizer` → node tests
   pass one by one.
3. Wire real CRM/CPQ/doc-gen/e-sign adapters behind interfaces; keep pricing and
   send gates human-owned.

## Integrations

CRM (Salesforce/HubSpot), CPQ/pricing, document generation (PDF/DOCX/Slides),
e-signature, approval workflows. All behind interfaces so tests use fakes.
