"""Sub-agent definitions (roles) for the Software Development Factory.

Each sub-agent is a harness — a model + system prompt + tools — with context
isolation, mapping 1:1 to the roles in the requirement doc. Prompts are
placeholders until implemented (red scaffold).
"""

from __future__ import annotations

from .tools import open_pr, read_repo, run_lint, run_tests, write_file

# TODO: replace placeholder prompts with real role instructions.
SUBAGENTS = [
    {
        "name": "planner",
        "description": "Decompose the task into a step-by-step plan and the files to touch.",
        "prompt": "TODO: planner instructions",
        "tools": [read_repo],
    },
    {
        "name": "implementer",
        "description": "Write code matching existing conventions in small, reviewable increments.",
        "prompt": "TODO: implementer instructions",
        "tools": [read_repo, write_file],
    },
    {
        "name": "test_engineer",
        "description": "Write/update tests; ensure they fail before and pass after the change.",
        "prompt": "TODO: test engineer instructions",
        "tools": [write_file, run_tests],
    },
    {
        "name": "reviewer",
        "description": "Correctness and quality pass on the diff; request changes until clean.",
        "prompt": "TODO: reviewer instructions",
        "tools": [read_repo],
    },
    {
        "name": "verifier",
        "description": "Run build, lint, and tests; confirm behavior, not just green tests.",
        "prompt": "TODO: verifier instructions",
        "tools": [run_tests, run_lint],
    },
    {
        "name": "integrator",
        "description": "Open a draft PR with summary, plan, and test evidence.",
        "prompt": "TODO: integrator instructions",
        "tools": [open_pr],
    },
]

SUBAGENT_NAMES = {s["name"] for s in SUBAGENTS}
