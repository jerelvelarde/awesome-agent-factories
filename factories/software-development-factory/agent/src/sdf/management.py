"""Management tools that let the factory create and manage its own sub-agents.

These are exposed to the orchestrator so it can author, update, and retire
specialized sub-agents at runtime — like Claude Code subagents — on top of the
seed roles. Stubs until implemented (red scaffold); real implementations operate
on a shared :class:`~sdf.registry.SubAgentRegistry`.
"""

from __future__ import annotations


def create_subagent(
    name: str,
    description: str,
    prompt: str,
    tools: list[str] | None = None,
    model: str | None = None,
) -> dict:
    """Create and register a new managed sub-agent; returns its spec."""
    raise NotImplementedError


def list_subagents() -> list[dict]:
    """List the factory's managed sub-agents."""
    raise NotImplementedError


def update_subagent(name: str, **changes) -> dict:
    """Update a managed sub-agent's definition."""
    raise NotImplementedError


def delete_subagent(name: str) -> None:
    """Retire a managed sub-agent."""
    raise NotImplementedError


MANAGEMENT_TOOLS = [create_subagent, list_subagents, update_subagent, delete_subagent]
MANAGEMENT_TOOL_NAMES = {t.__name__ for t in MANAGEMENT_TOOLS}
