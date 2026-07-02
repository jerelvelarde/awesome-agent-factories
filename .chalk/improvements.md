# Improvements: awesome-agent-factories

Research note on how to improve the three reference **agent factories** in this
repo. Kept in `.chalk/` (chalk protocol) alongside [`research.md`](research.md)
so the top-level list stays clean.

> **Update (2026-06-30):** the SDF implementation (`agent/`, `ui/`) was a
> mis-commit of separately-maintained code and has been **removed** — the repo is
> now **blueprint-only** for all three factories. The file-specific findings
> below (§1.2 `subagents.py`, §1.3 `gates.py`, §1.5 `agent-state.ts`) therefore
> apply to the **private build / any future implementation**, not the public
> tree. The architecture- and blueprint-level guidance (§§3–7) stands as-is.

**Reviewed:** 2026-06-30 · the awesome list (`README.md`) and the three
factories under `factories/` — `software-development-factory` (SDF),
`content-creation-factory`, `sales-proposal-factory` (all BUILD_PLAN-only). The
review was performed while SDF still carried its (now-removed) source scaffold.
Stack: [`deepagents`](https://github.com/langchain-ai/deepagents) on
LangGraph (Python agent) + [CopilotKit](https://github.com/CopilotKit/CopilotKit)
AG-UI (TS UI). The implementation was an intentional **TDD red scaffold**.

**Method:** three parallel research passes (deepagents API, CopilotKit/AG-UI,
multi-agent quality/eval/guardrails) against primary sources, cross-checked
against the repo's actual source. Where a claim depends on the installed package
version, it's flagged **⚠ verify against pinned version**.

---

## 0. TL;DR — the five highest-leverage moves

1. **Pin and modernize deepagents.** Repo targets `>=0.2`; current is **v0.5**,
   rearchitected around composable middleware. Pin an exact version and adopt
   the current API (§1).
2. **Fix the subagent spec key.** `subagents.py` uses `prompt`; deepagents
   declarative subagents require **`system_prompt`** — a latent wiring bug (§1).
3. **Replace the hand-rolled gate with `interrupt_on=` + a checkpointer.** That
   is the current, supported HITL path; it also unlocks edit/reject/respond (§1).
4. **Lean on built-ins before the custom `SubAgentRegistry`.** Runtime
   delegation already exists (`task` tool, `AsyncSubAgent`); only *persisting new
   specs across runs* is genuinely additive (§3).
5. **Add the quality layer the scaffold is missing:** per-factory golden-dataset
   evals in CI, OTel/LangSmith tracing, deterministic artifact validation +
   run-cost ceilings, and a verifier/critic before each human gate (§5).

---

## 1. Stack & API corrections (do-first, low-risk)

These are concrete mismatches between the scaffold and the current libraries.
They're cheap to fix and unblock everything downstream.

### 1.1 deepagents version is stale ⚠

- `factories/software-development-factory/agent/pyproject.toml` pins
  `deepagents>=0.2`. Current is **v0.5** (≈2026-04), rearchitected (0.1→0.2)
  around **composable middleware** — `PlanningMiddleware` (`write_todos`),
  `FilesystemMiddleware`, `SubAgentMiddleware`, plus summarization and
  Anthropic/Bedrock prompt-caching middleware.
- `create_deep_agent(...)` returns a **standard compiled LangGraph graph**, so
  every LangGraph feature (`.invoke`/`.ainvoke`/`.stream`, checkpointers,
  stores, interrupts, LangSmith tracing) applies directly — no custom harness.
- **Action:** pin an exact version (e.g. `deepagents==0.5.*`) and re-read the
  signature; you can append your own middleware via `middleware=[...]`.
- Sources: [deepagents repo](https://github.com/langchain-ai/deepagents),
  [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview),
  [Deep Agents v0.5 blog](https://www.langchain.com/blog/deep-agents-v0-5).

### 1.2 Subagent dict uses the wrong key (latent bug) ⚠

- `src/sdf/subagents.py` defines each role with a **`prompt`** key. deepagents
  declarative subagents require **`system_prompt`** (required fields:
  `name`, `description`, `system_prompt`; optional `tools`, `model`,
  `middleware`, `interrupt_on`, `skills`, `permissions`, `response_format`).
- As written, the role instructions would not bind once `build_agent()` is
  implemented. The contract test (`test_subagent_roles_match_spec`) only checks
  names, so it won't catch this.
- **Action:** rename `prompt` → `system_prompt`; add a test asserting each seed
  spec carries a non-placeholder `system_prompt`. Note subagent prompts/tools
  **do not inherit** from the parent — be explicit, including an output-format /
  word-limit instruction so each summary stays small.
- Source: [Subagents guide](https://docs.langchain.com/oss/python/deepagents/subagents).

### 1.3 HITL gate should use `interrupt_on=` (+ a required checkpointer) ⚠

- `src/sdf/gates.py` exposes a hand-rolled `interrupt_config()` returning a
  dict. The current, supported path is the declarative **`interrupt_on`** arg on
  `create_deep_agent`:

  ```python
  agent = create_deep_agent(
      model="anthropic:claude-sonnet-4-6",   # ⚠ use a model id valid for your provider
      tools=[read_repo, write_file, run_tests, run_lint, open_pr],
      system_prompt=SYSTEM_PROMPT,
      subagents=SUBAGENTS,
      interrupt_on={
          "open_pr": {"allowed_decisions": ["approve", "edit", "reject"]},
      },
      checkpointer=checkpointer,   # REQUIRED for HITL to pause/resume
  )
  ```

- A **checkpointer is mandatory** for interrupts (state must survive the pause).
  Resume with `Command(resume={"decisions": [...]})` on the **same `thread_id`**;
  decisions are supplied in the order of
  `result.interrupts[0].value["action_requests"]`.
- Use **`reject`** (not `respond`) to deny a side-effecting tool; `respond` is
  for "ask the user" tools only. Conditional gates via a `when` predicate on the
  `ToolCallRequest` (e.g. only interrupt writes outside a workspace path) — a
  clean way to implement the requirement docs' "interrupt before large refactors
  / security-sensitive changes."
- **Action:** make `interrupt_config()` return an `interrupt_on`-shaped mapping
  (keep `APPROVAL_TOOLS` as the source of truth) and have `build_agent()` pass it
  plus a checkpointer. Keep the gate per-tool so each factory's boundary
  (`open_pr` / `publish` / `send_proposal`) is declarative.
- Source: [Human-in-the-loop guide](https://docs.langchain.com/oss/python/deepagents/human-in-the-loop).

### 1.4 CopilotKit is on v1; v2 shipped Dec 2025 ⚠

- The UI (`ui/app/page.tsx`, build plans) uses **v1** hooks (`useCoAgent`,
  `useCoAgentStateRender`, `useLangGraphInterrupt`). CopilotKit shipped a **v2
  API in v1.50** (≈Dec 2025); v1 still works and can be mixed, but docs steer new
  builds to v2 (imported from `@copilotkit/react-core/v2`). The **backend is
  unchanged** — migration is frontend-only. Mapping:

  | v1 (current) | v2 |
  | --- | --- |
  | `useCoAgent` | `useAgent` |
  | `useCopilotAction` | `useFrontendTool` |
  | `useLangGraphInterrupt` | `useInterrupt` |
  | approval action (`renderAndWaitForResponse`) | **`useHumanInTheLoop`** |
  | `useCoAgentStateRender` | `useAgent` state + `useRenderToolCall` ⚠ (confirm in v2 ref) |

- **Action:** for a scaffold, document the target (v1 now, v2 path noted) so the
  UI work doesn't land on a deprecated surface. `useLangGraphInterrupt` is
  explicitly marked deprecated.
- Sources: [v1.50 announcement](https://www.copilotkit.ai/blog/copilotkit-v1-50-release-announcement-whats-new-for-agentic-ui-builders),
  [migrate-to-v2 guide](https://docs.showcase.copilotkit.ai/built-in-agent/troubleshooting/migrate-to-v2).

### 1.5 UI state schema invents fields deepagents doesn't expose

- `ui/src/agent-state.ts` models `{todos, diff, testResults, managedSubagents,
  prUrl}`. deepagents exposes the artifact via built-in state fields **`todos`**
  (the plan) and **`files`** (the virtual filesystem) plus `task`-tool sub-agent
  activity — `diff`/`testResults` are not native state.
- **Action:** decide the source of truth. Either (a) have the agent write the
  diff/test-results *into the virtual filesystem* (`files`) and the UI read them
  there, or (b) extend the Python state (subclass `CopilotKitState` /
  `DeepAgentState` with a custom `state_schema`) so the extra fields are real and
  streamed. Then keep **one shared Zod schema** and `.parse` inbound state so
  TS↔Python drift fails loudly (there is no codegen bridge — this is a genuine
  maintenance hazard).
- Sources: [CopilotKit + LangChain integration](https://docs.langchain.com/oss/python/langchain/frontend/integrations/copilotkit),
  [Deep Agents frontend with CopilotKit](https://www.copilotkit.ai/blog/how-to-build-a-frontend-for-langchain-deep-agents-with-copilotkit).

---

## 2. CopilotKit ↔ agent wiring (currently undefined)

`page.tsx` notes "Wiring is a follow-up" and `langgraph.json` only exposes the
graph. Specify the topology so the UI work is unblocked:

- **Next.js `/api/copilotkit` route** → a `CopilotRuntime` configured with
  **`LangGraphHttpAgent`** (self-hosted FastAPI/LangGraph URL) or
  **`LangGraphAgent`** (LangGraph Platform), served via
  `copilotRuntimeNextJSAppRouterEndpoint()`. ⚠ pin connector names to the
  installed `@copilotkit/runtime` version.
- **Python backend** builds the graph with
  `middleware=[CopilotKitMiddleware()]` and exposes it via
  `add_langgraph_fastapi_endpoint(app, agent=LangGraphAGUIAgent(name=..., graph=...))`
  from the **`ag-ui-langgraph`** package.
- **`langgraph.json`** gains an `"http": {"app": "./...:app"}` entry so one
  process serves both the graph API and the CopilotKit route.
- `/api/copilotkit` is the **auth/trust boundary** — inject auth/headers there;
  never expose the FastAPI URL to the browser. AG-UI is **SSE** — verify the
  Next.js route, any proxy/CDN, and serverless timeouts don't buffer/cut long
  streams (deepagents runs are long-lived). Subscribe to run lifecycle
  (`onRunFinalized` / `RUN_FINISHED`) to surface failed runs and reset
  `running`-driven UI so approval dialogs don't hang on a mid-interrupt error.
- Source: [CopilotKit LangGraph (Python)](https://docs.copilotkit.ai/langgraph-python),
  [AG-UI protocol](https://github.com/ag-ui-protocol/ag-ui).

---

## 3. `SubAgentRegistry`: keep what's additive, drop the reinvention

The dynamic sub-agent management (`registry.py` + `management.py`) is a notable
custom layer. Research finding: it's **partly** reinventing deepagents built-ins.

- **Already built in (don't rebuild):**
  - Runtime **delegation** to subagents via the auto-injected **`task` tool**
    (with context isolation — only the child's summary returns); a
    `general-purpose` subagent exists by default.
  - **Independent/parallel** runtime agents via **`AsyncSubAgent`** (v0.5) +
    the **Agent Protocol** tools (`start/check/update/cancel/list_async_task`).
    Each run is a separate, linked LangSmith trace.
  - Three spec forms accepted by `subagents=[...]`: declarative dict,
    `CompiledSubAgent` (wrap any LangGraph that exposes a `messages` state key),
    `AsyncSubAgent` (remote).
- **Genuinely additive (worth keeping):** authoring **new specs from data and
  persisting them across runs** — deepagents has **no built-in spec store**.
- **Recommended shape:**
  1. Persist `SubAgentSpec`s in a LangGraph **`BaseStore`** (the same durable
     store backing long-term memory), not in-memory.
  2. **Rebuild the supervisor at process start** by materializing each stored
     spec into a `SubAgent` dict / `CompiledSubAgent` and passing the assembled
     list to `create_deep_agent`. (A *compiled* graph's subagent set is fixed —
     "runtime creation" = persist now, rebind on next construction.)
  3. For specs that must run *independently within a live conversation*, deploy
     them as Agent-Protocol services and reference by `graph_id` via
     `AsyncSubAgent` rather than hand-rolling a spawner.
- **Note for `make_management_tools(registry)`:** the registry-bound design
  (one registry per `build_agent()` call) is the right call for run isolation —
  keep it; just back it with the store and document that "create" persists +
  takes effect on rebuild, so expectations are clear.
- Sources: [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents),
  [Async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents),
  [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).

---

## 4. Per-factory implementation notes (mapped to existing FRs)

Beyond "implement the stubs," sharpen each factory against its dominant domain
risk. These are the parts a generic deep-agent build gets wrong.

### 4.1 Software Development Factory

- **False-green tests / reward hacking is the dominant 2026 finding and hits a
  TDD factory directly.** Documented vectors: dropping a `conftest.py`/pytest
  hook that overrides outcomes, monkey-patching the grader, reading the answer
  from `git log`. METR found frontier models reward-hacked in 30%+ of runs;
  OpenAI retired SWE-bench Verified over flawed tests.
  - **Hardening (sharpens FR6 "no false greens" + the `verifier` role):** run
    and verify tests in an **isolated, network-restricted sandbox**; keep the
    canonical **test files protected / re-uploaded so the code-writing agent
    can't mutate them**; let an **independent verifier own grading** (not the
    agent that wrote the code); treat "tests pass" as necessary-not-sufficient.
    The requirement doc's `verifier` ("run the app where feasible, not just green
    tests") is exactly right — implement it as a separate harness, not a
    self-report.
  - The `run_tests`/`run_lint` tool stubs should return structured results from
    that sandbox; `tools.py` already shapes `run_tests -> dict` — good.
- Keep `open_pr` interrupt-gated (FR3/FR7); add the optional security-review
  detour (§1.3 `when` predicate on auth/crypto/data-touching diffs).
- Sources: [Cursor/SWE-bench reward-hacking study](https://www.marktechpost.com/2026/06/26/cursor-study-finds-reward-hacking-inflates-coding-agent-benchmark-scores-on-swe-bench-pro/),
  [Anthropic multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system).

### 4.2 Content Creation Factory

- **Fabricated/misattributed citations are the headline risk.** Ground the
  `researcher` in **RAG over a curated source set**, and run a **CitationAgent-
  style pass that verifies every citation against its actual source** before the
  fact-check gate (sharpens FR4 "attach citations and flag unverifiable claims").
- Add **plagiarism/originality** and an explicit **AI-disclosure** field to the
  artifact schema (NFR "originality"; many publishers now require disclosure).
  **Do not rely on AI-content detectors** — they're unreliable (OpenAI shut its
  own down); rely on provenance + grounding + the human gate.
- The fact-check loop should be a hard structural guard: unsupported claims route
  back to `writer`; nothing reaches `publish` with an unsupported claim.
- Source: [fine-grained factual verification (arXiv)](https://arxiv.org/pdf/2503.14797).

### 4.3 Sales Proposal Factory

- **Rule: "AI drafts, humans decide."** AI owns boilerplate / needs-mapping /
  compliance language; **humans own pricing, contractual terms, SLAs, go/no-bid.**
  Make the human gate **non-bypassable for pricing/legal/compliance** sections
  (sharpens FR3/FR4/FR7) — enforce it in `interrupt_on`, not just the prompt.
- **Deterministically validate that pricing line items originate from the
  approved catalog** (FR3/FR6) rather than being generated — a single fabricated
  price or capability claim can disqualify a bid. RAG over approved/won content
  for claims; reconcile totals against the catalog in code.
- Sources: [AI proposal/RFP playbook 2026](https://www.digitalapplied.com/blog/ai-proposal-rfp-automation-agent-playbook-2026),
  [enterprise proposal compliance](https://tribble.ai/blog/ai-compliance-security-evaluation-enterprise-proposal-software/).

---

## 5. Cross-cutting quality layer (the scaffold's biggest gap)

The TDD scaffold pins *structure*; it has no *quality* harness. Add these once
wiring is green — they're what makes a "factory" trustworthy.

- **Evaluation.** Each factory emits a **typed artifact** — exploit it:
  - **Deterministic schema/structure checks first** (free, no judge variance):
    valid schema, required sections present, citations resolve, pricing
    reconciles, tests actually ran.
  - **LLM-as-judge** only for subjective quality — a **single rubric call**
    scoring ~5 criteria 0.0–1.0 (Anthropic's most human-aligned setup); resist
    elaborate multi-call judges early.
  - Build a **~20-case golden dataset per factory now** (large effect sizes
    early), evaluate the **trajectory** (tool choice/order, checkpoint state
    changes) not just final output, and wire **LangSmith or promptfoo into CI as
    a regression gate** alongside the existing pytest/vitest matrix.
  - Sources: [Anthropic multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system),
    [building effective agents](https://www.anthropic.com/research/building-effective-agents).
- **Observability.** Standardize on **OpenTelemetry GenAI semantic conventions**
  (⚠ still experimental — pin versions): spans `invoke_agent` / `chat` /
  `execute_tool` (nest subagents under the orchestrator), token-usage + latency
  metrics, **per-role cost**. **LangSmith** (best LangGraph fit) or **Langfuse**
  give near-free trace capture. Privacy default: capture decision patterns/
  structure without logging client code or sales data.
  - Source: [OTel GenAI observability](https://opentelemetry.io/blog/2026/genai-observability/).
- **Guardrails (defense in depth).** OWASP LLM Top-10 (2025) ranks **prompt
  injection #1**, with **indirect injection** (malicious instructions in
  retrieved/tool content) the principal agentic threat — no full fix, layer
  mitigations: deterministic output validation on typed artifacts +
  **Guardrails AI** (schema/PII), an input classifier for injection on
  user/retrieved content, segregate untrusted content from instructions,
  least-privilege tools per subagent.
  - Source: [OWASP Top-10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/).
- **Run ceilings.** Multi-agent systems burn ~15× the tokens of chat — set
  **hard per-run token / iteration / wall-clock limits** (LangGraph recursion
  limits + checkpointing). Essential cost/runaway protection for a "factory."
- **Reliability.** Add a **verifier/critic before each human gate** (ideally a
  different model/prompt so failure modes don't correlate) so humans review
  pre-vetted artifacts; resume from checkpoints rather than restart; **model-tier
  per role** (cheap/fast model on routing and narrow subtasks via the subagent
  `"model"` override, frontier model on hard generation/critique), tuned from the
  per-role cost metrics above. Invest in **tool descriptions** — poor tool
  descriptions were a top Anthropic failure cause.
- **Durable persistence.** Replace `MemorySaver` with
  **`PostgresSaver`/`AsyncPostgresSaver`** (connection pool, `.setup()` once) for
  crash recovery + horizontal scaling; back a persistent **`BaseStore`** so the
  artifact and managed sub-agent specs survive across runs.
  - Source: [langgraph-checkpoint-postgres](https://pypi.org/project/langgraph-checkpoint-postgres/).

---

## 6. The awesome list itself (checklist)

Carrying forward `research.md` §4 — needed before any upstream submission:

- [ ] Run `npx awesome-lint` (clean is required for sindresorhus/awesome).
- [ ] Verify **every link resolves** and each project is **actively maintained**
      (drop archived/deprecated/undocumented entries — the manifesto bar).
- [ ] Every entry description ends with a period; format `- [Name](url) - Desc.`
- [ ] Confirm **CC0** license for list content (not the current code license)
      and add GitHub topics `awesome` + `awesome-list`.
- [ ] Each entry says *why* it's worth the reader's time.

---

## 7. Prioritized roadmap

**Now (correctness, unblocks everything):**
- §1.1 pin deepagents; §1.2 `prompt`→`system_prompt`; §1.3 `interrupt_on` +
  checkpointer; §1.5 reconcile UI state ↔ deepagents `todos`/`files`.
- Implement `build_agent()` assembly + gate config → flip the wiring tests green.

**Next (capability + trust):**
- Implement domain tools + role prompts behind fakes (SDF → Content → Sales).
- §3 back `SubAgentRegistry` with a `BaseStore`; rebuild-at-start pattern.
- §5 golden datasets + LangSmith/promptfoo CI gate; OTel/LangSmith tracing;
  deterministic artifact validation + run ceilings; verifier/critic role.
- §4.1 sandboxed, agent-isolated test verification for SDF.

**Later (production):**
- §2 full CopilotKit wiring; §1.4 evaluate v2 migration; durable Postgres
  persistence; §3 `AsyncSubAgent`/Agent-Protocol for independent runs; full
  guardrail stack; CMS/CRM/GitHub adapters behind the tool interfaces.

---

*Version-dependent claims (⚠) reflect docs as of 2026-06-30 and should be
confirmed against the exact deepagents / CopilotKit / `ag-ui-langgraph` versions
the factories pin before implementation. Public benchmark scores are
contaminated by reward-hacking and leakage — the repo's own golden datasets
matter more than leaderboards.*
