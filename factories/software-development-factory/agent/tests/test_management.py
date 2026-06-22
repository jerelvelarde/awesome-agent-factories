"""Tests for the sub-agent management tools (RED until implemented).

These tools let the factory create and manage its own sub-agents at runtime,
like Claude Code subagents.
"""

from sdf import management


def test_create_subagent_returns_spec():
    spec = management.create_subagent(
        name="perf_profiler",
        description="Profiles hot paths and proposes optimizations.",
        prompt="You find and fix performance bottlenecks.",
        tools=["read_repo", "run_tests"],
    )
    assert spec["name"] == "perf_profiler"


def test_list_subagents_includes_seed_roles():
    names = {s["name"] for s in management.list_subagents()}
    assert "planner" in names
