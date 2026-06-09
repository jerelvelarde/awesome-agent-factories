"""Contract tests for the Software Development Factory orchestrator.

Config/contract tests pass now; behavioral tests are RED until ``build_agent``
is implemented.
"""

import pytest

from sdf.agent import build_agent
from sdf.management import MANAGEMENT_TOOL_NAMES
from sdf.subagents import SUBAGENT_NAMES
from sdf.tools import TOOL_NAMES

EXPECTED_SUBAGENTS = {
    "planner",
    "implementer",
    "test_engineer",
    "reviewer",
    "verifier",
    "integrator",
}

EXPECTED_TOOLS = {"read_repo", "write_file", "run_tests", "run_lint", "open_pr"}

EXPECTED_MANAGEMENT_TOOLS = {
    "create_subagent",
    "list_subagents",
    "update_subagent",
    "delete_subagent",
}


def test_subagent_roles_match_spec():
    assert SUBAGENT_NAMES == EXPECTED_SUBAGENTS


def test_domain_tools_match_spec():
    assert TOOL_NAMES == EXPECTED_TOOLS


def test_management_tools_present():
    # The factory can create and manage its own sub-agents.
    assert MANAGEMENT_TOOL_NAMES == EXPECTED_MANAGEMENT_TOOLS


def test_build_agent_returns_invocable():
    agent = build_agent()
    assert hasattr(agent, "invoke")
