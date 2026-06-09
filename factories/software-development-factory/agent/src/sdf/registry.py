"""Dynamic sub-agent registry for the factory.

The factory can create and manage its own sub-agents at runtime — like Claude
Code subagents — rather than being limited to a fixed roster. Each managed
sub-agent is a harness definition: name + description + system prompt + tools
(+ optional model). Seed roles are registered at startup; the orchestrator may
author new specialized sub-agents and persist them via a backend so they are
managed across runs.

Read access (seed/list/get) is implemented; mutating operations are stubs until
implemented (red scaffold).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SubAgentSpec:
    """A managed sub-agent definition (a harness)."""

    name: str
    description: str
    prompt: str
    tools: tuple[str, ...] = ()
    model: str | None = None


def _spec_from_dict(d: dict) -> SubAgentSpec:
    return SubAgentSpec(
        name=d["name"],
        description=d["description"],
        prompt=d["prompt"],
        tools=tuple(t.__name__ if callable(t) else t for t in d.get("tools", ())),
        model=d.get("model"),
    )


class SubAgentRegistry:
    """In-memory registry of the sub-agents a factory creates and manages."""

    def __init__(self, seed: Iterable[dict] | None = None) -> None:
        self._specs: dict[str, SubAgentSpec] = {}
        for d in seed or ():
            spec = _spec_from_dict(d)
            self._specs[spec.name] = spec

    def list(self) -> list[SubAgentSpec]:
        return list(self._specs.values())

    def names(self) -> set[str]:
        return set(self._specs)

    def get(self, name: str) -> SubAgentSpec | None:
        return self._specs.get(name)

    def create(self, spec: SubAgentSpec) -> SubAgentSpec:
        """Register a new managed sub-agent and persist it."""
        raise NotImplementedError

    def update(self, name: str, **changes) -> SubAgentSpec:
        """Update an existing managed sub-agent's definition."""
        raise NotImplementedError

    def delete(self, name: str) -> None:
        """Retire a managed sub-agent."""
        raise NotImplementedError
