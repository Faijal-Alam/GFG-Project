<<<<<<< HEAD
# GFG-Project
=======
# 🚀 SkillBridge: Employability Gap Analyzer & Custom Coding Assessment Engine

> **GFG Hackathon Solution** | Empowering students to bridge the gap between academic/current skills and industry job requirements.

---

## 🌟 Overview

**SkillBridge** is an end-to-end EdTech solution designed to solve the **employability gap** for tech students and job seekers. By comparing a candidate's resume against a target job description (JD), SkillBridge provides actionable insights and generates **personalized GeeksforGeeks (GFG)-style coding challenges** specifically tailored to address the candidate's missing or priority skill gaps.

### Key Features
1. 📄 **Resume vs. Job Description Analysis**: Upload or paste resumes and target job descriptions.
2. 🤖 **AI-Powered Skill Gap Extraction**: Identifies matching skills, inferred skills, missing skills, and overall match percentage using LLMs (with fallback to robust keyword matching).
3. 🎯 **Targeted GFG-Style Challenge Generation**: Generates customized coding problems (with problem statement, input/output specifications, constraints, example test cases, and hidden test cases) targeting missing tech skills.
4. 💻 **Interactive In-Browser Code Editor**: Run Python code with real-time execution in Streamlit or through an embedded IDE experience.
5. 📊 **Instant Evaluation & Feedback**: Evaluates code against multiple hidden test cases, returning scores, pass/fail breakdowns, performance analysis, and actionable AI feedback.

---

## 🛠️ Architecture & Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/) with custom dark theme CSS and interactive web components.
- **LLM Engine**: Google Gemini API (`gemini-1.5-flash` / `gemini-1.5-pro`) for high-quality NLP extraction, problem generation, and detailed feedback synthesis.
- **Code Execution**: Python server-side isolated execution engine with timeout bounds and standard output capturing.
- **Fallback Engine**: Pre-packaged GFG coding challenges and heuristic skill extractors ensuring 100% functionality even without an API key or when offline.

---

## 📁 Repository Structure

```
GFG-Project/
├── app.py                     # Main Streamlit App entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .streamlit/
│   └── config.toml            # Streamlit visual theme configuration
├── components/
│   ├── skill_analyzer.py      # LLM + Keyword skill comparison logic
│   ├── challenge_generator.py # Personalized GFG challenge generator
│   └── code_evaluator.py      # Server-side Python sandbox execution & test runner
├── data/
│   ├── sample_resume.txt      # Pre-loaded candidate resume (Priya Sharma)
│   ├── sample_jd.txt          # Pre-loaded Job Description (Backend Engineer)
│   └── fallback_challenges.json# Curated pre-built GFG challenges for demo mode
└── utils/
    └── helpers.py             # Pyodide script generator, UI components, data loaders
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9 or higher installed.

### 1. Clone & Install Dependencies
```bash
# Clone the repository (or navigate to directory)
cd GFG-Project

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)
Copy `.env.example` to `.env` and add your Google Gemini API Key if available:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> 💡 *Note: If no API key is provided, SkillBridge automatically runs in **Demo Mode**, utilizing curated heuristic matching and pre-built interactive GFG coding challenges.*

### 3. Launch the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 🎯 How to Use (Demo Walkthrough)

1. **Upload / Select Input**: Select **"Use Pre-loaded Sample Data (Priya Sharma - Backend)"** from the sidebar or paste custom text.
2. **Analyze Skills**: Click **"⚡ Analyze Skill Gap"**. View the Match Score, Explicit/Inferred skills, Missing Skills, and targeted recommendations.
3. **Generate Challenge**: Click **"🚀 Generate Personalized GFG Challenge"**. Choose a target skill gap (e.g., *REST APIs*, *SQL*, *Docker*, *FastAPI*).
4. **Code Solution**: Write your Python solution in the code editor, test with sample input, or run against hidden test cases.
5. **Submit & Review**: Click **"⚡ Run Test Cases & Evaluate"** to view test results, overall score, execution time, and AI feedback.

---

## 🏆 Hackathon Value Proposition

- **Direct Impact**: Solves the mismatch between university curricula and real-world tech requirements.
- **GFG Ecosystem Synergy**: Enhances GFG's learning portal by transforming passive job matching into active assessment and targeted skill building.
- **Resilient Design**: Zero dependency lock-in with seamless fallback mechanisms, ensuring high availability during live demos.
>>>>>>> 9beba54 (Initial commit: SkillBridge - Employability Gap Analyzer & Custom Coding Assessment Engine)
