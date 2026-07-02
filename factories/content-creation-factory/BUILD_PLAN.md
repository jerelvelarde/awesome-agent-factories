# Build Plan: Content Creation Factory

Implements [`requirements/content-creation-factory.md`](../../requirements/content-creation-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green. Design reflects the researched best practices in
[`.chalk/improvements.md`](../../.chalk/improvements.md) (pin an exact
`deepagents` version — the API tracks the current 0.5 middleware model).

**Produces:** new content — publish-ready pieces plus channel variants.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the draft workspace (virtual filesystem), and the
publish gate (HITL interrupt) come from `deepagents`. `create_deep_agent(...)`
returns a standard compiled LangGraph graph, so checkpointers, stores, streaming,
and tracing all apply directly.

```
build_agent(checkpointer, store) -> create_deep_agent(
    model         = "anthropic:claude-sonnet-4-6",  # provider-prefixed; tier per sub-agent
    system_prompt = "Turn the brief into publish-ready, on-brand, fact-checked
                     content. Ground every claim in a source; never publish
                     without human approval.",
    tools         = [web_search, fetch_url, write_file, check_style, publish],
    subagents     = [researcher, strategist, writer, editor,
                     fact_checker, formatter],
    interrupt_on  = {"publish": {"allowed_decisions": ["approve", "edit", "reject"]}},
    checkpointer  = checkpointer,   # REQUIRED for HITL pause/resume
    store         = store,          # brand kit / source corpus / managed sub-agent specs
)
```

### Sub-agents (`subagents.py`)

Each sub-agent is a spec `{name, description, system_prompt, tools, model?}`
(note the key is **`system_prompt`**, not `prompt`; specs do not inherit the
parent's prompt/tools, so each is explicit and includes an output-format limit
so summaries stay small).

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `researcher` | Gather + cite sources, build factual outline | `web_search`, `fetch_url` |
| `strategist` | Set angle, hook, channel structure | filesystem |
| `writer` | Draft in brand voice | `write_file` |
| `editor` | Clarity/flow, enforce style guide | `check_style` |
| `fact_checker` | Verify claims vs sources, flag unsupported | filesystem |
| `formatter` | Repurpose into channel variants + metadata | `write_file` |

Give each sub-agent only the tools it needs, and write action-oriented
`description`s — the orchestrator routes on them. Model-tier per role: a fast
model for `strategist`/`formatter`, a frontier model for `writer`/`fact_checker`.

### Dynamic sub-agent management

Runtime delegation is **mostly built in**: deepagents auto-injects a `task` tool
(context-isolated sub-agent calls) and a default `general-purpose` sub-agent, and
`AsyncSubAgent` (+ the Agent Protocol) covers independent/parallel runs. The
genuinely additive part is **authoring and persisting new specs across runs** —
deepagents has no spec store. So the `SubAgentRegistry` (`registry.py`) +
management tools (`management.py`: `create_subagent`, `list_subagents`,
`update_subagent`, `delete_subagent`) persist specs in the LangGraph **`BaseStore`**
and the supervisor is **rebuilt at process start** from stored specs — e.g. an
`seo_specialist` or a per-channel writer. The registry is bound per
`build_agent()` call for run isolation.

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`, exposed as state
  `todos`).
- Sources, outline, draft, and variants live in the **virtual filesystem** (state
  `files`), backed by a `StoreBackend` so they survive across runs.
- The deliverable is the **approved piece + channel variants**.

### Persistence & durability

`MemorySaver` is dev-only. In production use **`PostgresSaver`/`AsyncPostgresSaver`**
(connection pool, `.setup()` once) plus a persistent **`BaseStore`** for the brand
kit/voice profile, the curated source corpus, the `StoreBackend` draft, and
managed sub-agent specs. Anthropic/Bedrock prompt caching is automatic on the
stable brand/voice sections of the system prompt.

### Approval gates (`gates.py`)

- HITL via the declarative **`interrupt_on`** map: `publish` pauses for human
  approval — the publish boundary (FR7). A checkpointer is required; resume with
  `Command(resume={"decisions": [...]})` on the same `thread_id`. Use **`reject`**
  to send an unpublished piece back with feedback.
- **Fact-check hard guard:** the `fact_checker` routes unsupported claims back to
  `writer`; nothing reaches `publish` with an unsupported claim (accuracy NFR).

## Quality & hardening

The scaffold pins structure; these make it trustworthy (add once wiring is green):

- **Eval:** deterministic checks on the typed artifact first (every claim has a
  resolvable citation, style-guide/terminology pass, required metadata present),
  then LLM-as-judge (single rubric call) for voice/quality. Build a ~20-case
  golden dataset and eval the **trajectory**, gating in CI via LangSmith or
  promptfoo.
- **Observability:** OTel GenAI conventions (per-role token/cost) via LangSmith or
  Langfuse; hard per-run token/iteration/wall-clock ceilings.
- **Domain hardening — fabricated citations** (the headline content risk): ground
  the `researcher` in **RAG over a curated source set**, and run a
  **CitationAgent-style verification** of every citation against its actual source
  before the publish gate (a `fact_checker`/`researcher` critic pair). Add
  **plagiarism/originality** and an explicit **AI-disclosure** field to the
  artifact schema. Do **not** rely on AI-content detectors (unreliable) — rely on
  provenance + grounding + the human gate.

## UI (CopilotKit)

- Render the plan/draft off deepagents state — `state.todos` (plan) and
  `state.files` (draft, sources, fact-check flags) — via `useCoAgent` (v1) /
  `useAgent` (v2). Keep the shared state schema as **one Zod schema** and `.parse`
  inbound state so TS↔Python drift fails loudly; subclass `CopilotKitState` on the
  Python side. The schema **rejects a claim with no source**.
- The `publish` gate renders an approve/edit/deny card via **`useHumanInTheLoop`**
  (v2) or `useInterrupt`. Both need a checkpointer + stable `threadId`.
- Wiring: Next.js `/api/copilotkit` → `CopilotRuntime` with `LangGraphHttpAgent`;
  Python builds the graph with `CopilotKitMiddleware` and exposes it via
  `add_langgraph_fastapi_endpoint` (`ag-ui-langgraph`); `langgraph.json` gains an
  `"http"` app entry. Note the CopilotKit **v2** API (Dec 2025) is the forward
  path; v1 hooks still work.

## Failing tests (red)

`agent/tests/`
- `test_agent.py` (RED until wired): `build_agent()` returns a deep agent with
  the six named sub-agents and expected tools.
- `test_tools.py` (RED): `web_search`/`fetch_url`/`publish`/… honor their
  signatures; stubs raise `NotImplementedError`. `researcher` output carries
  ≥1 cited source.
- `test_gates.py` (RED): the agent interrupts **before** `publish` and does not
  publish without approval.
- `test_registry.py`: seeding + read access pass; `create`/`delete` of a managed
  sub-agent are RED until implemented.
- `test_management.py` (RED): `create_subagent`/`list_subagents`/… return/manage
  specs.

`ui/test/`
- `agent-state.test.ts` — zod schema for `{todos, sources, draft, factcheck,
  variants}` round-trips; rejects a claim with no source.
- `hitl.test.ts` — the approval card renders on the `publish` interrupt (stub → RED).

## Green milestones

1. Assemble `build_agent()` + `interrupt_on`/checkpointer config → agent/gate
   tests pass with stubs.
2. Implement tools, then role prompts (`researcher` → `writer`/`editor` →
   `fact_checker` → `formatter`) → tool/behavior tests pass.
3. Add the quality layer (citation-verification pass, golden dataset + CI gate,
   tracing, run ceilings, plagiarism/AI-disclosure fields).
4. Wire CopilotKit to live state; connect real CMS/social/image adapters behind
   tool interfaces; keep publish human-owned.

## Integrations

CMS (WordPress/Webflow), social schedulers, Google Docs/Notion, image
generation, SEO tools — all behind tool interfaces so tests use fakes.
