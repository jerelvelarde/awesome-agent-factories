# Build Plan: Content Creation Factory

Implements [`requirements/content-creation-factory.md`](../../requirements/content-creation-factory.md)
as a standalone LangGraph project. TDD: red scaffold first, then green.

## Graph design

State graph modeling the research → draft → edit → fact-check → format loop.

### State (`state.py`)

```
brief: Brief                    # topic, goal, audience, channel, length/format
brand: BrandKit                 # voice/tone, style rules, terminology, do/don't
sources: list[Source]           # gathered + cited references
outline: Outline | None
draft: str | None
edits: str | None               # editor-revised draft
factcheck: FactCheck | None     # {flags: [...], all_supported: bool}
variants: dict[str, str]        # channel-specific repurposes
approvals: dict[str, bool]      # {"publish": bool}
iteration: int                  # fact-check loop counter
```

### Nodes (one agent role each, `nodes/`)

| Node | Role | Output keys |
| --- | --- | --- |
| `researcher` | Gather + cite sources, build factual outline | `sources`, `outline` |
| `strategist` | Set angle, hook, channel structure | `outline` (refined) |
| `writer` | Draft in brand voice | `draft` |
| `editor` | Clarity/flow, enforce style guide | `edits` |
| `fact_checker` | Verify claims vs sources, flag unsupported | `factcheck` |
| `publish_gate` | `interrupt` for human approval before publish | `approvals["publish"]` |
| `formatter` | Repurpose into channel variants + metadata | `variants` |

### Edges / routing (`graph.py`, `guardrails.py`)

```
START → researcher → strategist → writer → editor → fact_checker
fact_checker --has_flags--> writer            (loop, bounded by iteration)
fact_checker --all_supported--> publish_gate → formatter → END
```

- `publish_gate` is a hard interrupt; no publish/format output is released until
  `approvals["publish"]` is true (FR7, guardrail).
- `unsupported_claims(state)` routes back to `writer`; unsupported claims can
  never pass silently (non-functional: accuracy).
- `style_violations(state)` blocks off-brand output at the editor step.

## Failing tests (red)

`python/tests/`
- `test_state.py` — `Brief`/`BrandKit` validation; reject missing channel.
- `test_graph.py` (RED until wired):
  - graph compiles and exposes the 7 nodes;
  - `fact_checker` with flags routes back to `writer`;
  - `formatter` is unreachable until `approvals["publish"]` is true (interrupt);
  - `iteration` bound stops infinite fact-check loops.
- `test_nodes.py` (RED): each node returns its declared output key(s); stubs
  raise `NotImplementedError`. `researcher` output includes ≥1 cited `Source`.

`typescript/test/`
- `schema.test.ts` — `Brief`/`Source`/`FactCheck` zod schemas round-trip; reject
  a claim with no source.
- `client.test.ts` — CLI accepts a brief file and invokes the graph (stub → RED).

## Green milestones

1. Wire `build_graph()` + routing → structure/routing/interrupt tests pass.
2. Implement `researcher` (with web/source tools), then `writer`/`editor`, then
   `fact_checker`, `formatter` → node tests pass one by one.
3. Wire real CMS/social/image adapters behind interfaces; keep publish gated.

## Integrations

CMS (WordPress/Webflow), social schedulers, Google Docs/Notion, image
generation, SEO tools. All behind interfaces so tests use fakes.
