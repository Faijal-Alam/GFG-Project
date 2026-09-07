"""
components/challenge_generator.py
Generates personalized coding challenges — LLM first, pre-built fallback.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any

FALLBACK_PATH = Path(__file__).parent.parent / "data" / "fallback_challenges.json"

# ─── Skill → Challenge Key Mapping ──────────────────────────────────────────
# Maps a skill name to one of the pre-built challenge keys in fallback_challenges.json

SKILL_TO_KEY: Dict[str, str] = {
    # REST APIs / HTTP
    "REST APIs": "REST APIs",
    "RESTful API": "REST APIs",
    "API Design": "REST APIs",
    "HTTP": "REST APIs",
    "HTTPS": "REST APIs",
    "WebSockets": "REST APIs",
    "gRPC": "REST APIs",
    "GraphQL": "REST APIs",

    # FastAPI / Web Frameworks
    "FastAPI": "FastAPI",
    "Flask": "FastAPI",
    "Django": "FastAPI",
    "Express.js": "FastAPI",
    "Node.js": "FastAPI",
    "Spring Boot": "FastAPI",
    "JWT": "FastAPI",
    "OAuth": "FastAPI",
    "Authentication": "FastAPI",

    # SQL / Databases
    "SQL": "SQL",
    "MySQL": "SQL",
    "PostgreSQL": "SQL",
    "SQLite": "SQL",
    "MongoDB": "SQL",
    "Redis": "SQL",
    "Database Design": "SQL",
    "Elasticsearch": "SQL",

    # Docker / DevOps
    "Docker": "Docker",
    "Kubernetes": "Docker",
    "CI/CD": "Docker",
    "DevOps": "Docker",
    "Linux": "Docker",
    "AWS": "Docker",
    "GCP": "Docker",
    "Azure": "Docker",
    "Bash": "Docker",
    "GitHub Actions": "Docker",
    "Terraform": "Docker",

    # Algorithms / DSA
    "Data Structures": "Algorithms",
    "Algorithms": "Algorithms",
    "DSA": "Algorithms",
    "Dynamic Programming": "Algorithms",
    "Problem Solving": "Algorithms",
    "System Design": "Algorithms",
    "Recursion": "Algorithms",
    "Competitive Programming": "Algorithms",
    "Machine Learning": "Algorithms",
    "Deep Learning": "Algorithms",
    "TensorFlow": "Algorithms",
    "PyTorch": "Algorithms",
}


def _load_fallback() -> Dict:
    with open(FALLBACK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_fallback_challenge(skill: str) -> Dict[str, Any]:
    """Return the closest pre-built challenge for the given skill."""
    challenges = _load_fallback()

    # Direct match
    if skill in challenges:
        ch = dict(challenges[skill])
        ch["generated_by"] = "fallback"
        return ch

    # Mapped match
    key = SKILL_TO_KEY.get(skill)
    if key and key in challenges:
        ch = dict(challenges[key])
        ch["generated_by"] = "fallback"
        return ch

    # Default
    ch = dict(challenges.get("default", list(challenges.values())[0]))
    ch["generated_by"] = "fallback"
    return ch


# ─── LLM Challenge Generation ────────────────────────────────────────────────

def _generate_with_llm(skill: str, jd_context: str, api_key: str) -> Dict[str, Any]:
    """Generate an original coding challenge using Gemini."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Create an ORIGINAL coding challenge testing a candidate's practical understanding of: {skill}

Job context: {jd_context[:400] if jd_context else "Backend software engineering internship"}

Requirements:
- The problem must be ORIGINAL (NOT from LeetCode, HackerRank, GFG, or any platform)
- Solvable in Python within 20–30 minutes by an intermediate student
- Uses standard stdin/stdout (no GUI, no web calls)
- Has clear, unambiguous, deterministic test cases

Respond with ONLY a valid JSON object (no markdown):
{{
  "title": "<creative original title that hints at the skill>",
  "difficulty": "Easy|Medium|Hard",
  "problem_statement": "<clear 3-5 sentence description of the problem scenario and task>",
  "input_format": "<precise description of input format>",
  "output_format": "<precise description of expected output format>",
  "constraints": "<constraints on input size and values>",
  "examples": [
    {{
      "input": "<example input>",
      "output": "<example output>",
      "explanation": "<brief explanation>"
    }}
  ],
  "skill_tested": "{skill}",
  "starter_code": "<valid Python starter code with helpful TODO comments, using sys.stdin>",
  "test_cases": [
    {{"input": "<test input with \\n for newlines>", "expected_output": "<exact expected output with \\n>"}},
    {{"input": "<test input>", "expected_output": "<expected output>"}},
    {{"input": "<test input>", "expected_output": "<expected output>"}},
    {{"input": "<test input>", "expected_output": "<expected output>"}}
  ]
}}

CRITICAL:
- test_cases must have EXACTLY matching expected_output (strip trailing whitespace)
- starter_code must be runnable Python using sys.stdin for input
- All newlines in JSON string values must use \\n escape sequences"""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    challenge = json.loads(raw)
    challenge["generated_by"] = "llm"
    return challenge


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def generate_challenge(skill: str, jd_text: str = "") -> Dict[str, Any]:
    """
    Generate a personalized coding challenge for the given skill gap.
    Tries Gemini API first; gracefully falls back to pre-built challenges.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    try:
        import streamlit as st
        api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if api_key:
        try:
            return _generate_with_llm(skill, jd_text, api_key)
        except Exception as exc:
            print(f"[SkillBridge] LLM challenge generation failed ({exc}), using fallback.")

    return _get_fallback_challenge(skill)
