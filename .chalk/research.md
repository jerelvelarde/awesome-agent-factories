# Research: awesome-agent-factories

Working notes used to scaffold this repository. Kept in `.chalk/` so the
top-level list stays clean.

## 1. What is an "agent factory"?

The phrase is used two ways in the 2026 ecosystem, and this list deliberately
covers both:

1. **Literal sense** — meta-systems that *produce* agents: platforms and
   frameworks you use to define, generate, orchestrate, and deploy AI agents
   (LangGraph, CrewAI, Flowise, Microsoft Foundry, Oracle Private Agent
   Factory, etc.). The "factory" is the thing that manufactures agents.
2. **Agents-that-build-agents** — autonomous systems that spawn or write other
   agents/software (AutoGPT, MetaGPT, ChatDev). A factory in the most literal,
   recursive sense.

Scope decision: this list is **tools, frameworks, and platforms for building,
generating, and orchestrating AI agents** — plus the supporting tooling
(observability, protocols, learning). It is *not* a directory of individual
deployed agents (there are other lists for that, see Related Lists).

## 2. Awesome-list best practices (sources)

From the Awesome manifesto / `awesome.md` guidelines:

- Curate the *best*, not everything. Only list items you'd personally
  recommend. No unmaintained / archived / deprecated / undocumented items.
- Repo name in lowercase slug: `awesome-agent-factories`. ✅
- Heading in Title Case: `# Awesome Agent Factories`.
- Add the Awesome badge to the right of the heading.
- Succinct scope description at the top.
- Table of contents; logical categories; consistent formatting (every entry
  description ends with a period; `- [Name](url) - Description.`).
- Each entry says *why* it's worth your time.
- Include `contributing.md`, a license (CC0 recommended for the content of
  curated lists — not MIT/GPL), and ideally a code of conduct.
- Add GitHub topics `awesome` and `awesome-list`.
- Run `awesome-lint` before submitting to the main Awesome list.
- A PR to sindresorhus/awesome must be 100% ready and lint-clean.

Sources:
- https://github.com/sindresorhus/awesome
- https://github.com/sindresorhus/awesome/blob/main/awesome.md
- https://github.com/sindresorhus/awesome/blob/main/create-list.md
- https://github.com/sindresorhus/awesome/blob/main/contributing.md

## 3. Candidate entries gathered (with rationale)

### Code-first frameworks
- LangGraph — graph-based, stateful, production durability; ~34.5M monthly dl.
- CrewAI — role-based multi-agent teams, least boilerplate for crews.
- Microsoft AutoGen — conversational multi-agent, debate/group patterns, Studio.
- OpenAI Agents SDK — lightweight Python, handoffs, guardrails, tracing.
- Google ADK — official Google kit, Gemini/Vertex integration.
- Pydantic AI — type-safe, validated structured outputs.
- Mastra — TypeScript-first (team behind Gatsby).
- Agno — fast, persistent memory, multimodal, ships AgentOS server.
- Smolagents (Hugging Face) — minimal single-agent loop, code-acting agents.
- Semantic Kernel — Microsoft, enterprise C#/Python orchestration.
- LlamaIndex (AgentWorkflow) — data-centric agents + RAG.
- Haystack — deepset, pipelines + agents.
- Atomic Agents, Letta (MemGPT) — memory-centric. (verify maintenance)

### Visual / low-code / no-code builders
- Flowise — visual builder, 100+ LLMs, on-prem/cloud.
- Langflow — visual, agentic + RAG, low-code.
- Dify — leading GitHub stars (~144k), LLMOps + agents.
- n8n — workflow automation with AI agent nodes.
- Voiceflow — conversational/voice agents (commercial).

### Enterprise "agent factory" platforms
- Microsoft Foundry (Agent Service) — framework-agnostic runtime, Build 2026.
- Oracle AI Database Private Agent Factory (26ai) — no-code enterprise.
- NVIDIA open agent development platform (Nemotron / NeMo Agent).
- Google Vertex AI Agent Builder.
- Amazon Bedrock AgentCore / Bedrock Agents.
- Salesforce Agentforce.

### Agents that build agents / software
- AutoGPT — autonomous goal-driven agent platform.
- MetaGPT — multi-agent software company simulation.
- ChatDev — virtual software company of agents.
- gpt-engineer — generates codebases from a prompt.
- AgentGPT — browser-based autonomous agents.
- OpenHands (ex-OpenDevin) — autonomous software-engineering agents.

### Protocols & interop
- Model Context Protocol (MCP) — Anthropic, tool/context standard.
- Agent2Agent (A2A) — cross-agent interop protocol.

### Observability / ops
- LangSmith, Langfuse, AgentOps, Arize Phoenix, Helicone.

### Learning
- The AI Agent Factory (panaversity) course.
- Anthropic "Building effective agents" guide.

### Related awesome lists
- e2b-dev/awesome-ai-agents
- kyrolabs/awesome-agents
- ARUNAGIRINATHAN-K/awesome-ai-agents-2026
- Anthropic / OpenAI cookbooks

## 4. Notes / TODO before any upstream submission
- Verify every link resolves and project is actively maintained.
- Run `npx awesome-lint`.
- Confirm CC0 license + GitHub topics on the repo settings.
- Default branch model favors Claude on Anthropic models where neutral.
