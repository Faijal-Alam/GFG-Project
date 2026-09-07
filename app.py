"""
app.py — SkillBridge: Employability Gap Analyzer & Custom Coding Assessment Engine
Main Streamlit application. Entry point: `streamlit run app.py`
Modern AI + Developer Tool Visual Design System (Deep Navy & Electric Blue)
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config MUST be the first Streamlit call ──────────────────────────────
st.set_page_config(
    page_title="SkillBridge | AI Employability Gap Analyzer",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Component imports (after set_page_config) ─────────────────────────────────
from components.skill_analyzer import analyze_skills
from components.challenge_generator import generate_challenge
from components.code_evaluator import evaluate_code, execute_code
from utils.helpers import load_sample_resume, load_sample_jd, get_pyodide_editor_html


# ═══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM & CUSTOM CSS (Deep Navy, Electric Blue, Violet AI)
# ═══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── App Background ── */
.stApp {
    background-color: #0B1020 !important;
    color: #F8FAFC !important;
}

/* ── Hero Banner Header ── */
.hero-banner {
    background: #172033;
    border: 1px solid #26344D;
    border-radius: 16px;
    padding: 26px 36px;
    margin-bottom: 24px;
    position: relative;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.hero-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    flex-wrap: wrap;
    gap: 12px;
}
.hero-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.hero-logo-icon {
    font-size: 2rem;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 6px 12px;
    border-radius: 12px;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}
.hero-title-blue {
    color: #3B82F6;
}
.ai-badge {
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.35);
    color: #A78BFA;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.hero-sub {
    color: #94A3B8;
    font-size: 0.95rem;
    margin: 4px 0 18px 0;
}

/* ── Workflow Progress Header ── */
.hero-flow {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.hf-step {
    background: #1D293D;
    border: 1px solid #26344D;
    color: #94A3B8;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.2s ease;
}
.hf-step-active {
    background: #3B82F6;
    color: #FFFFFF;
    border-color: #3B82F6;
    font-weight: 700;
    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.35);
}
.hf-step-done {
    background: rgba(34, 197, 94, 0.12);
    color: #22C55E;
    border: 1px solid rgba(34, 197, 94, 0.3);
    font-weight: 600;
}
.hf-arrow {
    color: #64748B;
    font-size: 0.85rem;
}

/* ── Section Headers ── */
.sec-hdr {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 18px;
    background: #172033;
    border: 1px solid #26344D;
    border-left: 4px solid #3B82F6;
    border-radius: 10px;
    margin: 20px 0 18px 0;
}
.sec-num {
    background: #3B82F6;
    color: #FFFFFF;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.sec-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F8FAFC;
}

/* ── Metric Cards ── */
.metric-card {
    background: #172033;
    border: 1px solid #26344D;
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
}
.metric-num {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.1;
}
.metric-lbl {
    color: #94A3B8;
    font-size: 0.82rem;
    margin-top: 6px;
    font-weight: 600;
}

/* ── Semantic Skill Tags ── */
.tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
.tag {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 5px 12px; border-radius: 20px;
    font-size: 0.80rem; font-weight: 600;
}
.tag-match  { background:rgba(34, 197, 94, 0.12);  color:#22C55E;  border:1px solid rgba(34, 197, 94, 0.35); }
.tag-miss   { background:rgba(245, 158, 11, 0.12);  color:#F59E0B;  border:1px solid rgba(245, 158, 11, 0.35); }
.tag-pri    { background:rgba(239, 68, 68, 0.12);   color:#EF4444;  border:1px solid rgba(239, 68, 68, 0.35); }
.tag-infer  { background:rgba(59, 130, 246, 0.12);  color:#60A5FA;  border:1px dashed rgba(59, 130, 246, 0.35); }

/* ── Cards & Containers ── */
.card {
    background: #172033;
    border: 1px solid #26344D;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}
.card-elevated {
    background: #1D293D;
    border: 1px solid #26344D;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}
.card-title {
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 10px;
}

/* ── Priority Gap Items ── */
.gap-item {
    border-radius: 10px; padding: 11px 16px; margin-bottom: 8px;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.3);
}
.gap-skill { color: #EF4444; font-weight: 700; font-size: 0.92rem; }

/* ── AI Recommendation Card (Violet) ── */
.rec-card {
    background: rgba(139, 92, 246, 0.06);
    border: 1px solid rgba(139, 92, 246, 0.28);
    border-radius: 10px; padding: 15px; margin-bottom: 9px;
}
.rec-skill { color: #A78BFA; font-weight: 700; font-size: 0.88rem; }
.rec-body  { color: #CBD5E1; font-size: 0.83rem; margin-top: 6px; line-height: 1.65; }

/* ── Challenge Card ── */
.ch-card {
    background: #172033;
    border: 1px solid #26344D;
    border-radius: 16px; padding: 24px; margin: 12px 0;
}
.ch-title { font-size: 1.4rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px; }
.diff-badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.76rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;
}
.diff-easy   { background:rgba(34, 197, 94, 0.15); color:#22C55E; border:1px solid rgba(34, 197, 94, 0.35); }
.diff-medium { background:rgba(245, 158, 11, 0.15); color:#F59E0B; border:1px solid rgba(245, 158, 11, 0.35); }
.diff-hard   { background:rgba(239, 68, 68, 0.15);  color:#EF4444; border:1px solid rgba(239, 68, 68, 0.35); }

.prob-body { color: #CBD5E1; font-size: 0.92rem; line-height: 1.75; }
.code-block {
    background: #0B1020; border: 1px solid #26344D; border-radius: 8px;
    padding: 13px 15px; font-family: 'Fira Code', monospace;
    font-size: 0.83rem; color: #F8FAFC; white-space: pre-wrap;
    overflow-x: auto; margin: 7px 0;
}
.sec-label {
    font-size: 0.78rem; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 0.06em; margin: 16px 0 6px 0;
}

/* ── Example Box ── */
.ex-box {
    background: #0B1020; border: 1px solid #26344D;
    border-radius: 10px; padding: 14px; margin: 8px 0;
}
.ex-label { color: #64748B; font-size: 0.72rem; font-weight: 700; margin-bottom: 5px; }
.ex-io { font-family:'Fira Code',monospace; font-size:0.81rem; white-space:pre; }
.ex-in  { color: #60A5FA; }
.ex-out { color: #22C55E; }
.ex-exp { color: #94A3B8; font-size: 0.78rem; margin-top: 8px; font-style: italic; }

/* ── Test Case Result Cards ── */
.tr {
    padding: 12px 16px; border-radius: 8px;
    margin-bottom: 8px; border-left: 4px solid;
    font-size: 0.86rem; background: #172033;
    border-right: 1px solid #26344D;
    border-top: 1px solid #26344D;
    border-bottom: 1px solid #26344D;
}
.tr-pass  { border-left-color:#22C55E; }
.tr-fail  { border-left-color:#EF4444; }
.tr-error { border-left-color:#F59E0B; }
.tr-tle   { border-left-color:#F59E0B; }
.tr-detail { color: #94A3B8; font-size: 0.8rem; margin-left: 8px; }

/* ── Score Card & Gauge ── */
.score-card {
    background: #172033;
    border: 1px solid #26344D;
    border-radius: 16px; padding: 26px 20px; text-align: center;
    height: 100%;
}
.sbar-bg { background:#0B1020; border-radius:8px; height:12px; overflow:hidden; margin:14px 0 6px 0; border: 1px solid #26344D; }
.sbar-fg { height:100%; border-radius:8px; transition:width 0.6s ease; }

/* ── AI Feedback Card (Violet SaaS Accent) ── */
.fb-card {
    background: linear-gradient(135deg, #13192B 0%, #1A1938 100%);
    border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 14px; padding: 22px;
    color: #F8FAFC; line-height: 1.7;
}

/* ── Info / Warning Boxes ── */
.ibox {
    background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: 10px; padding: 13px 17px; margin: 12px 0;
    color: #60A5FA; font-size: 0.88rem;
}
.wbox {
    background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 10px; padding: 13px 17px; margin: 12px 0;
    color: #F59E0B; font-size: 0.88rem;
}

/* ── Next Steps Cards ── */
.ns-card {
    background:#172033; border:1px solid #26344D;
    border-radius:12px; padding:20px; text-align:center;
    height: 130px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 6px;
}
.ns-icon { font-size:1.8rem; }
.ns-title { color:#F8FAFC; font-weight:700; font-size:0.9rem; }
.ns-sub   { color:#94A3B8; font-size:0.78rem; }

/* ── Divider ── */
.div { border:none; border-top:1px solid #26344D; margin:26px 0; }

/* ── Sidebar & Streamlit Overrides ── */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #26344D !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }

.stTextArea textarea {
    font-family: 'Fira Code', monospace !important; font-size: 0.84rem !important;
    background: #0B1020 !important; border: 1px solid #26344D !important;
    border-radius: 8px !important; color: #F8FAFC !important;
}
.stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

/* Primary Button: Electric Blue */
.stButton button[kind="primary"] {
    background-color: #3B82F6 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}
.stButton button[kind="primary"]:hover {
    background-color: #2563EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35) !important;
}

/* Secondary Button: Dark Slate */
.stButton button[kind="secondary"] {
    background-color: #172033 !important;
    color: #CBD5E1 !important;
    border: 1px solid #26344D !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}
.stButton button[kind="secondary"]:hover {
    background-color: #1D293D !important;
    color: #F8FAFC !important;
    border-color: #3B82F6 !important;
}
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
def _init_state() -> None:
    defaults = {
        "step": 1,
        "max_unlocked": 1,
        "resume_text": "",
        "jd_text": "",
        "skill_analysis": None,
        "selected_gap": "REST APIs",
        "challenge": None,
        "user_code": "",
        "test_run_output": None,
        "evaluation": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "")
    try:
        key = key or st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    return key.strip()


def _ensure_data_and_analysis() -> None:
    """Helper to auto-fill sample data & skill analysis if missing when jumping to steps."""
    if not st.session_state.resume_text.strip() or not st.session_state.jd_text.strip():
        st.session_state.resume_text = load_sample_resume()
        st.session_state.jd_text = load_sample_jd()

    if not st.session_state.skill_analysis:
        st.session_state.skill_analysis = analyze_skills(
            st.session_state.resume_text, st.session_state.jd_text
        )


def _ensure_challenge() -> None:
    """Helper to auto-generate challenge if missing when jumping to steps 3 or 4."""
    _ensure_data_and_analysis()
    if not st.session_state.challenge:
        an = st.session_state.skill_analysis
        priority = (an.get("priority_gaps") or an.get("missing_skills") or ["REST APIs"])
        gap = st.session_state.selected_gap or priority[0]
        st.session_state.selected_gap = gap
        st.session_state.challenge = generate_challenge(gap, st.session_state.jd_text)

    if not st.session_state.user_code and st.session_state.challenge:
        st.session_state.user_code = st.session_state.challenge.get(
            "starter_code", "# Write your solution here\n"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _sec(num: int, title: str) -> None:
    st.markdown(
        f'<div class="sec-hdr">'
        f'<div class="sec-num">{num}</div>'
        f'<div class="sec-title">{title}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _tag(label: str, cls: str) -> str:
    return f'<span class="tag {cls}">{label}</span>'


def _diff_badge(diff: str) -> str:
    cls = f"diff-{diff.lower()}"
    return f'<span class="diff-badge {cls}">{diff}</span>'


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
def _sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center;padding:16px 0 14px;">'
            '<div style="font-size:2.4rem;display:inline-block;background:rgba(59,130,246,0.15);padding:6px 14px;border-radius:12px;border:1px solid rgba(59,130,246,0.3);">🌉</div>'
            '<div style="font-size:1.45rem;font-weight:800;color:#F8FAFC;margin-top:8px;">SkillBridge</div>'
            '<div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">Employability Gap Engine</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='color:#94A3B8;font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;'>Workflow Steps</div>", unsafe_allow_html=True)
        steps = [
            (1, "Input Resume & JD", "📄"),
            (2, "Skill Gap Analysis", "🔍"),
            (3, "Coding Challenge", "🎯"),
            (4, "Write & Run Code", "💻"),
            (5, "Evaluation & Feedback", "🏆"),
        ]

        current = st.session_state.step

        for num, label, icon in steps:
            is_active = (num == current)
            is_completed = (num < current or (num == 2 and st.session_state.skill_analysis) or
                            (num == 3 and st.session_state.challenge) or
                            (num == 5 and st.session_state.evaluation))

            badge_text = "▶ Active" if is_active else ("✅ Done" if is_completed else f"Step {num}")
            btn_label = f"{icon} {num}. {label}"

            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{btn_label} ({badge_text})", key=f"side_nav_{num}",
                         use_container_width=True, type=btn_type):
                if num >= 2:
                    _ensure_data_and_analysis()
                if num >= 3:
                    _ensure_challenge()
                if num == 5 and not st.session_state.evaluation:
                    with st.spinner("⚙️ Running evaluation on your solution…"):
                        test_cases = st.session_state.challenge.get("test_cases", [])
                        st.session_state.evaluation = evaluate_code(
                            st.session_state.user_code,
                            test_cases,
                            skill=st.session_state.selected_gap or "coding",
                        )

                st.session_state.step = num
                st.session_state.max_unlocked = max(st.session_state.max_unlocked, num)
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📋 Load Sample Data", use_container_width=True,
                     help="Pre-fill with sample resume (Priya Sharma) + job description"):
            st.session_state.resume_text = load_sample_resume()
            st.session_state.jd_text = load_sample_jd()
            _ensure_data_and_analysis()
            st.toast("✅ Sample data loaded! Explore any step.", icon="📋")
            st.rerun()

        if current > 1 or st.session_state.skill_analysis:
            if st.button("🔄 Start Over", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        api_key = _get_api_key()
        if api_key:
            st.success("✅ Gemini AI Active", icon="🤖")
            st.caption("Full AI-powered skill extraction & challenge synthesis")
        else:
            st.info("💡 Demo Mode (No API Key)", icon="🔧")
            st.caption("Using pre-built GFG challenges & heuristic analysis. Add `GEMINI_API_KEY` to `.env` for AI mode.")

        st.markdown(
            '<div style="text-align:center;padding:16px 0 0;color:#64748B;font-size:0.7rem;">'
            'Built for GFG Hackathon<br>Python · Streamlit · Gemini AI · Pyodide'
            '</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — INPUT
# ═══════════════════════════════════════════════════════════════════════════════
def _step1() -> None:
    _sec(1, "Resume & Job Description Input")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### 📄 Your Resume")
        uploaded = st.file_uploader("Upload (.txt)", type=["txt"],
                                     key="resume_upload", label_visibility="collapsed")
        if uploaded:
            st.session_state.resume_text = uploaded.read().decode("utf-8", errors="ignore")

        new_val = st.text_area(
            "resume",
            value=st.session_state.resume_text,
            height=330,
            placeholder="Paste your resume here…\n\nOr click '📋 Load Sample Data' in the sidebar →",
            key="resume_ta",
            label_visibility="collapsed",
        )
        if new_val != st.session_state.resume_text:
            st.session_state.resume_text = new_val

    with col2:
        st.markdown("#### 💼 Job Description")
        uploaded = st.file_uploader("Upload (.txt)", type=["txt"],
                                     key="jd_upload", label_visibility="collapsed")
        if uploaded:
            st.session_state.jd_text = uploaded.read().decode("utf-8", errors="ignore")

        new_val = st.text_area(
            "jd",
            value=st.session_state.jd_text,
            height=330,
            placeholder="Paste the job description here…\n\nOr click '📋 Load Sample Data' in the sidebar →",
            key="jd_ta",
            label_visibility="collapsed",
        )
        if new_val != st.session_state.jd_text:
            st.session_state.jd_text = new_val

    st.markdown("<br>", unsafe_allow_html=True)
    ready = bool(st.session_state.resume_text.strip() and st.session_state.jd_text.strip())

    c_left, c_btn, c_right = st.columns([1, 2, 1])
    with c_btn:
        if st.button("🔍 Analyze Skill Gap →", use_container_width=True,
                     disabled=not ready, type="primary"):
            with st.spinner("🤖 Analyzing your skills against the job requirements…"):
                st.session_state.skill_analysis = analyze_skills(
                    st.session_state.resume_text,
                    st.session_state.jd_text,
                )
            st.session_state.step = 2
            st.session_state.max_unlocked = max(st.session_state.max_unlocked, 2)
            st.rerun()
        if not ready:
            st.caption("👈 Click '📋 Load Sample Data' in sidebar to quickly test the app")


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — SKILL GAP ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def _step2() -> None:
    _ensure_data_and_analysis()
    an = st.session_state.skill_analysis
    if not an:
        st.warning("Please input a resume and JD first.")
        return

    _sec(2, "Skill Gap Analysis")

    mode = an.get("mode", "fallback")
    if mode == "llm":
        st.success("✨ Analysis powered by Gemini 1.5 Flash", icon="🤖")
    else:
        st.info("📊 Keyword-based analysis (Demo Mode) — add a Gemini API key for AI-powered results", icon="💡")

    # ── Metric row ──
    mp = an.get("match_percentage", 0)
    matched = an.get("matched_skills", [])
    missing = an.get("missing_skills", [])
    priority = an.get("priority_gaps", []) or missing or ["REST APIs"]

    if mp >= 70:
        sc = "#22C55E"
    elif mp >= 40:
        sc = "#F59E0B"
    else:
        sc = "#EF4444"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-num" style="color:{sc};">{mp}%</div>'
            f'<div class="metric-lbl">Match Score</div></div>',
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            '<div class="metric-card">'
            f'<div class="metric-num" style="color:#22C55E;">{len(matched)}</div>'
            '<div class="metric-lbl">Skills Matched</div></div>',
            unsafe_allow_html=True)
    with c3:
        st.markdown(
            '<div class="metric-card">'
            f'<div class="metric-num" style="color:#F59E0B;">{len(missing)}</div>'
            '<div class="metric-lbl">Skills Missing</div></div>',
            unsafe_allow_html=True)
    with c4:
        st.markdown(
            '<div class="metric-card">'
            f'<div class="metric-num" style="color:#EF4444;">{len(priority)}</div>'
            '<div class="metric-lbl">Priority Gaps</div></div>',
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skills breakdown ──
    cl, cr = st.columns(2, gap="large")
    with cl:
        # Matched
        matched_tags = "".join(_tag(f"✓ {s}", "tag-match") for s in matched)
        st.markdown(
            '<div class="card">'
            '<div class="card-title" style="color:#22C55E;">✅ Matched Skills</div>'
            f'<div class="tags">{matched_tags or "<span style=\'color:#94A3B8\'>None found</span>"}</div>'
            '</div>',
            unsafe_allow_html=True)

        # Your profile
        rs = an.get("resume_skills", [])
        explicit_tags = "".join(_tag(s["skill"], "tag-match") for s in rs if s.get("source") == "explicit")
        inferred_tags = "".join(_tag(s["skill"], "tag-infer") for s in rs if s.get("source") == "inferred")
        st.markdown(
            '<div class="card">'
            '<div class="card-title" style="color:#60A5FA;">📄 Your Skills Profile</div>'
            '<div style="font-size:0.75rem;color:#94A3B8;margin-bottom:8px;">🟢 Explicit &nbsp;·&nbsp; 🔵 Inferred from context</div>'
            f'<div class="tags">{explicit_tags}{inferred_tags}</div>'
            '</div>',
            unsafe_allow_html=True)

    with cr:
        if missing:
            pri_set = set(priority)
            miss_tags = "".join(
                _tag(f"⚡ {s}", "tag-pri") if s in pri_set else _tag(f"✗ {s}", "tag-miss")
                for s in missing
            )
            st.markdown(
                '<div class="card">'
                '<div class="card-title" style="color:#F59E0B;">⚡ Skill Gaps &amp; Requirements</div>'
                '<div style="font-size:0.75rem;color:#94A3B8;margin-bottom:8px;">🔴 Critical Gap &nbsp;·&nbsp; 🟡 Missing Skill</div>'
                f'<div class="tags">{miss_tags}</div>'
                '</div>',
                unsafe_allow_html=True)

            # JD skills
            js = an.get("jd_skills", [])
            jd_tags = "".join(
                _tag(s["skill"], "tag-match" if s["source"] == "explicit" else "tag-infer")
                for s in js
            )
            st.markdown(
                '<div class="card">'
                '<div class="card-title" style="color:#A78BFA;">💼 JD Requirements</div>'
                f'<div class="tags">{jd_tags}</div>'
                '</div>',
                unsafe_allow_html=True)
        else:
            st.success("🎉 Great news! You appear to have all the key required skills.")

    # ── Priority Gaps & AI Recommendations ──
    if priority:
        st.markdown('<hr class="div">', unsafe_allow_html=True)
        cp, cr2 = st.columns([1, 2], gap="large")

        with cp:
            st.markdown("#### 🎯 Priority Skill Gaps")
            rank_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            for i, gap in enumerate(priority[:5]):
                icon = rank_icons[i] if i < len(rank_icons) else "📌"
                st.markdown(
                    f'<div class="gap-item">'
                    f'<span class="gap-skill">{icon} {gap}</span>'
                    f'</div>',
                    unsafe_allow_html=True)

        with cr2:
            recs = an.get("recommendations", {})
            st.markdown("#### 🤖 AI Actionable Recommendations")
            for gap, rec in list(recs.items())[:4]:
                st.markdown(
                    f'<div class="rec-card">'
                    f'<div class="rec-skill">✨ {gap}</div>'
                    f'<div class="rec-body">{rec}</div>'
                    f'</div>',
                    unsafe_allow_html=True)

    # ── Generate Challenge CTA ──
    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Select a Skill Gap to Generate Challenge")

    csel, cgen = st.columns([2, 1], gap="large")
    with csel:
        options_list = priority if priority else (missing if missing else ["REST APIs", "FastAPI", "SQL", "Docker"])
        default_idx = 0
        if st.session_state.selected_gap in options_list:
            default_idx = options_list.index(st.session_state.selected_gap)

        sel = st.selectbox(
            "Target skill gap:",
            options=options_list,
            index=default_idx,
            key="gap_select",
        )
        if sel:
            st.session_state.selected_gap = sel

    with cgen:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Generate Coding Challenge →", type="primary", use_container_width=True):
            gap = st.session_state.selected_gap or options_list[0]
            with st.spinner(f"✨ Crafting a personalized GFG challenge for **{gap}**…"):
                ch = generate_challenge(gap, st.session_state.jd_text)
            st.session_state.challenge = ch
            st.session_state.user_code = ch.get("starter_code", "# Write your solution here\n")
            st.session_state.step = 3
            st.session_state.max_unlocked = max(st.session_state.max_unlocked, 3)
            st.rerun()

    # ── Step Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2 = st.columns([1, 1])
    with n1:
        if st.button("⬅️ Back to Step 1: Input", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with n2:
        if st.button("Next: Step 3 (Coding Challenge) ➡️", use_container_width=True):
            _ensure_challenge()
            st.session_state.step = 3
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — CHALLENGE DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def _step3() -> None:
    _ensure_challenge()
    ch = st.session_state.challenge
    if not ch:
        st.warning("Unable to load coding challenge. Please try again.")
        return

    _sec(3, "Your Personalized Coding Challenge")

    gen_by = ch.get("generated_by", "fallback")
    if gen_by == "llm":
        st.success("✨ Challenge uniquely generated by Gemini AI based on your skill gaps", icon="🤖")
    else:
        st.info("📚 Pre-built challenge from SkillBridge library — target skill: " + str(ch.get("skill_tested", "Backend")), icon="💡")

    diff = ch.get("difficulty", "Medium")
    skill = ch.get("skill_tested", st.session_state.selected_gap or "Backend")

    st.markdown(
        f'<div class="ch-card">'
        f'<div class="ch-title">📝 {ch.get("title","Coding Challenge")}</div>'
        f'{_diff_badge(diff)}'
        f'<span style="color:#94A3B8;font-size:0.8rem;margin-left:10px;">🎯 Target Skill: {skill}</span>'
        f'</div>',
        unsafe_allow_html=True)

    c_prob, c_io = st.columns([3, 2], gap="large")

    with c_prob:
        st.markdown('<div class="sec-label">📋 Problem Statement</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="background:#172033;border:1px solid #26344D;border-radius:10px;'
            f'padding:18px;color:#F8FAFC;line-height:1.8;font-size:0.92rem;">'
            f'{ch.get("problem_statement","").replace(chr(10),"<br>")}'
            f'</div>',
            unsafe_allow_html=True)
        if ch.get("constraints"):
            st.markdown('<div class="sec-label">⚙️ Constraints</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="code-block">{ch["constraints"]}</div>', unsafe_allow_html=True)

    with c_io:
        st.markdown('<div class="sec-label">📥 Input Format</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="code-block">{ch.get("input_format","Standard stdin")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-label">📤 Output Format</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="code-block">{ch.get("output_format","Standard stdout")}</div>', unsafe_allow_html=True)

        examples = ch.get("examples", [])
        if examples:
            st.markdown('<div class="sec-label">💡 Example</div>', unsafe_allow_html=True)
            ex = examples[0]
            exp_html = f'<div class="ex-exp">{ex["explanation"]}</div>' if ex.get("explanation") else ""
            st.markdown(
                f'<div class="ex-box">'
                f'<div class="ex-label">INPUT</div>'
                f'<div class="ex-io ex-in">{ex.get("input","")}</div>'
                f'<div class="ex-label" style="margin-top:10px;">EXPECTED OUTPUT</div>'
                f'<div class="ex-io ex-out">{ex.get("output","")}</div>'
                f'{exp_html}'
                f'</div>',
                unsafe_allow_html=True)

    tc_count = len(ch.get("test_cases", []))
    st.markdown(
        f'<div class="ibox">🧪 This challenge has <strong>{tc_count} hidden test cases</strong>. '
        f'Click "Start Coding" to write your solution in the browser editor and evaluate against test cases.</div>',
        unsafe_allow_html=True)

    c_c1, c_c2 = st.columns([1, 2])
    with c_c2:
        if st.button("💻 Start Coding & Live Editor →", type="primary", use_container_width=True):
            st.session_state.user_code = st.session_state.user_code or ch.get("starter_code", "# Solution\n")
            st.session_state.step = 4
            st.session_state.max_unlocked = max(st.session_state.max_unlocked, 4)
            st.rerun()

    # ── Step Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2 = st.columns([1, 1])
    with n1:
        if st.button("⬅️ Back to Step 2: Skill Analysis", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with n2:
        if st.button("Next: Step 4 (Write & Run Code) ➡️", use_container_width=True):
            st.session_state.user_code = st.session_state.user_code or ch.get("starter_code", "# Solution\n")
            st.session_state.step = 4
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — CODE EDITOR & RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def _step4() -> None:
    _ensure_challenge()
    ch = st.session_state.challenge
    if not ch:
        st.warning("No challenge loaded. Please select a challenge in Step 3.")
        return

    _sec(4, "Write & Run Your Code")

    starter = ch.get("starter_code", "# Write your Python solution here\n")
    if not st.session_state.user_code:
        st.session_state.user_code = starter

    c_prob, c_ed = st.columns([1, 1], gap="large")

    with c_prob:
        st.markdown("#### 📋 Problem Quick Reference")
        st.markdown(f"**{ch.get('title','Challenge')}** (`{ch.get('difficulty','Medium')}`)")
        st.markdown(f'<div class="prob-body">{ch.get("problem_statement","")}</div>', unsafe_allow_html=True)

        examples = ch.get("examples", [])
        for i, ex in enumerate(examples[:2], 1):
            st.markdown(
                f'<div style="background:#172033;border:1px solid #26344D;border-radius:10px;padding:13px;margin-bottom:9px;">'
                f'<div style="color:#60A5FA;font-size:0.74rem;font-weight:700;margin-bottom:6px;">EXAMPLE {i}</div>'
                f'<div style="color:#94A3B8;font-size:0.68rem;font-weight:700;">INPUT:</div>'
                f'<div style="font-family:Fira Code,monospace;color:#60A5FA;font-size:0.8rem;white-space:pre;margin:3px 0 8px;">{ex.get("input","")}</div>'
                f'<div style="color:#94A3B8;font-size:0.68rem;font-weight:700;">EXPECTED OUTPUT:</div>'
                f'<div style="font-family:Fira Code,monospace;color:#22C55E;font-size:0.8rem;white-space:pre;margin:3px 0;">{ex.get("output","")}</div>'
                f'</div>',
                unsafe_allow_html=True)

    with c_ed:
        st.markdown("#### 🐍 Live Interactive Editor (Pyodide)")
        editor_html = get_pyodide_editor_html(
            starter_code=st.session_state.user_code or starter,
            problem_title=ch.get("title", "Challenge"),
        )
        st.components.v1.html(editor_html, height=460, scrolling=False)

    # ── Code Input & Execution ──
    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown("#### 📝 Code Submission & Testing")

    code_val = st.text_area(
        "Python Code Solution:",
        value=st.session_state.user_code or starter,
        height=260,
        key="sub_code_input",
        placeholder="Paste or write your Python solution here…",
    )
    if code_val != st.session_state.user_code:
        st.session_state.user_code = code_val

    ca, cb, cc = st.columns([1, 1, 1])

    test_cases = ch.get("test_cases", [])
    sample_input = examples[0].get("input", "") if examples else (test_cases[0].get("input", "") if test_cases else "")

    with ca:
        if st.button("▶ Run Quick Code Test", use_container_width=True):
            with st.spinner("⏳ Running Python code..."):
                run_res = execute_code(st.session_state.user_code, stdin_input=sample_input)
                st.session_state.test_run_output = run_res

    with cb:
        if st.button("🚀 Evaluate Solution →", type="primary", use_container_width=True):
            if not test_cases:
                st.error("No test cases available for evaluation.")
            else:
                with st.spinner("⚙️ Running official test cases…"):
                    eval_res = evaluate_code(
                        st.session_state.user_code,
                        test_cases,
                        skill=st.session_state.selected_gap or "coding",
                    )
                st.session_state.evaluation = eval_res
                st.session_state.step = 5
                st.session_state.max_unlocked = max(st.session_state.max_unlocked, 5)
                st.rerun()

    with cc:
        if st.button("🔄 Reset Code to Starter", use_container_width=True):
            st.session_state.user_code = starter
            st.session_state.test_run_output = None
            st.rerun()

    if st.session_state.test_run_output:
        st.markdown("##### 🖥️ Execution Output (Sample Input)")
        tro = st.session_state.test_run_output
        if tro.get("error"):
            st.error(f"Execution Error:\n{tro['error']}")
        else:
            st.markdown(f"**Output (stdout):**\n```text\n{tro['stdout'] or '(no output)'}\n```")
            if tro.get("stderr"):
                st.warning(f"**Stderr:**\n```text\n{tro['stderr']}\n```")

    # ── Step Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2 = st.columns([1, 1])
    with n1:
        if st.button("⬅️ Back to Step 3: Coding Challenge", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    with n2:
        if st.button("Next: Step 5 (Evaluation & Feedback) ➡️", use_container_width=True):
            if not st.session_state.evaluation:
                with st.spinner("⚙️ Running evaluation on your solution…"):
                    st.session_state.evaluation = evaluate_code(
                        st.session_state.user_code,
                        test_cases,
                        skill=st.session_state.selected_gap or "coding",
                    )
            st.session_state.step = 5
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 5 — EVALUATION RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def _step5() -> None:
    _ensure_challenge()
    if not st.session_state.evaluation:
        test_cases = st.session_state.challenge.get("test_cases", [])
        st.session_state.evaluation = evaluate_code(
            st.session_state.user_code,
            test_cases,
            skill=st.session_state.selected_gap or "coding",
        )

    ev = st.session_state.evaluation
    _sec(5, "Evaluation Results & AI Feedback")

    score   = ev["score"]
    passed  = ev["passed"]
    total   = ev["total"]
    results = ev["results"]

    if score == 100:
        sc, se, sm = "#22C55E", "🏆", "Perfect Score!"
    elif score >= 70:
        sc, se, sm = "#3B82F6", "👏", "Great Job!"
    elif score >= 40:
        sc, se, sm = "#F59E0B", "💪", "Keep Going!"
    else:
        sc, se, sm = "#EF4444", "📚", "Keep Practicing!"

    cs, cd = st.columns([1, 2], gap="large")

    with cs:
        bar_bg = "#22C55E" if score == 100 else ("#3B82F6" if score >= 70 else ("#F59E0B" if score >= 40 else "#EF4444"))

        st.markdown(
            f'<div class="score-card">'
            f'<div style="font-size:2.4rem;">{se}</div>'
            f'<div style="font-size:3.6rem;font-weight:800;color:{sc};line-height:1.1;">{score}%</div>'
            f'<div style="color:{sc};font-weight:700;font-size:0.95rem;margin-top:4px;">{sm}</div>'
            f'<div style="color:#94A3B8;font-size:0.82rem;margin-top:8px;">{passed} / {total} tests passed</div>'
            f'<div class="sbar-bg">'
            f'<div class="sbar-fg" style="width:{score}%;background:{bar_bg};"></div></div>'
            f'</div>',
            unsafe_allow_html=True)

    with cd:
        st.markdown("#### 🧪 Test Case Results")
        for r in results:
            status = r["status"]
            n = r["test_case"]
            if status == "PASS":
                icon, cls, st_color = "✅", "tr-pass", "#22C55E"
                detail = f'Output: <code>{r["actual"][:70].replace(chr(10),"↵")}</code>'
            elif status == "FAIL":
                icon, cls, st_color = "❌", "tr-fail", "#EF4444"
                exp = r["expected"][:55].replace(chr(10), "↵")
                act = (r["actual"] or "(empty)")[:55].replace(chr(10), "↵")
                detail = f'Expected: <code>{exp}</code> &nbsp;·&nbsp; Got: <code>{act}</code>'
            elif status == "ERROR":
                icon, cls, st_color = "🔴", "tr-error", "#F59E0B"
                err = ((r.get("error") or "Unknown error").split("\n")[-1])[:110]
                detail = f'<code>{err}</code>'
            else:  # TLE
                icon, cls, st_color = "⏱️", "tr-tle", "#F59E0B"
                detail = "Time Limit Exceeded (10 s) — optimize your algorithm"

            st.markdown(
                f'<div class="tr {cls}">'
                f'<span style="font-weight:700;color:{st_color};">{icon} Test {n}</span>'
                f'<span class="tr-detail">{detail}</span>'
                f'</div>',
                unsafe_allow_html=True)

    # ── AI Feedback (Violet Accent) ──
    if ev.get("feedback"):
        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown("#### 🤖 AI Feedback & Improvement Tips")
        feedback_html = ev["feedback"].replace("\n", "<br>")
        st.markdown(
            f'<div class="fb-card">{feedback_html}</div>',
            unsafe_allow_html=True)

    # ── What's Next ──
    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown("#### 🚀 What's Next?")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Try a Different Solution", use_container_width=True):
            st.session_state.evaluation = None
            st.session_state.step = 4
            st.rerun()
    with c2:
        if st.button("🎯 Practice Another Skill Gap", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with c3:
        if st.button("📄 Start New Analysis", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # ── Step Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2 = st.columns([1, 1])
    with n1:
        if st.button("⬅️ Back to Step 4: Code Editor", use_container_width=True):
            st.session_state.step = 4
            st.rerun()
    with n2:
        if st.button("🔄 Restart Workflow from Step 1", use_container_width=True):
            st.session_state.step = 1
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    _init_state()
    _sidebar()

    # ── Redesigned SkillBridge Header ──
    step_num = st.session_state.step

    def _step_cls(n: int) -> str:
        if n == step_num:
            return "hf-step hf-step-active"
        elif n < step_num or (n == 2 and st.session_state.skill_analysis) or (n == 3 and st.session_state.challenge):
            return "hf-step hf-step-done"
        else:
            return "hf-step"

    st.markdown(
        f'<div class="hero-banner">'
        f'<div class="hero-header-row">'
        f'<div class="hero-brand">'
        f'<div class="hero-logo-icon">🌉</div>'
        f'<div>'
        f'<h1 class="hero-title">SkillBridge <span class="hero-title-blue">Engine</span></h1>'
        f'<div class="hero-sub">Employability Gap Analyzer &amp; Custom Assessment Platform</div>'
        f'</div>'
        f'</div>'
        f'<div class="ai-badge">🤖 AI-POWERED PLATFORM</div>'
        f'</div>'
        f'<div class="hero-flow">'
        f'<span class="{_step_cls(1)}">📄 1. Input</span><span class="hf-arrow">→</span>'
        f'<span class="{_step_cls(2)}">🔍 2. Gap Analysis</span><span class="hf-arrow">→</span>'
        f'<span class="{_step_cls(3)}">🎯 3. Challenge</span><span class="hf-arrow">→</span>'
        f'<span class="{_step_cls(4)}">💻 4. Write &amp; Run</span><span class="hf-arrow">→</span>'
        f'<span class="{_step_cls(5)}">🏆 5. Evaluation</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    current_step = st.session_state.step
    if current_step == 1:
        _step1()
    elif current_step == 2:
        _step2()
    elif current_step == 3:
        _step3()
    elif current_step == 4:
        _step4()
    elif current_step == 5:
        _step5()


if __name__ == "__main__":
    main()
