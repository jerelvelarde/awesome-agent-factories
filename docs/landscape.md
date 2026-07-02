# Choosing an agent stack

A short, opinionated guide to the [Awesome Agent Factories](../README.md) landscape:
**which kind of tool you actually need**, and a **side-by-side comparison** of the
leading code-first harnesses. Curated 2026; verified against primary sources.

An *agent factory* is a group of agents — each a *harness* (model + instructions +
tools) — orchestrated to produce one type of artifact. Building one means picking a
piece from several layers, not a single "framework."

## Pick by layer

| You need to… | Reach for | Category |
| --- | --- | --- |
| Define agents in code with full control | LangGraph, deepagents, OpenAI Agents SDK, CrewAI, Pydantic AI, Google ADK | [Code-First Frameworks](../README.md#code-first-frameworks) |
| Assemble agents visually / with a team | Dify, Langflow, Flowise, Sim Studio | [Visual & Low-Code Builders](../README.md#visual--low-code-builders) |
| Run agents at enterprise scale with governance | Bedrock AgentCore, Microsoft Foundry, watsonx Orchestrate | [Enterprise Agent Platforms](../README.md#enterprise-agent-platforms) |
| Have an agent write/ship software | OpenHands, SWE-agent, Aider, Cline | [Agents That Build Agents](../README.md#agents-that-build-agents) |
| Put a UI on an agent (state, streaming, approvals) | CopilotKit, assistant-ui, Vercel AI SDK | [Agent UIs](../README.md#agent-uis) |
| Build a voice / phone agent | LiveKit Agents, Pipecat, Vapi | [Voice & Realtime Agents](../README.md#voice--realtime-agents) |
| Drive a browser or a computer | Browser Use, Stagehand, Playwright MCP | [Browser & Computer-Use](../README.md#browser--computer-use-agents) |
| Give agents long-term memory | Letta, Mem0, Zep, Cognee | [Memory & State](../README.md#memory--state) |
| Give agents authenticated tools | Composio, Arcade.dev, MCP registries | [Tools & Integrations](../README.md#tools--integrations) |
| Let agents interoperate | MCP, A2A, AG-UI | [Protocols](../README.md#protocols--interoperability) |
| Run agent-generated code safely | E2B, Modal, Daytona, Microsandbox | [Sandboxes & Execution](../README.md#sandboxes--execution) |
| Measure whether the agent is good | LangSmith, promptfoo, DeepEval, Ragas | [Evaluation & Testing](../README.md#evaluation--testing) |
| See what agents do in production | Langfuse, Helicone, AgentOps, OpenLLMetry | [Observability & Ops](../README.md#observability--ops) |
| Keep agents safe and on-policy | Guardrails AI, NeMo Guardrails, LLM Guard, Presidio | [Guardrails & Safety](../README.md#guardrails--safety) |

A real factory usually combines **one harness + memory + tools + a sandbox (if it
runs code) + eval + observability + a guardrail + a UI**. The [reference factories](../README.md#reference-factories)
in this repo are worked examples of exactly that composition.

## Code-first harness comparison

The nine most-used code-first harnesses, compared on the axes that matter when you
pick one for a factory. Cells are terse by design; follow the framework's docs for
detail.

| Framework | Language(s) | Multi-agent | Human-in-the-loop | Memory / persistence | Streaming / UI | Eval / observability | License |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **LangGraph** | Python, JS/TS | Yes — graph; supervisor & swarm | Yes — `interrupt()` / `Command(resume)` | Checkpointers (short) + Store (long) | Token/step streaming; Studio; AG-UI/CopilotKit | LangSmith (native); OpenTelemetry | MIT |
| **CrewAI** | Python | Yes — crews + flows | Yes — built-in | Unified memory (short/long/entity) + flow state | Streaming; Control Plane UI (EE) | Native tracing; AgentOps | MIT |
| **AutoGen** | Python, .NET | Yes — teams / group chat | Yes — `UserProxyAgent` | Agent memory + state | Token streaming; AutoGen Studio | OpenTelemetry (native) | MIT · maintenance mode¹ |
| **deepagents** | Python, JS/TS | Yes — sub-agents (isolated context) | Yes — inherits LangGraph interrupts | Virtual filesystem + LangGraph checkpointer | Streaming via LangGraph; Studio | LangSmith (via LangGraph) | MIT |
| **Google ADK** | Python, Java, TS, Go | Yes — Sequential/Parallel/Loop + sub-agents; A2A | Yes — `require_confirmation` / long-running tools | Session / State / Memory services | Bidi live streaming; `adk web` | Native eval; OTel; Cloud Trace | Apache-2.0 |
| **OpenAI Agents SDK** | Python, JS/TS | Yes — handoffs, agents-as-tools | Yes — run interruption | Sessions (SQLite/Redis/Postgres) | Token streaming; Traces dashboard | Native tracing; OTel exporters | MIT |
| **Pydantic AI** | Python | Yes — delegation, graph flow | Yes — tool-call approval | Message history; durable execution | Structured streaming; AG-UI, Vercel AI | Native OpenTelemetry; Logfire | MIT |
| **Mastra** | TypeScript/JS | Yes — workflows, agent networks | Yes — workflow suspend/resume | Memory + storage adapters | Resumable streaming; AG-UI/CopilotKit | Built-in scorers; OTel | Apache-2.0² |
| **Agno** | Python | Yes — teams + step workflows | Yes — pause/approval flows | Sessions, memory, knowledge (own DB) | Streaming; AgentOS runtime + UI | Native OpenTelemetry; run history | Apache-2.0 |

¹ AutoGen is in maintenance mode; Microsoft positions the Agent Framework as its
successor — both are still actively committed. ² Mastra's core is Apache-2.0; its
enterprise (`ee/`) directories are source-available.

*All cells verified against official docs/repositories as of 2026. Star counts and
exact feature availability move fast — confirm against each project before relying
on a specific capability.*
