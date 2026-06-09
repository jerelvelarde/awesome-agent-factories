"""Tests for the dynamic sub-agent registry.

Seeding and read access pass now; create/update/delete are RED until the
factory's self-management is implemented.
"""

from sdf.registry import SubAgentRegistry, SubAgentSpec
from sdf.subagents import SUBAGENTS


def test_registry_seeds_roles():
    reg = SubAgentRegistry(seed=SUBAGENTS)
    assert "planner" in reg.names()
    assert len(reg.list()) == len(SUBAGENTS)


def test_create_managed_subagent():
    reg = SubAgentRegistry(seed=SUBAGENTS)
    spec = SubAgentSpec(
        name="migration_specialist",
        description="Handles database migrations.",
        prompt="You write safe, reversible migrations.",
        tools=("read_repo", "write_file"),
    )
    reg.create(spec)
    assert reg.get("migration_specialist") == spec


def test_delete_managed_subagent():
    reg = SubAgentRegistry(seed=SUBAGENTS)
    reg.delete("planner")
    assert "planner" not in reg.names()
