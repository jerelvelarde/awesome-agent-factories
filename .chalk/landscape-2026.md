# Research notes: 2026 agent-factory landscape expansion

Working notes (chalk protocol) behind the README expansion of 2026-07-02. Captures
the deep-research method, curation decisions, and prunes so the list is auditable.
Companion to [`research.md`](research.md), [`improvements.md`](improvements.md),
[`launch-plan.md`](launch-plan.md).

## Method

Six parallel research passes (one per landscape slice), each returning candidate
entries with a maintenance signal (stars + recency), license, and a best-only
verdict, plus a refresh (keep/prune/re-describe) of existing entries. Curated to a
**lean best-only** bar (protecting the sindresorhus/awesome submission): actively
maintained, documented, on-scope, no duplicate URLs, OSI-license preferred (SaaS
allowed where it's the category norm, e.g. enterprise/voice).

Result: ~43 → ~100 entries across **15 content categories** (6 new).

## New categories

- **Voice & Realtime Agents**, **Browser & Computer-Use Agents**, **Tools &
  Integrations**, **Sandboxes & Execution**, **Guardrails & Safety** — all net-new.
- **Evaluation & Testing** — split out of Observability & Ops (LangSmith and Arize
  Phoenix relocated to Eval as their headline strength; Langfuse and AgentOps kept
  in Observability).

## Notable prunes / updates

- **gpt-engineer** — PRUNED: repo archived (last push May 2025), self-described
  precursor to closed-source Lovable. Fails the not-archived bar.
- **MetaGPT** — URL updated `geekan/MetaGPT` → `FoundationAgents/MetaGPT` (moved).
- **Oracle** — renamed to Oracle AI Database Private Agent Factory (canonical URL).
- **Model Context Protocol** — governance moved to the Linux Foundation.

## Deliberate exclusions (borderline, held out to keep it lean)

- **License / scope:** GPT Pilot (FSL-1.1, not OSI), Nango (Elastic-2.0), Patronus
  AI (pivoted off OSS eval), Braintrust (closed SaaS), Toolhouse (proprietary).
- **Unmaintained:** Rebuff (archived, superseded by LLM Guard), Literal AI & Lunary
  (sunset), Ultravox (cadence slowed), Blaxel (templates only).
- **Low signal:** Inngest AgentKit, Memobase, Redis Agent Memory Server, Steel,
  W&B Weave, TruLens, Amazon Nova Act (research preview), Vellum, Stack AI.
- **Proprietary hosted-only, no OSS core:** Cursor, Devin, Bolt.new, Lovable, v0,
  Replit Agent (excluded from Agents-That-Build).
- **Directories, not lists:** mcp.so, Smithery, PulseMCP (kept Official MCP Registry
  + awesome-mcp-servers instead).

## Dedupe decisions

- **Zep / Graphiti** — listed once as Zep (Graphiti is Zep's OSS engine).
- **ACP** — folded into A2A (the agent-to-agent lane consolidated onto A2A).
- Phoenix / LangSmith counted once each under Evaluation (not double-listed in
  Observability). Portkey placed in Observability on its metrics strength.

## Watch-items before the upstream submission

- AutoGen (maintenance mode) and Semantic Kernel (superseded by MS Agent Framework)
  still pass the bar but a strict reviewer may question longevity.
- Daytona's public OSS repo froze (Jun 2026) though the hosted product is active.
- Refresh exact star counts at PR time (reviewers sometimes check).
- ✅ Reference-factory links repointed to the canonical upstream
  `jerelvelarde/awesome-agent-factories` (2026-07-02); the `docs/landscape.md`
  differentiator uses repo-relative links, so it resolves in either repo. Note:
  these blob URLs 404 until PR #3 merges into upstream `main`, then resolve.

## Differentiator

`docs/landscape.md` — a "pick by layer" decision guide + a verified 9-framework
code-first harness comparison matrix (kept out of the linted README so the list
stays lean; awesome-lint only lints README.md).
