"""
components/code_evaluator.py
Server-side Python code execution and test case evaluation.
Uses threading for timeout safety and exec() with I/O redirection.
"""

import sys
import io
import os
import json
import threading
import traceback
from typing import Dict, Any, List, Optional


# ─── Safe Code Execution ─────────────────────────────────────────────────────

def execute_code(code: str, stdin_input: str = "", timeout: int = 10) -> Dict[str, Any]:
    """
    Execute Python code safely with:
    - Redirected stdin (from stdin_input string)
    - Captured stdout and stderr
    - Timeout via daemon thread
    Returns dict with keys: stdout, stderr, error, timed_out
    """
    result: Dict[str, Any] = {
        "stdout": "",
        "stderr": "",
        "error": None,
        "timed_out": False,
    }

    # Use local references in case thread outlives function
    _stdin_io = io.StringIO(stdin_input)
    _stdout_io = io.StringIO()
    _stderr_io = io.StringIO()

    def _run() -> None:
        orig_stdin = sys.stdin
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdin = _stdin_io
            sys.stdout = _stdout_io
            sys.stderr = _stderr_io
            # Compile first to surface SyntaxErrors cleanly
            compiled = compile(code, "<student_solution>", "exec")
            exec(compiled, {"__builtins__": __builtins__, "__name__": "__main__"})
            result["stdout"] = _stdout_io.getvalue()
            result["stderr"] = _stderr_io.getvalue()
        except SyntaxError as exc:
            result["error"] = f"SyntaxError on line {exc.lineno}: {exc.msg}"
            result["stdout"] = _stdout_io.getvalue()
        except Exception:
            result["error"] = traceback.format_exc()
            result["stdout"] = _stdout_io.getvalue()
        finally:
            sys.stdin = orig_stdin
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        result["timed_out"] = True
        result["error"] = f"⏱️ Time Limit Exceeded ({timeout} seconds)"
        # Restore streams if the thread is still running
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    return result


# ─── Test Case Runner ────────────────────────────────────────────────────────

def run_test_cases(code: str, test_cases: List[Dict]) -> Dict[str, Any]:
    """
    Run student code against each test case.
    Returns detailed per-case results plus overall score.
    """
    case_results: List[Dict] = []

    for i, tc in enumerate(test_cases, start=1):
        stdin_input = tc.get("input", "")
        expected = tc.get("expected_output", "").strip()

        exec_result = execute_code(code, stdin_input, timeout=10)
        actual = exec_result["stdout"].strip()

        if exec_result["timed_out"]:
            status = "TLE"
            passed = False
        elif exec_result["error"]:
            status = "ERROR"
            passed = False
        elif actual == expected:
            status = "PASS"
            passed = True
        else:
            status = "FAIL"
            passed = False

        case_results.append({
            "test_case": i,
            "status": status,
            "passed": passed,
            "input": stdin_input,
            "expected": expected,
            "actual": actual,
            "error": exec_result.get("error"),
        })

    total = len(test_cases)
    passed_count = sum(1 for r in case_results if r["passed"])
    score = round(passed_count / total * 100) if total > 0 else 0

    return {
        "results": case_results,
        "score": score,
        "passed": passed_count,
        "total": total,
    }


# ─── AI Feedback Generation ──────────────────────────────────────────────────

def _deterministic_feedback(eval_result: Dict, skill: str) -> str:
    """Generate structured feedback without an LLM."""
    score = eval_result["score"]
    passed = eval_result["passed"]
    total = eval_result["total"]
    results = eval_result["results"]

    failed = [r for r in results if not r["passed"]]

    if score == 100:
        return (
            f"🏆 **Perfect Score! All {total} test cases passed.**\n\n"
            f"Your solution demonstrates a solid understanding of **{skill}** concepts. "
            f"To take it further:\n"
            f"- Analyze your solution's time and space complexity\n"
            f"- Try to optimize if possible (e.g., reduce from O(n²) to O(n log n))\n"
            f"- Consider edge cases beyond what was tested\n"
            f"- Apply this knowledge in a real project involving {skill}"
        )

    issues = []
    for r in failed[:3]:
        if r["status"] == "ERROR":
            err_preview = (r["error"] or "Unknown error").split("\n")[-1][:120]
            issues.append(f"- **Test {r['test_case']} (ERROR):** `{err_preview}`")
        elif r["status"] == "FAIL":
            exp_preview = r["expected"][:60].replace("\n", "↵")
            act_preview = r["actual"][:60].replace("\n", "↵") if r["actual"] else "(empty)"
            issues.append(
                f"- **Test {r['test_case']} (FAIL):**  \n"
                f"  Expected: `{exp_preview}`  \n"
                f"  Got: `{act_preview}`"
            )
        elif r["status"] == "TLE":
            issues.append(f"- **Test {r['test_case']} (TLE):** Code exceeded 10-second time limit — optimize your algorithm.")

    issues_text = "\n".join(issues) if issues else "- Review the failed test cases carefully."

    if score >= 60:
        mood = "👍 **Good progress!**"
        tip = (
            f"You're close! Check boundary conditions — are all edge cases handled?\n"
            f"Verify output format exactly (trailing spaces, extra newlines, casing)."
        )
    else:
        mood = "💪 **Keep going!**"
        tip = (
            f"Re-read the problem statement and trace through the example manually.\n"
            f"Start with a brute-force solution, get it working, then optimize.\n"
            f"Check your input parsing — are you reading ALL lines correctly?"
        )

    return (
        f"{mood} You passed **{passed}/{total}** test cases (**{score}%**).\n\n"
        f"**Issues found:**\n{issues_text}\n\n"
        f"**Tips to improve:**\n{tip}\n\n"
        f"**Concept focus for {skill}:**  \n"
        f"Review the core mechanics of {skill} and make sure your solution handles "
        f"all described constraints and edge cases."
    )


def _llm_feedback(code: str, eval_result: Dict, skill: str, api_key: str) -> str:
    """Generate AI-powered feedback using Gemini."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        failed = [r for r in eval_result["results"] if not r["passed"]]
        score = eval_result["score"]

        failed_summary = json.dumps(
            [{"test": r["test_case"], "status": r["status"],
              "expected": r["expected"][:100], "actual": r["actual"][:100],
              "error": (r["error"] or "")[:200]} for r in failed[:3]],
            indent=2
        )

        prompt = f"""A student submitted a Python solution for a coding challenge testing {skill} skills.

**Result:** {score}% — {eval_result['passed']}/{eval_result['total']} tests passed

**Student's code:**
```python
{code[:1500]}
```

**Failed test cases (up to 3):**
{failed_summary if failed else "All passed!"}

Write concise, encouraging feedback (4–6 sentences, markdown formatted):
1. What the student did well
2. Specific bug or logic issue (if any), with a hint on how to fix it
3. One targeted tip for strengthening their understanding of {skill}

Be specific, kind, and practical. Use bold for key points."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as exc:
        print(f"[SkillBridge] LLM feedback failed ({exc}), using deterministic feedback.")
        return _deterministic_feedback(eval_result, skill)


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def evaluate_code(
    code: str,
    test_cases: List[Dict],
    skill: str,
) -> Dict[str, Any]:
    """
    Full evaluation pipeline:
    1. Run code against all test cases
    2. Generate AI or deterministic feedback
    Returns eval_result dict with added 'feedback' key.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    try:
        import streamlit as st
        api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    eval_result = run_test_cases(code, test_cases)

    if api_key:
        eval_result["feedback"] = _llm_feedback(code, eval_result, skill, api_key)
    else:
        eval_result["feedback"] = _deterministic_feedback(eval_result, skill)

    return eval_result
