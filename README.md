# Awesome Agent Factories [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of frameworks, platforms, and tools for **building, generating, and orchestrating AI agents** — the "factories" that manufacture agents.

An *agent factory* is a **group of agents, built on harnesses, that produces one type of artifact** — software, content, proposals, and so on. A *harness* is the base model + system instructions + tools that each agent runs on; an *agent* is a harness assigned a role; a *factory* orchestrates a group of them to manufacture its output. This list collects the best tools across that stack — harnesses and frameworks, visual builders, enterprise platforms, agents that build agents, plus the UIs, protocols, memory, tools, sandboxes, evaluation, observability, and guardrails around them — and links to worked reference factories built in this repo.

Only actively maintained, documented, and genuinely recommendable projects are included. New here? See the [agent-stack decision guide and framework comparison](docs/landscape.md).

## Contents

- [Code-First Frameworks](#code-first-frameworks)
- [Visual & Low-Code Builders](#visual--low-code-builders)
- [Enterprise Agent Platforms](#enterprise-agent-platforms)
- [Agents That Build Agents](#agents-that-build-agents)
- [Agent UIs](#agent-uis)
- [Voice & Realtime Agents](#voice--realtime-agents)
- [Browser & Computer-Use Agents](#browser--computer-use-agents)
- [Memory & State](#memory--state)
- [Tools & Integrations](#tools--integrations)
- [Protocols & Interoperability](#protocols--interoperability)
- [Sandboxes & Execution](#sandboxes--execution)
- [Evaluation & Testing](#evaluation--testing)
- [Observability & Ops](#observability--ops)
- [Guardrails & Safety](#guardrails--safety)
- [Learning Resources](#learning-resources)
- [Reference Factories](#reference-factories)

## Code-First Frameworks

Libraries for defining agents in code, with control over tools, state, and multi-agent orchestration.

- [Agno](https://github.com/agno-agi/agno) - Fast multi-agent framework with persistent memory and multimodal input; ships AgentOS, a pre-built server with sessions, streaming, and RBAC.
- [Atomic Agents](https://github.com/BrainBlend-AI/atomic-agents) - Lightweight, modular Python framework for building agents from reusable, composable components on Pydantic and Instructor.
- [AutoGen](https://github.com/microsoft/autogen) - Microsoft framework for conversational multi-agent systems, including group decision-making and debate patterns, with an optional no-code Studio.
- [Cloudflare Agents](https://github.com/cloudflare/agents) - TypeScript SDK for persistent, stateful agents on Cloudflare Workers with real-time communication, scheduling, and MCP support.
- [CrewAI](https://github.com/crewAIInc/crewAI) - Role-based orchestration for modeling teams of agents with the least boilerplate; intuitive for business workflow automation.
- [deepagents](https://github.com/langchain-ai/deepagents) - Batteries-included agent harness on LangGraph with built-in planning, a virtual filesystem, sub-agent context isolation, and human-in-the-loop interrupts.
- [Google ADK](https://github.com/google/adk-python) - Google's official Agent Development Kit with native Gemini and Vertex AI integration.
- [Haystack](https://github.com/deepset-ai/haystack) - Composable pipelines and agents over search and LLMs, from deepset.
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based framework for stateful, durable, production-grade agent workflows with fine-grained control over branching and error handling.
- [LlamaIndex](https://github.com/run-llama/llama_index) - Data-centric framework whose AgentWorkflow combines agents with first-class RAG over your data.
- [Mastra](https://github.com/mastra-ai/mastra) - TypeScript-first agent framework (from the team behind Gatsby) for the JavaScript ecosystem.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Lightweight Python framework for multi-agent workflows with handoffs, guardrails, and built-in tracing.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Type-safe agent framework from the Pydantic team; gives validated, structured outputs without writing the validators yourself.
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Microsoft's enterprise orchestration SDK for C#, Python, and Java with planners and plugins.
- [smolagents](https://github.com/huggingface/smolagents) - Hugging Face's minimal library for code-acting agents; the fastest setup for a single-agent loop.
- [Strands Agents](https://github.com/strands-agents/sdk-python) - AWS's model-agnostic SDK for building and orchestrating agents in a few lines of Python or TypeScript, with built-in tools and observability.

## Visual & Low-Code Builders

Drag-and-drop and low-code tools for assembling agents without writing everything by hand.

- [Botpress](https://botpress.com) - Developer-friendly visual editor for building multi-channel conversational agents with drag-and-drop flows and 50+ integrations.
- [Dify](https://github.com/langgenius/dify) - LLMOps platform combining a visual agent/workflow builder with prompt management and observability.
- [Flowise](https://github.com/FlowiseAI/Flowise) - Visual builder with modular blocks for multi-agent systems; supports 100+ LLMs, embeddings, and vector databases, deployable on-prem or in the cloud.
- [Gumloop](https://www.gumloop.com) - No-code drag-and-drop canvas for building AI automations and agents with a deep integration library.
- [Langflow](https://github.com/langflow-ai/langflow) - Low-code visual editor for agentic and RAG applications with a large component library.
- [Lindy](https://www.lindy.ai) - No-code builder for autonomous AI assistants that trigger on events and act across email, meetings, and CRMs.
- [n8n](https://github.com/n8n-io/n8n) - Source-available workflow automation with native AI agent nodes for wiring agents into hundreds of integrations.
- [Relevance AI](https://relevanceai.com) - Low-code platform for building AI agents and multi-agent teams with a visual builder and tool ecosystem.
- [Sim Studio](https://github.com/simstudioai/sim) - Open-source, Figma-like canvas for visually building and deploying agentic workflows with a strong self-host story.
- [Voiceflow](https://www.voiceflow.com) - Collaborative platform for designing and shipping conversational and voice agents.

## Enterprise Agent Platforms

Managed platforms for building and running agents at scale with governance, security, and data integration.

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) - AWS runtime and tooling for deploying and operating agents securely at scale.
- [Databricks Agent Bricks](https://www.databricks.com/product/artificial-intelligence/agent-bricks) - Governed platform for building auto-optimized agents with supervisor orchestration and Unity Catalog governance on your own data.
- [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate) - Enterprise control plane to build, deploy, govern, and monitor agents across frameworks under unified policy and audit.
- [Microsoft Foundry](https://ai.azure.com) - Framework-agnostic runtime; agents built with Agent Framework, LangGraph, or other SDKs deploy without rewrites.
- [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) - Open toolkit for connecting, profiling, and optimizing teams of agents across frameworks.
- [Oracle Private Agent Factory](https://www.oracle.com/database/agent-factory/) - No-code platform to build and run trusted agents over private enterprise data in Oracle AI Database.
- [Salesforce Agentforce](https://www.salesforce.com/agentforce/) - Platform for building autonomous agents embedded across the Salesforce ecosystem.
- [ServiceNow AI Agent Studio](https://www.servicenow.com/products/ai-agents.html) - Governed studio for building and orchestrating agents natively across ITSM, CSM, HR, and SecOps workflows.
- [Sierra](https://sierra.ai) - Enterprise platform for deploying action-taking conversational agents across chat, voice, and messaging at scale.
- [UiPath Agentic Automation](https://www.uipath.com/platform/agentic-automation) - Platform combining AI agents, robots, and people under orchestration and governance for end-to-end process automation.
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) - Google Cloud's managed stack for building, deploying, and scaling agents on Vertex AI.

## Agents That Build Agents

Autonomous systems that generate other agents, code, or whole software projects — the most literal factories.

- [Aider](https://github.com/Aider-AI/aider) - AI pair-programming CLI that edits code across your repo, auto-commits with Git, and works with almost any model.
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Platform for creating, deploying, and managing continuous, goal-driven autonomous agents.
- [ChatDev](https://github.com/OpenBMB/ChatDev) - Virtual software company where agents in different roles collaborate to develop software.
- [Cline](https://github.com/cline/cline) - Autonomous coding agent (IDE extension, CLI, and SDK) that plans, edits, and executes across a codebase with human-in-the-loop control.
- [Goose](https://github.com/block/goose) - Block's open-source, extensible agent that installs, executes, edits, and tests code with any LLM via a pluggable extension system.
- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) - Multi-agent framework that simulates a software company, assigning roles to turn one prompt into a project.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) - Platform for autonomous software-engineering agents that write code, run commands, and browse the web.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) - Princeton's agent that autonomously reads a GitHub issue and produces a fix with any LLM; a strong SWE-bench performer.

## Agent UIs

Frontend frameworks for rendering agent state, streaming, and human-in-the-loop approvals.

- [assistant-ui](https://github.com/assistant-ui/assistant-ui) - React primitives for AI chat with streaming, tool-call UIs, generative UI, and human-in-the-loop.
- [Chainlit](https://github.com/Chainlit/chainlit) - Python framework for building agent UIs fast, with step and tool-call visualization, streaming, and human feedback.
- [CopilotKit](https://github.com/CopilotKit/CopilotKit) - React frontend stack for agents (maker of the AG-UI protocol) with first-class LangGraph and deep-agents support for shared state, generative UI, and human-in-the-loop.
- [LibreChat](https://github.com/danny-avila/LibreChat) - Self-hostable, multi-model chat app with first-class agents, MCP, tools, and artifacts.
- [Vercel AI SDK](https://ai-sdk.dev) - TypeScript toolkit for streaming, tool calls, and generative UI, with AI Elements components for rendering agent state.

## Voice & Realtime Agents

Frameworks and platforms for building voice and realtime conversational agents.

- [ElevenLabs Agents](https://elevenlabs.io/conversational-ai) - Multimodal agent platform pairing best-in-class TTS/STT with turn-taking, RAG, and tools across phone, chat, and web.
- [LiveKit Agents](https://github.com/livekit/agents) - Production-grade Python and Node framework for server-side realtime voice agents over WebRTC.
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) - Speech-to-speech API with tool-calling, image input, and SIP phone calling for low-latency voice agents.
- [Pipecat](https://github.com/pipecat-ai/pipecat) - Vendor-neutral Python framework for real-time voice and multimodal pipelines, swapping any STT, LLM, or TTS.
- [Vapi](https://vapi.ai) - Full-stack developer platform bundling STT, LLM, TTS, telephony, and orchestration for phone and web voice agents.

## Browser & Computer-Use Agents

Frameworks and tools for agents that drive a browser or a computer.

- [Browser Use](https://github.com/browser-use/browser-use) - Popular open-source Python framework for driving a browser from natural-language agent instructions.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) - Microsoft's MCP server giving any LLM structured, accessibility-tree browser control without screenshots.
- [Skyvern](https://github.com/Skyvern-AI/skyvern) - LLM-plus-computer-vision browser automation that survives layout changes without brittle selectors.
- [Stagehand](https://github.com/browserbase/stagehand) - Browserbase's TypeScript SDK blending natural-language actions with code for reliable production browser agents.

## Memory & State

Building blocks that give agents long-term memory and persistence.

- [Cognee](https://github.com/topoteretes/cognee) - Open-source AI memory that builds self-hostable knowledge graphs to give agents persistent long-term memory.
- [Letta](https://github.com/letta-ai/letta) - Framework (formerly MemGPT) for stateful agents with long-term memory and transparent reasoning.
- [Mem0](https://github.com/mem0ai/mem0) - Memory layer that lets agents remember user preferences and facts across sessions.
- [Supermemory](https://github.com/supermemoryai/supermemory) - Fast, scalable, self-hostable memory and context-engine API for agents.
- [Zep](https://github.com/getzep/zep) - Memory server providing temporal knowledge graphs and recall for agents.

## Tools & Integrations

Platforms that give agents authenticated tools and actions across other apps.

- [Apify MCP Server](https://github.com/apify/apify-mcp-server) - Exposes Apify's thousands of web-scraping and automation Actors to agents over MCP for real-world web data and actions.
- [Arcade.dev](https://www.arcade.dev) - Authenticated tool-calling runtime giving agents OAuth-secured tools across Google, Slack, Microsoft, and Salesforce.
- [Composio](https://github.com/ComposioHQ/composio) - Tool and integration platform giving agents 250+ authenticated app connectors with tool search, auth, and a sandboxed workbench.
- [Official MCP Registry](https://github.com/modelcontextprotocol/registry) - Canonical, community-driven registry service for discovering Model Context Protocol servers.

## Protocols & Interoperability

Standards that let agents talk to tools and to each other.

- [Agent2Agent (A2A)](https://github.com/a2aproject/A2A) - Open protocol for interoperability and communication between agents from different vendors.
- [AG-UI](https://github.com/ag-ui-protocol/ag-ui) - Open protocol standardizing the interaction layer between agents and user-facing applications.
- [Model Context Protocol](https://modelcontextprotocol.io) - Open standard (now under the Linux Foundation) for connecting agents to tools and data sources through a common interface.
- [x402](https://github.com/x402-foundation/x402) - HTTP-native, chain-agnostic payments protocol (reviving the 402 status code) for agents and APIs to transact autonomously.

## Sandboxes & Execution

Secure runtimes for executing agent- and LLM-generated code.

- [Daytona](https://www.daytona.io) - Elastic infrastructure for running AI-generated code in isolated sandboxes with sub-100ms startup and filesystem, process, and Git APIs.
- [E2B](https://e2b.dev) - Open-source secure cloud runtime that executes AI-generated code in Firecracker microVM sandboxes via Python and JS SDKs.
- [Microsandbox](https://github.com/microsandbox/microsandbox) - Self-hostable, local-first microVM runtime for safely running untrusted agent code with hardware-level isolation and an MCP server.
- [Modal Sandboxes](https://modal.com/docs/guide/sandbox) - First-class primitive for executing untrusted agent code in gVisor-isolated ephemeral containers with filesystem snapshots.

## Evaluation & Testing

Frameworks for evaluating and regression-testing agents and their trajectories.

- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Open-source, OpenTelemetry-native evaluation and tracing for LLM and agent pipelines, with LLM-as-judge and RAG scoring.
- [DeepEval](https://github.com/confident-ai/deepeval) - Pytest-style evaluation framework for LLM and agent apps with 14+ metrics like faithfulness, hallucination, and G-Eval.
- [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) - The UK AI Safety Institute's rigorous framework for LLM and agentic evaluations with datasets, solvers, tools, and model-graded scorers.
- [LangSmith](https://www.langchain.com/langsmith) - Tracing, dataset-driven evaluation, and LLM-as-judge scoring for LLM and agent apps, deepest on LangGraph.
- [OpenAI Evals](https://github.com/openai/evals) - Framework and open registry of benchmarks for evaluating LLMs and LLM systems.
- [promptfoo](https://github.com/promptfoo/promptfoo) - Declarative CLI and CI framework for testing prompts, agents, and RAG with side-by-side comparison and red-teaming.
- [Ragas](https://github.com/explodinggradients/ragas) - Toolkit for evaluating and optimizing RAG and agent pipelines with reference-free metrics and synthetic test-set generation.

## Observability & Ops

Tracing, monitoring, and cost control for agents in production.

- [AgentOps](https://github.com/AgentOps-AI/agentops) - SDK for tracking agent runs, costs, latency, and failures across popular frameworks.
- [Helicone](https://github.com/Helicone/helicone) - One-line-integration LLM observability with logging, sessions, and cost and latency tracking, plus a bundled open-source gateway.
- [Langfuse](https://github.com/langfuse/langfuse) - Open-source observability and analytics for LLM agents with tracing, evals, and prompt management.
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - OpenTelemetry-native instrumentation for LLM and agent apps that exports traces to Datadog, Honeycomb, and any OTel backend.
- [Portkey Gateway](https://github.com/portkey-ai/gateway) - Open-source AI gateway routing to 1,600+ models with built-in observability metrics and guardrails.

## Guardrails & Safety

Input/output validation, prompt-injection defense, and PII handling for agents.

- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - Python framework that runs composable input/output validators from a community hub to catch PII, hallucinations, and format violations.
- [LLM Guard](https://github.com/protectai/llm-guard) - Security toolkit that scans, redacts, and sanitizes LLM inputs and outputs for prompt injection, toxicity, PII, and secrets.
- [Microsoft Presidio](https://github.com/microsoft/presidio) - De facto open-source standard for detecting, redacting, and anonymizing PII and PHI before it reaches logs or LLM context.
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - NVIDIA's toolkit for adding programmable topical, safety, and jailbreak rails to LLM and agent apps via a declarative config language.
- [PurpleLlama](https://github.com/meta-llama/PurpleLlama) - Meta's umbrella of open safeguard models (Llama Guard, Prompt Guard, Code Shield) for content moderation and prompt-injection defense.

## Learning Resources

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) - Widely adopted engineering principles for building reliable, production-grade LLM agents.
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - OpenAI's concise guide to agent design, orchestration, guardrails, and multi-agent patterns.
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic's guide to agent patterns, when to use them, and how to keep them simple.
- [Chip Huyen — Agents](https://huyenchip.com/2025/01/07/agents.html) - Deep, vendor-neutral essay on agent capabilities, tool selection, planning, and failure modes.
- [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) - Free, hands-on course building agents with smolagents, LangGraph, and LlamaIndex, with certification.
- [OpenAI Cookbook — Agents](https://cookbook.openai.com/topic/agents) - Worked examples and recipes for building agents with the OpenAI platform.
- [The AI Agent Factory](https://agentfactory.panaversity.org/) - Open course on the agent-factory paradigm and building production agents.

## Reference Factories

Worked examples built in this repo, each a *group of agents on harnesses that produces one type of artifact*. The reference stack is deepagents for the harness and orchestration and CopilotKit for the UI. Each ships a requirement doc and a build plan.

- [Software Development Factory](https://github.com/breadoncee/awesome-agent-factories/blob/main/factories/software-development-factory/BUILD_PLAN.md) - Blueprint for a factory that produces new software: a reviewed, tested draft pull request.
- [Content Creation Factory](https://github.com/breadoncee/awesome-agent-factories/blob/main/factories/content-creation-factory/BUILD_PLAN.md) - Blueprint for a factory that produces new content: publish-ready pieces plus channel variants.
- [Sales Proposal Factory](https://github.com/breadoncee/awesome-agent-factories/blob/main/factories/sales-proposal-factory/BUILD_PLAN.md) - Blueprint for a factory that produces new proposals: tailored, priced, and compliance-checked.

## Related Lists

- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents) - Broad directory of AI agents and frameworks maintained by e2b.
- [Awesome AI Agents 2026](https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents-2026) - Large 2026-focused collection of agents, frameworks, and comparisons.
- [Awesome Agents](https://github.com/kyrolabs/awesome-agents) - Curated open-source tools and products for building AI agents.
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - Curated skills, agents, hooks, slash-commands, and plugins for Claude Code.
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps) - Curated LLM and agent applications with source code.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) - The canonical, massive catalog of Model Context Protocol servers for agent tooling.

## Contributing

Contributions are welcome! Please read the [contribution guidelines](contributing.md) first. In short: suggest only projects you would personally recommend, keep them maintained and documented, and match the existing entry format.
