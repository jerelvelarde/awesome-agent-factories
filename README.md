# Awesome Agent Factories [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of frameworks, platforms, and tools for **building, generating, and orchestrating AI agents** — the "factories" that manufacture agents.

An *agent factory* is a **group of agents, built on harnesses, that produces one type of artifact** — software, content, proposals, and so on. A *harness* is the base model + system instructions + tools that each agent runs on; an *agent* is a harness assigned a role; a *factory* orchestrates a group of them to manufacture its output. This list collects the best tools across that stack — harnesses and frameworks, visual builders, enterprise platforms, agents that build agents, plus the UIs, protocols, observability, and learning resources around them — and links to worked [reference factories](#reference-factories) built in this repo.

Only actively maintained, documented, and genuinely recommendable projects are included.

## Contents

- [Code-First Frameworks](#code-first-frameworks)
- [Visual & Low-Code Builders](#visual--low-code-builders)
- [Enterprise Agent Platforms](#enterprise-agent-platforms)
- [Agents That Build Agents](#agents-that-build-agents)
- [Agent UIs](#agent-uis)
- [Memory & State](#memory--state)
- [Protocols & Interoperability](#protocols--interoperability)
- [Observability & Ops](#observability--ops)
- [Learning Resources](#learning-resources)
- [Reference Factories](#reference-factories)
- [Related Lists](#related-lists)
- [Contributing](#contributing)

## Code-First Frameworks

Libraries for defining agents in code, with control over tools, state, and multi-agent orchestration.

- [Agno](https://github.com/agno-agi/agno) - Fast multi-agent framework with persistent memory and multimodal input; ships AgentOS, a pre-built server with sessions, streaming, and RBAC.
- [AutoGen](https://github.com/microsoft/autogen) - Microsoft framework for conversational multi-agent systems, including group decision-making and debate patterns, with an optional no-code Studio.
- [CrewAI](https://github.com/crewAIInc/crewAI) - Role-based orchestration for modeling teams of agents with the least boilerplate; intuitive for business workflow automation.
- [deepagents](https://github.com/langchain-ai/deepagents) - Batteries-included agent harness on LangGraph with built-in planning, a virtual filesystem, sub-agent context isolation, and human-in-the-loop interrupts.
- [Google ADK](https://github.com/google/adk-python) - Google's official Agent Development Kit with native Gemini and Vertex AI integration.
- [Haystack](https://github.com/deepset-ai/haystack) - deepset's framework for composable pipelines and agents over search and LLMs.
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based framework for stateful, durable, production-grade agent workflows with fine-grained control over branching and error handling.
- [LlamaIndex](https://github.com/run-llama/llama_index) - Data-centric framework whose AgentWorkflow combines agents with first-class RAG over your data.
- [Mastra](https://github.com/mastra-ai/mastra) - TypeScript-first agent framework (from the team behind Gatsby) for the JavaScript ecosystem.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Lightweight Python framework for multi-agent workflows with handoffs, guardrails, and built-in tracing.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Type-safe agent framework from the Pydantic team; gives validated, structured outputs without writing the validators yourself.
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Microsoft's enterprise orchestration SDK for C#, Python, and Java with planners and plugins.
- [smolagents](https://github.com/huggingface/smolagents) - Hugging Face's minimal library for code-acting agents; the fastest setup for a single-agent loop.

## Visual & Low-Code Builders

Drag-and-drop and low-code tools for assembling agents without writing everything by hand.

- [Dify](https://github.com/langgenius/dify) - LLMOps platform combining a visual agent/workflow builder with prompt management and observability.
- [Flowise](https://github.com/FlowiseAI/Flowise) - Visual builder with modular blocks for multi-agent systems; supports 100+ LLMs, embeddings, and vector databases, deployable on-prem or in the cloud.
- [Langflow](https://github.com/langflow-ai/langflow) - Low-code visual editor for agentic and RAG applications with a large component library.
- [n8n](https://github.com/n8n-io/n8n) - Source-available workflow automation with native AI agent nodes for wiring agents into hundreds of integrations.
- [Voiceflow](https://www.voiceflow.com) - Collaborative platform for designing and shipping conversational and voice agents.

## Enterprise Agent Platforms

Managed platforms for building and running agents at scale with governance, security, and data integration.

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) - AWS runtime and tooling for deploying and operating agents securely at scale.
- [Microsoft Foundry](https://ai.azure.com) - Framework-agnostic runtime; agents built with Agent Framework, LangGraph, or other SDKs deploy without rewrites.
- [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) - Open toolkit for connecting, profiling, and optimizing teams of agents across frameworks.
- [Oracle Private Agent Factory](https://blogs.oracle.com/database/introducing-private-agent-factory-unlocking-the-agentic-ai-potential-in-enterprises-with-oracle-ai-database-26ai) - No-code platform to build and run trusted agents over private enterprise data in Oracle AI Database.
- [Salesforce Agentforce](https://www.salesforce.com/agentforce/) - Platform for building autonomous agents embedded across the Salesforce ecosystem.
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) - Google Cloud's managed stack for building, deploying, and scaling agents on Vertex AI.

## Agents That Build Agents

Autonomous systems that generate other agents, code, or whole software projects — the most literal factories.

- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Platform for creating, deploying, and managing continuous, goal-driven autonomous agents.
- [ChatDev](https://github.com/OpenBMB/ChatDev) - Virtual software company where agents in different roles collaborate to develop software.
- [gpt-engineer](https://github.com/gpt-engineer-org/gpt-engineer) - Generates an entire codebase from a natural-language specification, asking for clarification as needed.
- [MetaGPT](https://github.com/geekan/MetaGPT) - Multi-agent framework that simulates a software company, assigning roles to turn one prompt into a project.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) - Platform for autonomous software-engineering agents that write code, run commands, and browse the web.

## Agent UIs

Frontend frameworks for rendering agent state, streaming, and human-in-the-loop approvals.

- [CopilotKit](https://github.com/CopilotKit/CopilotKit) - React frontend stack for agents (maker of the AG-UI protocol) with first-class LangGraph and deep-agents support for shared state, generative UI, and human-in-the-loop.

## Memory & State

Building blocks that give agents long-term memory and persistence.

- [Letta](https://github.com/letta-ai/letta) - Framework (formerly MemGPT) for stateful agents with long-term memory and transparent reasoning.
- [Mem0](https://github.com/mem0ai/mem0) - Memory layer that lets agents remember user preferences and facts across sessions.
- [Zep](https://github.com/getzep/zep) - Memory server providing temporal knowledge graphs and recall for agents.

## Protocols & Interoperability

Standards that let agents talk to tools and to each other.

- [Agent2Agent (A2A)](https://github.com/a2aproject/A2A) - Open protocol for interoperability and communication between agents from different vendors.
- [AG-UI](https://github.com/ag-ui-protocol/ag-ui) - Open protocol standardizing the interaction layer between agents and user-facing applications.
- [Model Context Protocol](https://github.com/modelcontextprotocol) - Anthropic's open standard for connecting agents to tools and data sources through a common interface.

## Observability & Ops

Tracing, evaluation, and monitoring for agents in development and production.

- [AgentOps](https://github.com/AgentOps-AI/agentops) - SDK for tracking agent runs, costs, latency, and failures across popular frameworks.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Open-source tracing and evaluation for LLM and agent pipelines built on OpenTelemetry.
- [Langfuse](https://github.com/langfuse/langfuse) - Open-source observability and analytics for LLM agents with tracing, evals, and prompt management.
- [LangSmith](https://www.langchain.com/langsmith) - Tracing, evaluation, and monitoring for LLM and agent applications.

## Learning Resources

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic's guide to agent patterns, when to use them, and how to keep them simple.
- [OpenAI Cookbook — Agents](https://github.com/openai/openai-cookbook) - Worked examples and recipes for building agents with the OpenAI platform.
- [The AI Agent Factory](https://agentfactory.panaversity.org/) - Open course on the agent-factory paradigm and building production agents.

## Reference Factories

Worked examples built in this repo, each a *group of agents on harnesses that produces one type of artifact*. The reference stack is [deepagents](https://github.com/langchain-ai/deepagents) for the harness and orchestration and [CopilotKit](https://github.com/CopilotKit/CopilotKit) for the UI. Each has a [requirement doc](requirements) and a [build plan](factories).

- [Software Development Factory](factories/software-development-factory/BUILD_PLAN.md) - Produces new software: a reviewed, tested draft pull request. ([requirements](requirements/software-development-factory.md))
- [Content Creation Factory](factories/content-creation-factory/BUILD_PLAN.md) - Produces new content: publish-ready pieces plus channel variants. ([requirements](requirements/content-creation-factory.md))
- [Sales Proposal Factory](factories/sales-proposal-factory/BUILD_PLAN.md) - Produces new proposals: tailored, priced, and compliance-checked. ([requirements](requirements/sales-proposal-factory.md))

## Related Lists

- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents) - Broad directory of AI agents and frameworks maintained by e2b.
- [Awesome AI Agents 2026](https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents-2026) - Large 2026-focused collection of agents, frameworks, and comparisons.
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps) - Curated LLM and agent applications with source code.

## Contributing

Contributions are welcome! Please read the [contribution guidelines](contributing.md) first. In short: suggest only projects you would personally recommend, keep them maintained and documented, and match the existing entry format.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, the authors have waived all copyright and related or neighboring rights to this work.
