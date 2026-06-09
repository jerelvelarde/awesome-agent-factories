"""Human-in-the-loop approval gates for the Software Development Factory.

Approval gates are tool-level interrupts: the orchestrator pauses before an
approval-gated tool runs and waits for human confirmation (surfaced in the
CopilotKit UI). The human owns the merge boundary, so ``open_pr`` is gated.
"""

from __future__ import annotations

# Tools that require human approval before they execute.
APPROVAL_TOOLS = ["open_pr"]


def interrupt_config() -> dict:
    """Return the deepagents/LangGraph interrupt config for the approval tools.

    Expected shape: a mapping that marks each tool in ``APPROVAL_TOOLS`` as
    requiring an interrupt (human approval) before execution.
    """
    raise NotImplementedError
