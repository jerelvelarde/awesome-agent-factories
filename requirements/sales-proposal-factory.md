# Requirements: Sales Proposal Factory

## 1. Overview

The Sales Proposal Factory is an agent factory that turns a prospect's context
and discovery notes into a tailored, accurate, and on-brand sales proposal or
RFP response. A team of agents researches the account, maps needs to offerings,
prices the deal, drafts the document, and reviews it for accuracy and
compliance — so reps produce winning proposals in minutes instead of days.

### Concept & reference stack

This factory is a **group of agents built on harnesses**. A *harness* is a base
model + system instructions + tools; an *agent* is a harness assigned a role;
the *factory* is the orchestrated group of agents that produces one type of
artifact — here, **new proposals** (tailored, priced, compliance-checked). The
reference implementation uses [`deepagents`](https://github.com/langchain-ai/deepagents)
as the harness and orchestration (built-in planning, a virtual filesystem for
the proposal workspace, sub-agent context isolation, and human-in-the-loop
interrupts) and [CopilotKit](https://github.com/CopilotKit/CopilotKit) for the
UI. See [`factories/sales-proposal-factory/BUILD_PLAN.md`](../factories/sales-proposal-factory/BUILD_PLAN.md).

## 2. Goals & Non-Goals

### Goals
- Generate a tailored proposal from CRM data, discovery notes, and a product/pricing catalog.
- Map the prospect's stated needs to specific offerings and outcomes.
- Produce accurate pricing within approved guardrails.
- Enforce a research → solution → price → draft → review loop with human sign-off.

### Non-Goals
- Sending proposals or committing pricing without human approval.
- Setting list pricing or discount policy (human/finance-owned).
- Negotiating contract terms autonomously.

## 3. Users & Personas

| Persona | Need |
| --- | --- |
| Account executive | Produce tailored proposals fast, accurately. |
| Sales engineer | Map technical needs to solution scope. |
| Sales ops / RevOps | Enforce pricing, approval, and brand standards at scale. |

## 4. Inputs

- Prospect context: company, industry, size, CRM record, discovery notes.
- Stated requirements / pain points (call notes, RFP questions).
- Product and pricing catalog with packaging and discount rules.
- Proposal templates, brand kit, and legal/approved language.
- Deal parameters: term, seats, region, approval thresholds.

## 5. Agent Architecture

A supervised proposal pipeline, realized as a single **deepagents** deep agent
whose **sub-agents** are the roles below (each a harness: model + system prompt
+ tools, with context isolation):

1. **Account Researcher** — enriches and summarizes the prospect, industry
   context, and likely priorities from CRM and notes.
2. **Solution Architect** — maps stated needs to specific products, scope, and
   measurable outcomes; flags gaps or upsell fit.
3. **Pricing Agent** — assembles line items and totals from the catalog within
   discount guardrails; routes out-of-policy pricing for approval.
4. **Proposal Writer** — drafts the document from a template: executive
   summary, problem, solution, scope, pricing, timeline, ROI, next steps.
5. **Reviewer/Compliance** — checks factual accuracy, legal/approved language,
   pricing validity, and brand consistency.
6. **Personalizer/Formatter** — applies prospect-specific tailoring and outputs
   the final formatted document.

The **orchestrator deep agent** enforces the loop, plans via its built-in todo
list, applies approval gates, and escalates to the rep/manager — implemented as
human-in-the-loop interrupts (before accepting out-of-policy pricing and before
sending) that CopilotKit surfaces as approve/deny steps in the UI.

## 6. Outputs / Deliverables

- A formatted, prospect-specific proposal (PDF/DOCX/slides).
- An itemized pricing summary within approved guardrails.
- An executive summary and ROI/value rationale.
- A change log of what was tailored and any items needing approval.

## 7. Functional Requirements

- FR1: Pull prospect context from CRM and ingest discovery notes.
- FR2: Map each stated need to a specific offering and stated outcome.
- FR3: Generate pricing only from the approved catalog and discount rules.
- FR4: Flag any out-of-policy pricing or scope for human approval.
- FR5: Draft from an approved template with required sections.
- FR6: Use only legal-approved boilerplate and claims.
- FR7: Require human approval before the proposal is sent or shared externally.
- FR8: Write outcomes back to CRM (proposal sent, value, stage).
- FR9: Create and manage its own sub-agents at runtime (like Claude Code
  subagents) — author, list, update, and retire specialized roles on top of the
  seed roles, persisting them across runs.

## 8. Non-Functional Requirements

- Accuracy: no invented capabilities, references, pricing, or commitments.
- Compliance: legal/approved language only; honor regional and contractual rules.
- Security: protect prospect data; respect access controls and retention.
- Consistency: brand voice and formatting stable across proposals.

## 9. Integrations

CRM (Salesforce/HubSpot), CPQ/pricing systems, document generation
(PDF/DOCX/Slides), e-signature, content/asset libraries, and approval
workflows.

## 10. Guardrails & Quality

- Hard gate: human approval before sending; pricing approval for out-of-policy deals.
- No capability or ROI claims beyond the approved catalog and case studies.
- Pricing math validated against the catalog; totals reconciled.
- Compliance review on legal terms and regulated-industry language.

## 11. Success Metrics

- Time from discovery to approved proposal.
- Proposal win rate and average deal size.
- % of proposals requiring pricing/compliance rework.
- Rep adoption and proposals generated per period.

## 12. Open Questions

- Source of truth for pricing and discount authority levels.
- Depth of CRM write-back and which fields.
- Handling of multi-product / multi-year / custom-scope deals.
