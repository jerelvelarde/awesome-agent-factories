"""Domain tools for the Software Development Factory.

Stubs only — each raises ``NotImplementedError`` until implemented (red
scaffold). Real implementations will wrap these as LangChain tools behind
adapters (GitHub, CI, an isolated build/test sandbox) so tests can use fakes.
"""

from __future__ import annotations


def read_repo(path: str) -> str:
    """Return the contents of a repository path."""
    raise NotImplementedError


def write_file(path: str, content: str) -> None:
    """Write content to a file in the working tree."""
    raise NotImplementedError


def run_tests(target: str = "") -> dict:
    """Run the test suite and return a structured result (e.g. ``{"passed": int, "failed": int}``)."""
    raise NotImplementedError


def run_lint(target: str = "") -> dict:
    """Run linters and return a structured result."""
    raise NotImplementedError


def open_pr(title: str, body: str, branch: str) -> str:
    """Open a draft pull request and return its URL. Approval-gated."""
    raise NotImplementedError


ALL_TOOLS = [read_repo, write_file, run_tests, run_lint, open_pr]
TOOL_NAMES = {t.__name__ for t in ALL_TOOLS}
