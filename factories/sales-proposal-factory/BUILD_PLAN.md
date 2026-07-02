# Build Plan: Sales Proposal Factory

Implements [`requirements/sales-proposal-factory.md`](../../requirements/sales-proposal-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green. Design reflects the researched best practices in
[`.chalk/improvements.md`](../../.chalk/improvements.md) (pin an exact
`deepagents` version — the API tracks the current 0.5 middleware model).

**Produces:** new proposals — tailored, priced, compliance-checked.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the proposal workspace (virtual filesystem), and two
approval gates (HITL interrupts) come from `deepagents`. `create_deep_agent(...)`
returns a standard compiled LangGraph graph, so checkpointers, stores, streaming,
and tracing all apply directly.

```
build_agent(checkpointer, store) -> create_deep_agent(
    model         = "anthropic:claude-sonnet-4-6",  # provider-prefixed; tier per sub-agent
    system_prompt = "Turn prospect context into a tailored, accurate proposal.
                     Price only from the catalog; never send without human
                     approval, and escalate out-of-policy pricing.",
    tools         = [crm_lookup, price_catalog, write_file, render_doc,
                     send_proposal, crm_write],
    subagents     = [account_researcher, solution_architect, pricing_agent,
                     proposal_writer, compliance_reviewer, personalizer],
    interrupt_on  = {
        "send_proposal": {"allowed_decisions": ["approve", "reject"]},
        "price_catalog": {"allowed_decisions": ["approve", "edit", "reject"],
                          "when": out_of_policy},   # predicate on the ToolCallRequest
    },
    checkpointer  = checkpointer,   # REQUIRED for HITL pause/resume
    store         = store,          # catalog / approved language / managed sub-agent specs
)
```

### Sub-agents (`subagents.py`)

Each sub-agent is a spec `{name, description, system_prompt, tools, model?}`
(note the key is **`system_prompt`**, not `prompt`; specs do not inherit the
parent's prompt/tools, so each is explicit and includes an output-format limit
so summaries stay small).

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `account_researcher` | Enrich + summarize prospect from CRM/notes | `crm_lookup` |
| `solution_architect` | Map needs → offerings + outcomes | filesystem |
| `pricing_agent` | Build line items/total within discount rules | `price_catalog` |
| `proposal_writer` | Draft proposal from template | `write_file` |
| `compliance_reviewer` | Accuracy + legal/approved-language check | filesystem |
| `personalizer` | Tailor + render final document | `render_doc` |

Give each sub-agent only the tools it needs, and write action-oriented
`description`s — the orchestrator routes on them. Model-tier per role: a fast
model for `account_researcher`/`personalizer`, a frontier model for
`solution_architect`/`compliance_reviewer`.

### Dynamic sub-agent management

Runtime delegation is **mostly built in**: deepagents auto-injects a `task` tool
(context-isolated sub-agent calls) and a default `general-purpose` sub-agent, and
`AsyncSubAgent` (+ the Agent Protocol) covers independent/parallel runs. The
genuinely additive part is **authoring and persisting new specs across runs** —
deepagents has no spec store. So the `SubAgentRegistry` (`registry.py`) +
management tools (`management.py`: `create_subagent`, `list_subagents`,
`update_subagent`, `delete_subagent`) persist specs in the LangGraph **`BaseStore`**
and the supervisor is **rebuilt at process start** from stored specs — e.g. an
industry- or product-line specialist. The registry is bound per `build_agent()`
call for run isolation.

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`, exposed as state
  `todos`).
- Prospect summary, solution map, pricing, and draft live in the **virtual
  filesystem** (state `files`), backed by a `StoreBackend` so they survive across
  runs.
- The deliverable is a **rendered proposal**, then a **CRM write-back**.

### Persistence & durability

`MemorySaver` is dev-only. In production use **`PostgresSaver`/`AsyncPostgresSaver`**
(connection pool, `.setup()` once) plus a persistent **`BaseStore`** for the
product/pricing catalog, legal-approved language, templates, and managed
sub-agent specs. Anthropic/Bedrock prompt caching is automatic on the stable
template/boilerplate sections of the system prompt.

### Approval gates (`gates.py`)

- HITL via the declarative **`interrupt_on`** map (a checkpointer is required;
  resume with `Command(resume={"decisions": [...]})` on the same `thread_id`):
  - `send_proposal` pauses for human approval — the send boundary (FR7).
  - `price_catalog` pauses **only when out of policy** (a `when` predicate on the
    `ToolCallRequest`, FR4); in-policy pricing proceeds. This gate is
    **non-bypassable** for pricing/legal/compliance.
- **Pricing-reconciliation guard:** line items must sum to the total, and every
  line item must **originate from the approved catalog** (validated in code, not
  generated) — a single fabricated price can disqualify a bid.

## Quality & hardening

The scaffold pins structure; these make it trustworthy (add once wiring is green):

- **Eval:** deterministic checks on the typed artifact first (pricing reconciles
  and comes from the catalog, only legal-approved boilerplate used, required
  sections present), then LLM-as-judge (single rubric call) for persuasiveness.
  Build a ~20-case golden dataset and eval the **trajectory**, gating in CI via
  LangSmith or promptfoo.
- **Observability:** OTel GenAI conventions (per-role token/cost) via LangSmith or
  Langfuse; hard per-run token/iteration/wall-clock ceilings.
- **Domain hardening — "AI drafts, humans decide":** AI owns boilerplate,
  needs-mapping, and compliance-mapping; **humans own pricing, contractual terms,
  SLAs, and go/no-bid.** Keep the pricing/legal gate **non-bypassable by design**
  (enforced in `interrupt_on`, not just the prompt); ground claims via **RAG over
  approved/won content** and have `compliance_reviewer` verify each cited claim
  against the knowledge base.

## UI (CopilotKit)

- Render the plan/proposal off deepagents state — `state.todos` (plan) and
  `state.files` (solution map, itemized pricing, compliance flags) — via
  `useCoAgent` (v1) / `useAgent` (v2). Keep the shared state schema as **one Zod
  schema** and `.parse` inbound state so TS↔Python drift fails loudly; subclass
  `CopilotKitState` on the Python side. The schema **rejects a line item not in
  the catalog**.
- The out-of-policy pricing and `send_proposal` gates render approve/deny cards
  via **`useHumanInTheLoop`** (v2) or `useInterrupt`. Both need a checkpointer +
  stable `threadId`.
- Wiring: Next.js `/api/copilotkit` → `CopilotRuntime` with `LangGraphHttpAgent`;
  Python builds the graph with `CopilotKitMiddleware` and exposes it via
  `add_langgraph_fastapi_endpoint` (`ag-ui-langgraph`); `langgraph.json` gains an
  `"http"` app entry. `/api/copilotkit` is the auth boundary (prospect data). Note
  the CopilotKit **v2** API (Dec 2025) is the forward path; v1 hooks still work.

## Failing tests (red)

`agent/tests/`
- `test_agent.py` (RED until wired): `build_agent()` returns a deep agent with
  the six named sub-agents and expected tools.
- `test_tools.py` (RED): `crm_lookup`/`price_catalog`/`send_proposal`/… honor
  signatures; stubs raise `NotImplementedError`. `price_catalog` only emits
  catalog line items and reconciles lines to total.
- `test_gates.py` (RED): out-of-policy pricing interrupts before acceptance;
  in-policy pricing does not; the agent interrupts **before** `send_proposal`.
- `test_registry.py`: seeding + read access pass; `create`/`delete` of a managed
  sub-agent are RED until implemented.
- `test_management.py` (RED): `create_subagent`/`list_subagents`/… return/manage
  specs.

`ui/test/`
- `agent-state.test.ts` — zod schema for `{todos, prospect, solutionMap,
  pricing, compliance, document}` round-trips; rejects a line item not in the
  catalog.
- `hitl.test.ts` — approval cards render on the pricing and `send_proposal`
  interrupts (stub → RED).

## Green milestones

1. Assemble `build_agent()` + `interrupt_on`/checkpointer config → agent/gate
   tests pass with stubs.
2. Implement tools, then role prompts (`account_researcher` →
   `solution_architect`/`pricing_agent` → `proposal_writer`/`compliance_reviewer`
   → `personalizer`) → tool/behavior tests pass.
3. Add the quality layer (catalog-origin pricing validation, golden dataset + CI
   gate, tracing, run ceilings, RAG over approved content).
4. Wire CopilotKit to live state; connect real CRM/CPQ/doc-gen/e-sign adapters
   behind tool interfaces; keep pricing and send gates human-owned.

## Integrations

CRM (Salesforce/HubSpot), CPQ/pricing, document generation (PDF/DOCX/Slides),
e-signature, approval workflows — all behind tool interfaces so tests use fakes.
