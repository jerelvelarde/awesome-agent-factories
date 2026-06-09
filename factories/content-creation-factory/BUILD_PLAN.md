# Build Plan: Content Creation Factory

Implements [`requirements/content-creation-factory.md`](../../requirements/content-creation-factory.md)
as a standalone **deepagents** project with a **CopilotKit** UI. TDD: red
scaffold first, then green.

**Produces:** new content — publish-ready pieces plus channel variants.

## Agent design

One orchestrator deep agent whose **sub-agents** are the requirement-doc roles.
Planning (`write_todos`), the draft workspace (virtual filesystem), and the
publish gate (HITL interrupt) come from `deepagents`.

```
build_agent() -> create_deep_agent(
    model        = <Claude model>,
    system_prompt= "Turn the brief into publish-ready, on-brand, fact-checked
                    content. Ground every claim in a source; never publish
                    without human approval.",
    tools        = [web_search, fetch_url, write_file, check_style, publish],
    subagents    = [researcher, strategist, writer, editor,
                    fact_checker, formatter],
)
```

### Sub-agents (`subagents.py`)

| Sub-agent | Role | Tools |
| --- | --- | --- |
| `researcher` | Gather + cite sources, build factual outline | `web_search`, `fetch_url` |
| `strategist` | Set angle, hook, channel structure | filesystem |
| `writer` | Draft in brand voice | `write_file` |
| `editor` | Clarity/flow, enforce style guide | `check_style` |
| `fact_checker` | Verify claims vs sources, flag unsupported | filesystem |
| `formatter` | Repurpose into channel variants + metadata | `write_file` |

### Artifact & plan

- The plan is the deep agent's **todo list** (`write_todos`).
- Sources, outline, draft, and variants live in the **virtual filesystem**.
- The deliverable is the **approved piece + channel variants**.

### Approval gates (`gates.py`)

- HITL interrupt **before `publish`** — human owns the publish boundary (FR7).
- Fact-check guard: the system prompt + `fact_checker` route unsupported claims
  back to `writer`; nothing publishes with unsupported claims (accuracy NFR).

## UI (CopilotKit)

- `useCoAgent` streams the todo list and current sub-agent (research → write →
  edit → fact-check → format) live.
- `useCoAgentStateRender` renders the draft, the sources list, and fact-check
  flags as they update.
- The `publish` interrupt renders an **approve/edit/deny** card before publish.

## Failing tests (red)

`agent/tests/`
- `test_agent.py` (RED until wired): `build_agent()` returns a deep agent with
  the six named sub-agents and expected tools.
- `test_tools.py` (RED): `web_search`/`fetch_url`/`publish`/… honor their
  signatures; stubs raise `NotImplementedError`. `researcher` output carries
  ≥1 cited source.
- `test_gates.py` (RED): the agent interrupts **before** `publish` and does not
  publish without approval.

`ui/test/`
- `agent-state.test.ts` — zod schema for `{todos, sources, draft, factcheck,
  variants}` round-trips; rejects a claim with no source.
- `hitl.test.ts` — the approval card renders on the `publish` interrupt (stub → RED).

## Green milestones

1. Assemble `build_agent()` + gate config → agent/gate tests pass with stubs.
2. Implement tools, then role prompts (`researcher` → `writer`/`editor` →
   `fact_checker` → `formatter`) → tool/behavior tests pass.
3. Wire CopilotKit to live state; connect real CMS/social/image adapters behind
   tool interfaces; keep publish human-owned.

## Integrations

CMS (WordPress/Webflow), social schedulers, Google Docs/Notion, image
generation, SEO tools — all behind tool interfaces so tests use fakes.
