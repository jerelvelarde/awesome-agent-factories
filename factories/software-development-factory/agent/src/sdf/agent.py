"""Software Development Factory — the orchestrator deep agent.

Assembles the role sub-agents (harnesses) into one deepagents deep agent that
produces a reviewed, tested draft pull request. Planning, the code workspace
(virtual filesystem), and approval interrupts come from deepagents.

The orchestrator also gets management tools so the factory can create and manage
its own sub-agents at runtime (like Claude Code subagents) on top of the seed
roles, via a shared :class:`~sdf.registry.SubAgentRegistry`.
"""

from __future__ import annotations

from .gates import APPROVAL_TOOLS, interrupt_config  # noqa: F401  (used once implemented)
from .management import make_management_tools  # noqa: F401
from .registry import SubAgentRegistry  # noqa: F401
from .subagents import SUBAGENTS  # noqa: F401
from .tools import ALL_TOOLS  # noqa: F401

DEFAULT_MODEL = "anthropic:claude-sonnet-4-6"

SYSTEM_PROMPT = """\
You are the orchestrator of a Software Development Factory. Given a task,
produce a reviewed, tested change as a draft pull request. Plan first using
your todo list, delegate to your sub-agents, and create new specialized
sub-agents when a task needs a role you do not yet have. Never open a pull
request without passing tests and human approval.
"""


def build_agent(model: str = DEFAULT_MODEL, checkpointer=None):
    """Build the orchestrator deep agent.

    Seeds a per-agent :class:`SubAgentRegistry` with ``SUBAGENTS`` and wires
    ``SYSTEM_PROMPT``, ``ALL_TOOLS``, and the registry-bound management tools
    from ``make_management_tools(registry)`` (for dynamic sub-agent management)
    into a deepagents deep agent, with ``APPROVAL_TOOLS`` interrupt-gated for
    human-in-the-loop approval. Returns a compiled deep agent (a LangGraph
    graph).
    """
    raise NotImplementedError("build_agent is not implemented yet (red scaffold)")
