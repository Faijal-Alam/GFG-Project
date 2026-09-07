"""
components/skill_analyzer.py
Skill gap analysis — tries Gemini LLM first, falls back to keyword matching.
Clearly distinguishes: explicit skills, inferred skills, missing skills.
"""

import os
import re
import json
from typing import Dict, Any, List

# ─── Skill Taxonomy ──────────────────────────────────────────────────────────

# Comprehensive list of tech skills with common aliases
SKILLS_LIST = [
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "C#",
    "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R",
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
    "Cassandra", "DynamoDB", "Elasticsearch", "Oracle",
    # Web / APIs
    "REST APIs", "GraphQL", "gRPC", "WebSockets", "HTTP",
    "FastAPI", "Flask", "Django", "Express.js", "Spring Boot", "Node.js",
    "Next.js", "React", "Vue", "Angular", "Svelte",
    # DevOps / Cloud
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD",
    "Jenkins", "GitHub Actions", "Terraform", "Linux", "Bash",
    # Data Science / ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "scikit-learn", "Pandas", "NumPy", "Matplotlib", "NLP",
    # DS&Algo
    "Data Structures", "Algorithms", "DSA", "Dynamic Programming",
    "Problem Solving", "Recursion", "Competitive Programming",
    # Auth / Security
    "JWT", "OAuth", "Authentication", "Authorization",
    # Testing
    "pytest", "Unit Testing", "TDD", "Jest",
    # Architecture
    "System Design", "Microservices", "OOP", "Functional Programming",
    # Tools
    "Git", "GitHub", "Postman", "Swagger", "Jupyter",
    # Other
    "Agile", "Scrum", "API Design", "Database Design",
]

# Aliases map: canonical skill → list of alternative phrases to search for
SKILL_ALIASES: Dict[str, List[str]] = {
    "REST APIs":          ["rest api", "restful api", "rest apis", "rest web service",
                           "restful", "http api", "web api", "api development", "api design"],
    "Data Structures":    ["data structures", "data structure", "dsa", "ds&algo", "ds & algo"],
    "Algorithms":         ["algorithm", "dsa", "competitive programming", "problem-solving"],
    "Problem Solving":    ["problem solving", "problem-solving", "analytical thinking"],
    "Machine Learning":   ["machine learning", "ml model", "supervised learning"],
    "Deep Learning":      ["deep learning", "neural network", "cnn", "rnn", "lstm"],
    "FastAPI":            ["fastapi", "fast api"],
    "scikit-learn":       ["scikit-learn", "sklearn"],
    "GitHub Actions":     ["github actions", "github ci"],
    "Express.js":         ["express.js", "express js", "expressjs"],
    "System Design":      ["system design", "distributed system", "scalable architecture"],
    "Unit Testing":       ["unit test", "unit testing", "test driven"],
    "CI/CD":              ["ci/cd", "ci cd", "continuous integration", "continuous deployment"],
    "Database Design":    ["database design", "schema design", "db design", "er diagram"],
}

# Inferred skill patterns: if these phrases appear, we infer the skill
INFERENCE_RULES: Dict[str, List[str]] = {
    "REST APIs":      ["endpoint", "http request", "api call", "web service", "request handling"],
    "FastAPI":        ["async api", "openapi", "pydantic model", "swagger"],
    "System Design":  ["scalable", "distributed", "microservice", "load balanc", "caching layer"],
    "Problem Solving":["leetcode", "hackerrank", "competitive", "algorithmic thinking"],
    "Docker":         ["container", "containerize", "dockerfile", "image pull"],
    "CI/CD":          ["pipeline", "automated deploy", "build system"],
    "JWT":            ["token-based", "bearer token", "authentication token"],
}


def _normalize(text: str) -> str:
    return text.lower()


def _skill_in_text(skill: str, text_lower: str) -> bool:
    """Check if a skill appears explicitly in the text (word-boundary aware)."""
    candidates = [skill.lower()] + [a for a in SKILL_ALIASES.get(skill, [])]
    for phrase in candidates:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, text_lower):
            return True
    return False


def _skill_inferred(skill: str, text_lower: str) -> bool:
    """Check if a skill can be reasonably inferred from context clues."""
    for keyword in INFERENCE_RULES.get(skill, []):
        if keyword in text_lower:
            return True
    return False


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract skills from free text, returning:
      - explicit: directly mentioned skills
      - inferred: skills implied by context
    """
    text_lower = _normalize(text)
    explicit, inferred = [], []

    for skill in SKILLS_LIST:
        if _skill_in_text(skill, text_lower):
            explicit.append(skill)
        elif _skill_inferred(skill, text_lower):
            inferred.append(skill)

    return {"explicit": list(dict.fromkeys(explicit)),
            "inferred": list(dict.fromkeys(inferred))}


def _prioritize_missing(missing: List[str], jd_text: str) -> List[str]:
    """Rank missing skills by frequency in JD text (proxy for importance)."""
    jd_lower = _normalize(jd_text)
    scored = []
    for skill in missing:
        count = len(re.findall(r"\b" + re.escape(skill.lower()) + r"\b", jd_lower))
        # Check aliases too
        for alias in SKILL_ALIASES.get(skill, []):
            count += jd_lower.count(alias)
        scored.append((skill, count))
    scored.sort(key=lambda x: -x[1])
    return [s for s, _ in scored]


_RECOMMENDATIONS: Dict[str, str] = {
    "REST APIs": (
        "Start by learning HTTP methods (GET, POST, PUT, DELETE), status codes (2xx, 4xx, 5xx), "
        "and JSON request/response format. Build a simple CRUD API using Flask or FastAPI to "
        "get hands-on experience with endpoint design, path parameters, and query strings."
    ),
    "FastAPI": (
        "Install FastAPI and follow the official tutorial to build a simple API with typed "
        "path/query parameters, request bodies using Pydantic models, and automatic Swagger docs. "
        "Practice async/await for non-blocking endpoints."
    ),
    "SQL": (
        "Practice complex SQL beyond basic SELECT: write JOINs (INNER, LEFT, RIGHT), aggregate "
        "functions with GROUP BY and HAVING, subqueries, and window functions. Use PostgreSQL "
        "locally and solve exercises on SQLZoo or LeetCode's Database section."
    ),
    "Docker": (
        "Learn Docker fundamentals: build a Dockerfile for a Python app, run containers, "
        "map ports, and use docker-compose to orchestrate multi-service setups (e.g., FastAPI + "
        "PostgreSQL). Aim to containerize one of your existing projects."
    ),
    "JWT": (
        "Study the JWT structure (header.payload.signature) and the auth flow: login → issue token "
        "→ client sends token in headers → server validates. Implement JWT auth in a FastAPI app "
        "using the python-jose library and understand token expiry/refresh."
    ),
    "Machine Learning": (
        "Start with scikit-learn: load a dataset, split train/test, train a classifier (e.g., "
        "RandomForest), evaluate with metrics (accuracy, F1). Follow Andrew Ng's ML course on "
        "Coursera to build conceptual foundations."
    ),
    "System Design": (
        "Read 'Designing Data-Intensive Applications' (Kleppmann). Practice drawing system "
        "diagrams for common problems (URL shortener, rate limiter, chat app). Focus on "
        "scalability patterns: load balancing, caching (Redis), database sharding."
    ),
    "AWS": (
        "Create an AWS free-tier account. Practice S3 (file storage), EC2 (virtual servers), "
        "Lambda (serverless functions), and RDS (managed databases). Deploy a simple Python "
        "app to EC2 and aim for the AWS Cloud Practitioner certification."
    ),
    "Problem Solving": (
        "Solve 2–3 LeetCode problems daily focusing on patterns: sliding window, two pointers, "
        "binary search, BFS/DFS, and dynamic programming. Aim for 100+ medium problems. "
        "Track your progress and revisit problems you couldn't solve."
    ),
    "GraphQL": (
        "Learn the GraphQL schema definition language (SDL), resolvers, and client-side queries. "
        "Build a simple GraphQL API using Strawberry (Python) or Ariadne. Compare it with "
        "REST to understand the tradeoffs."
    ),
}


def _get_recommendations(priority_gaps: List[str]) -> Dict[str, str]:
    result = {}
    for gap in priority_gaps[:4]:
        if gap in _RECOMMENDATIONS:
            result[gap] = _RECOMMENDATIONS[gap]
        else:
            result[gap] = (
                f"Practice {gap} through official documentation, tutorials, and small projects. "
                f"Build one project specifically using {gap} and document it on GitHub."
            )
    return result


# ─── Fallback (Keyword-Based) Analysis ───────────────────────────────────────

def analyze_skills_fallback(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Rule-based skill gap analysis — no LLM required."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    all_resume = set(resume_skills["explicit"] + resume_skills["inferred"])
    all_jd = set(jd_skills["explicit"] + jd_skills["inferred"])

    matched = sorted(all_resume & all_jd)
    missing = sorted(all_jd - all_resume)

    priority_gaps = _prioritize_missing(missing, jd_text)[:5]
    recommendations = _get_recommendations(priority_gaps)

    match_pct = min(100, round(len(matched) / max(len(all_jd), 1) * 100))

    resume_skills_labeled = (
        [{"skill": s, "source": "explicit"} for s in resume_skills["explicit"]] +
        [{"skill": s, "source": "inferred"} for s in resume_skills["inferred"]]
    )
    jd_skills_labeled = (
        [{"skill": s, "source": "explicit"} for s in jd_skills["explicit"]] +
        [{"skill": s, "source": "inferred"} for s in jd_skills["inferred"]]
    )

    return {
        "match_percentage": match_pct,
        "resume_skills": resume_skills_labeled,
        "jd_skills": jd_skills_labeled,
        "matched_skills": matched,
        "missing_skills": missing,
        "priority_gaps": priority_gaps,
        "recommendations": recommendations,
        "mode": "fallback",
    }


# ─── LLM-Powered Analysis ────────────────────────────────────────────────────

def analyze_skills_with_llm(resume_text: str, jd_text: str, api_key: str) -> Dict[str, Any]:
    """Gemini-powered skill gap analysis with structured JSON output."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are a professional technical recruiter and career coach.
Analyze this resume and job description to identify skill gaps.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:2000]}

Respond with ONLY a valid JSON object (no markdown fences, no explanation):
{{
  "match_percentage": <integer 0-100>,
  "resume_skills": [
    {{"skill": "<skill>", "source": "explicit|inferred"}}
  ],
  "jd_skills": [
    {{"skill": "<skill>", "source": "explicit|inferred"}}
  ],
  "matched_skills": ["<skill>", ...],
  "missing_skills": ["<skill>", ...],
  "priority_gaps": ["<most_important_missing>", "<2nd>", "<3rd>", "<4th>", "<5th>"],
  "recommendations": {{
    "<skill>": "<2-3 sentence actionable recommendation>"
  }},
  "mode": "llm"
}}

Rules:
1. Only include skills actually stated or strongly implied — do NOT hallucinate
2. "explicit" = directly mentioned; "inferred" = clearly implied by context
3. Priority gaps = missing skills most critical for this specific job (ranked)
4. Recommendations must be specific and actionable (not generic)
5. Return valid JSON only"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    result = json.loads(raw)
    result["mode"] = "llm"
    return result


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def analyze_skills(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Analyze skill gaps between resume and JD.
    Tries Gemini API first; gracefully falls back to keyword matching.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    try:
        import streamlit as st
        api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if api_key:
        try:
            return analyze_skills_with_llm(resume_text, jd_text, api_key)
        except Exception as exc:
            print(f"[SkillBridge] LLM analysis failed ({exc}), using keyword fallback.")

    return analyze_skills_fallback(resume_text, jd_text)
