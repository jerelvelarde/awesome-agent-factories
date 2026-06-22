"""Management tools that let the factory create and manage its own sub-agents.

These are exposed to the orchestrator so it can author, update, and retire
specialized sub-agents at runtime — like Claude Code subagents — on top of the
seed roles.

The module-level functions below are the static catalog (stable names/signatures
used for wiring and tests). Because each agent gets its own
:class:`~sdf.registry.SubAgentRegistry` inside ``build_agent()``, the *runtime*
tools must be bound to that specific instance rather than module-level global
state (which would break isolation across concurrent runs). Use
:func:`make_management_tools` to build registry-bound tools. All stubs until
implemented (red scaffold).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .registry import SubAgentRegistry


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


def make_management_tools(registry: "SubAgentRegistry") -> list:
    """Build management tools bound to a specific ``registry`` instance.

    Implementations should close over ``registry`` (or expose it as methods) so
    each agent run manages its own sub-agents in isolation. Returns a list of
    bound tools mirroring :data:`MANAGEMENT_TOOLS`.
    """
    raise NotImplementedError
