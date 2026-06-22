"""Contract tests for the factory's domain tools (RED until implemented)."""

from sdf import tools


def test_run_tests_returns_structured_result():
    result = tools.run_tests("tests/")
    assert "passed" in result


def test_open_pr_returns_url():
    url = tools.open_pr("title", "body", "feature-branch")
    assert url.startswith("http")
