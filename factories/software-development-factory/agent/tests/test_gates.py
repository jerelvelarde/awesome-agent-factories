"""Tests for human-in-the-loop approval gates."""

from sdf.gates import APPROVAL_TOOLS, interrupt_config


def test_open_pr_requires_approval():
    assert "open_pr" in APPROVAL_TOOLS


def test_interrupt_config_gates_approval_tools():
    # RED until implemented.
    config = interrupt_config()
    assert "open_pr" in config
