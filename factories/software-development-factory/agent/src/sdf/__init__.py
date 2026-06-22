"""Software Development Factory: a deepagents-based agent factory.

Produces new software — a reviewed, tested draft pull request — as a group of
role-specialized sub-agents (harnesses) orchestrated by one deep agent.
"""

from .agent import build_agent

__all__ = ["build_agent"]
