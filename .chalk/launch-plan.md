# Launch plan: open-sourcing awesome-agent-factories

Working note (chalk protocol). Companion to [`research.md`](research.md) and
[`improvements.md`](improvements.md). Date: 2026-06-30.

## Decisions (locked)

- **The awesome list is the product.** The reference-factory **blueprints** are a
  differentiator, not the headline.
- **Blueprints-only at launch.** Factory implementations stay private; the repo
  ships requirements + build plans for all three factories.
- **Primary goal:** acceptance into [`sindresorhus/awesome`](https://github.com/sindresorhus/awesome).
  Everything below optimizes for that bar.

---

## Part 1 — How to improve the factories (blueprint level)

Since we ship blueprints (not code), "improving the factories" = making each
blueprint a **credible, best-practice, buildable spec** that a reader could
implement and that signals authority. Pull the durable, architecture-level
guidance from [`improvements.md`](improvements.md) into the BUILD_PLANs/
requirements so the blueprints *embody* current best practice:

1. **Fix the design details the research surfaced** so the blueprints are
   technically correct: HITL via deepagents' declarative **`interrupt_on=` + a
   checkpointer** (not a hand-rolled gate); subagent specs keyed by
   **`system_prompt`**; durable persistence (**Postgres checkpointer + `BaseStore`**);
   and be honest that dynamic sub-agents are mostly built-in (`task` tool /
   `AsyncSubAgent`) with only spec-persistence being additive.
2. **Bake in the quality layer** every serious factory needs, as blueprint
   sections: per-factory **eval harness + ~20-case golden dataset**, **OTel/
   LangSmith tracing**, **deterministic artifact validation + run-cost ceilings**,
   and a **verifier/critic before each human gate**.
3. **Lead with the domain-specific hardening** — this is what makes the
   blueprints stand out from generic "build an agent" content:
   - SDF → defenses against **false-green tests / reward hacking** (sandboxed,
     agent-isolated, protected test files).
   - Content → **citation verification** + plagiarism/AI-disclosure fields.
   - Sales → **"AI drafts, humans decide"**: non-bypassable pricing/legal gate,
     pricing validated against an approved catalog.
4. **Keep the three blueprints uniform** (same section shape, depth, and stack
   framing) so the set reads as one coherent body of work.

> Scope note: this is polish that strengthens the *differentiator*. It is **not**
> on the critical path to awesome acceptance (Part 2 is). Do it in parallel or
> just after submission.

---

## Part 2 — Launch readiness (the critical path)

### 2a. `awesome-lint` findings — must be green before submitting

`npx awesome-lint` currently reports **15 errors**. Grouped with fixes:

**GitHub repo settings (not file changes):**
- Set a **repository description**.
- Add GitHub **topics `awesome` and `awesome-list`**.

**README fixes (in-repo):**
- **Remove the `## License` section** — awesome forbids a license *section*; the
  `license` file (already CC0 ✅) is what's required.
- **Dedupe links** — awesome forbids the same URL twice. Offenders:
  `#reference-factories` (intro + ToC), and `deepagents` / `CopilotKit` (linked
  in their framework/UI entries *and* again in the Reference Factories intro,
  line 112). Fix: link each URL once — make the second mentions plain text.
- **Fix ToC ↔ heading alignment** — ToC drifts against the `License`/trailing
  sections. Regenerate/align so ToC matches headings exactly (drop
  Contributing/License from the ToC per convention).
- **Fix entry casing** (line 33) — a description must start with valid casing.
- **Reference Factories local links (lines 114–116) are "invalid list item
  link URL"** — awesome list items must be real `http(s)` URLs, not in-repo
  relative paths. **This is the one real tension** between "blueprints in the
  repo" and lint compliance. Options (pick one):
  1. Point each entry at its **full GitHub blob URL**
     (`https://github.com/<owner>/awesome-agent-factories/blob/main/factories/...`).
     Keeps the section, passes lint. **Recommended.**
  2. Move Reference Factories into a **non-list prose block** (not `- [..](..)`
     bullets) so the list-item rule doesn't apply.
  3. Drop the section from the linted README and describe the factories in a
     separate `factories/README.md`.

Re-run `npx awesome-lint` until **0 errors**.

### 2b. Pre-submission repo hygiene

- ✅ Awesome badge, scope blockquote, Title-Case heading, CC0 `license`,
  `contributing.md`, lowercase repo slug, `main` default branch, `.gitignore`
  (just added).
- ⬜ Add a **`code-of-conduct.md`** (Contributor Covenant) — required by the
  awesome contributing guidelines.
- ⬜ Confirm **every external link resolves** and each project is **actively
  maintained** (drop archived/deprecated; the manifesto bar). Spot-check the
  enterprise-platform and observability entries especially.
- ⬜ Ensure **every entry description ends with a period** and says *why* it's
  worth the reader's time.
- ⬜ Note: the removed SDF implementation remains in git history (by choice) —
  fine for a blueprint-only public repo; nothing further needed.

### 2c. sindresorhus/awesome submission requirements (the gate)

From [awesome.md](https://github.com/sindresorhus/awesome/blob/main/awesome.md) /
[create-list.md](https://github.com/sindresorhus/awesome/blob/main/create-list.md):

- ⬜ **The list must be ≥30 days old** before you submit the upstream PR (they
  enforce this). This sets the earliest submission date — plan around it.
- ⬜ Repo passes `awesome-lint` with **0 errors** (Part 2a).
- ⬜ Description, `awesome`/`awesome-list` topics set (Part 2a).
- ⬜ **One list per PR**; PR title exactly **`Add Awesome Agent Factories`**.
- ⬜ Add the entry to the **correct category** of the main awesome README, in the
  right alphabetical position, format `- [Agent Factories](url) - desc.`
- ⬜ Complete the PR's **requirements checklist honestly** (it's strict — partial
  compliance gets closed).
- ⬜ **Scope must be distinct** from existing lists (e.g. `e2b-dev/awesome-ai-agents`,
  `kyrolabs/awesome-agents`). Our angle — *factories that manufacture agents*
  (frameworks/platforms/agents-that-build-agents) **+ worked reference
  blueprints** — is genuinely differentiated; state that clearly in the PR.
- ⬜ Enough high-quality, non-duplicate entries (we have ~10 categories — good).

---

## Part 3 — Launch sequence

**Phase 0 — Make it lint-clean & public (now):**
1. Apply Part 2a README fixes; add `code-of-conduct.md`.
2. Set GitHub description + topics; verify repo is public.
3. `npx awesome-lint` → 0 errors. Tag a `v1.0` once green.

**Phase 1 — Strengthen the differentiator (parallel, ~weeks):**
4. Apply Part 1 blueprint upgrades (correctness + quality + domain hardening).
5. Verify all external links; prune anything unmaintained.

**Phase 2 — Seed credibility (during the 30-day wait):**
6. Light promotion to start real usage/stars (HN "Show HN", relevant subreddits,
   LangChain/CopilotKit communities, X/LinkedIn). Genuine traction helps the
   reviewer take it seriously and surfaces dead links/bad entries early.
7. Triage early issues/PRs to show the list is maintained.

**Phase 3 — Upstream submission (day ≥30, lint green):**
8. Open the `sindresorhus/awesome` PR per Part 2c; complete the checklist;
   respond fast to reviewer feedback (they close stale/non-compliant PRs).

**Phase 4 — Post-acceptance maintenance:**
9. Keep entries current (the list lives or dies on freshness); a quarterly
   review cadence; clear `contributing.md` so external PRs are easy to accept.

---

## Risks / watch-items

- **Local reference-factory links vs. lint** — resolved by Part 2a option 1
  (full GitHub URLs); don't let the differentiator break the gate.
- **30-day age rule** is the long pole — start the clock by making the repo
  public and lint-clean *now*.
- **Maintenance signal** — awesome reviewers reject lists that look abandoned;
  Phase 2 traction + Phase 4 cadence matter.
- **Don't over-invest in blueprints pre-submission** — Part 2 is the gate; Part 1
  is differentiation and can trail.
