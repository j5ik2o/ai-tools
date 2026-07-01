"""Tests for scripts.generate_report module."""

from scripts.generate_report import generate_html


def make_history_entry(train_results, test_results=None):
    passed = sum(1 for r in train_results if r["pass"])
    return {
        "iteration": 1,
        "description": "desc",
        "train_passed": passed,
        "train_failed": len(train_results) - passed,
        "train_total": len(train_results),
        "train_results": train_results,
        "test_passed": None,
        "test_failed": None,
        "test_total": None,
        "test_results": test_results,
    }


class TestGenerateHtml:
    def test_duplicate_query_columns_keep_their_own_results(self):
        train_results = [
            {"query": "same query", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1},
            {"query": "same query", "should_trigger": False, "pass": False, "triggers": 1, "runs": 1},
        ]
        data = {
            "history": [make_history_entry(train_results)],
            "holdout": 0,
            "original_description": "orig",
            "best_description": "best",
            "best_score": "1/2",
            "iterations_run": 1,
            "train_size": 2,
            "test_size": 0,
        }

        html = generate_html(data)

        # A query-text lookup would render both cells from the same entry
        assert html.count("\u2713") == 1
        assert html.count("\u2717") == 1

    def test_none_test_results_render_without_error(self):
        train_results = [
            {"query": "q", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1},
        ]
        data = {
            "history": [make_history_entry(train_results, test_results=None)],
            "holdout": 0,
            "original_description": "orig",
            "best_description": "best",
            "best_score": "1/1",
            "iterations_run": 1,
            "train_size": 1,
            "test_size": 0,
        }

        html = generate_html(data)

        assert "\u2713" in html
