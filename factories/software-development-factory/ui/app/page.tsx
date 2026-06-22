"use client";

import React from "react";
import { CopilotKit, useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import type { AgentState } from "../src/agent-state";

const AGENT_NAME = "software_development_factory";

function FactoryView() {
  const { state } = useCoAgent<Partial<AgentState>>({ name: AGENT_NAME });

  return (
    <main style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, padding: 16 }}>
      <section>
        <h2>Plan</h2>
        <ol>
          {(state.todos ?? []).map((t) => (
            <li key={t.content}>
              {t.status}: {t.content}
            </li>
          ))}
        </ol>

        <h2>Sub-agents</h2>
        <ul>
          {(state.managedSubagents ?? []).map((s) => (
            <li key={s.name}>
              <strong>{s.name}</strong> — {s.description}
            </li>
          ))}
        </ul>

        <h2>Diff</h2>
        <pre>{state.diff ?? "(none yet)"}</pre>

        {state.prUrl ? <a href={state.prUrl}>View pull request</a> : null}
      </section>

      <section>
        <CopilotChat labels={{ initial: "Describe the task to build." }} />
      </section>
    </main>
  );
}

export default function Page() {
  // runtimeUrl points at the CopilotKit runtime that bridges to the deep agent
  // (exposed via langgraph.json / AG-UI). Wiring is a follow-up.
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent={AGENT_NAME}>
      <FactoryView />
    </CopilotKit>
  );
}
