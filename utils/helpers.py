"""
utils/helpers.py
Utility functions for SkillBridge: sample data loaders, Pyodide HTML generator.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ─── Sample Data Loaders ────────────────────────────────────────────────────

def load_sample_resume() -> str:
    """Load the sample resume from the data directory."""
    try:
        return (DATA_DIR / "sample_resume.txt").read_text(encoding="utf-8")
    except FileNotFoundError:
        return _DEFAULT_RESUME


def load_sample_jd() -> str:
    """Load the sample job description from the data directory."""
    try:
        return (DATA_DIR / "sample_jd.txt").read_text(encoding="utf-8")
    except FileNotFoundError:
        return _DEFAULT_JD


_DEFAULT_RESUME = """PRIYA SHARMA | B.Tech CSE, IIT Delhi | 2024
SKILLS: Python, C, C++, MySQL (Basic SQL), Data Structures, Algorithms, Git, OOP
PROJECTS: Student Grade Management System (Python, MySQL), Data Structures Library
EDUCATION: B.Tech CSE CGPA 8.2 (2020-2024)
CERTIFICATIONS: Python Basics (Coursera), Introduction to Databases (edX)"""

_DEFAULT_JD = """SOFTWARE ENGINEER - BACKEND (INTERNSHIP)
REQUIRED: Python, SQL, REST API development, FastAPI, Data Structures & Algorithms,
Problem Solving, Git. GOOD TO HAVE: Docker, JWT, AWS, pytest."""


# ─── Pyodide Editor HTML Generator ──────────────────────────────────────────

def get_pyodide_editor_html(starter_code: str, problem_title: str = "Challenge") -> str:
    """
    Generate a self-contained HTML page with:
    - CodeMirror editor (Python syntax highlighting, Dracula theme)
    - Pyodide runtime for in-browser Python execution
    - Run button, Clear button, output panel
    """
    starter_code_json = json.dumps(starter_code)  # Properly escaped for JS embedding

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SkillBridge Editor</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css">
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      background:#1e1e2e; color:#cdd6f4;
      font-family:'Fira Code','Courier New',monospace;
      height:100vh; overflow:hidden;
      display:flex; flex-direction:column;
    }}
    .toolbar {{
      background:#181825; padding:7px 14px;
      display:flex; justify-content:space-between; align-items:center;
      border-bottom:1px solid #313244; flex-shrink:0;
      min-height: 40px;
    }}
    .toolbar-left {{ display:flex; align-items:center; gap:10px; }}
    .lang-badge {{
      background:#313244; color:#a6e3a1;
      font-size:0.72rem; padding:3px 9px;
      border-radius:4px; font-weight:700; letter-spacing:0.04em;
    }}
    .editor-subtitle {{ color:#585b70; font-size:0.75rem; }}
    #pyodide-status {{ font-size:0.75rem; color:#f9e2af; }}
    .btn {{
      border:none; padding:5px 14px; border-radius:6px;
      cursor:pointer; font-weight:700; font-size:0.78rem;
      font-family:inherit; transition:all 0.2s;
    }}
    .btn-run {{ background:#a6e3a1; color:#1e1e2e; }}
    .btn-run:hover:not(:disabled) {{ background:#94e2d5; transform:scale(1.03); }}
    .btn-clear {{ background:#313244; color:#cdd6f4; margin-right:6px; }}
    .btn-clear:hover {{ background:#45475a; }}
    .btn:disabled {{ background:#313244; color:#585b70; cursor:not-allowed; transform:none !important; }}
    .editor-wrapper {{ flex:1; overflow:hidden; min-height:0; }}
    .CodeMirror {{ height:100% !important; font-size:0.85rem; line-height:1.55; }}
    .output-panel {{
      background:#11111b; border-top:1px solid #313244;
      padding:9px 14px; max-height:135px; min-height:80px;
      overflow-y:auto; flex-shrink:0;
    }}
    .out-header {{ color:#585b70; font-size:0.7rem; font-weight:700; letter-spacing:0.07em; margin-bottom:5px; text-transform:uppercase; }}
    #output {{ font-size:0.82rem; line-height:1.6; white-space:pre-wrap; word-break:break-word; }}
    .out-normal {{ color:#cdd6f4; }}
    .out-error {{ color:#f38ba8; }}
    .out-info {{ color:#89b4fa; font-style:italic; }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div class="toolbar-left">
      <span class="lang-badge">🐍 Python</span>
      <span class="editor-subtitle">Pyodide In-Browser Runtime · Ctrl+Enter to Run</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <span id="pyodide-status">⏳ Loading Pyodide...</span>
      <button class="btn btn-clear" onclick="clearOutput()">⌫ Clear</button>
      <button class="btn btn-run" id="run-btn" onclick="runCode()" disabled>▶ Run</button>
    </div>
  </div>

  <div class="editor-wrapper">
    <textarea id="editor-area"></textarea>
  </div>

  <div class="output-panel">
    <div class="out-header">▸ Output</div>
    <div id="output"><span class="out-info">Click ▶ Run or press Ctrl+Enter to execute your code...</span></div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/matchbrackets.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closebrackets.min.js"></script>
  <script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>

  <script>
    const STARTER = {starter_code_json};

    const cm = CodeMirror.fromTextArea(document.getElementById('editor-area'), {{
      mode: 'python',
      theme: 'dracula',
      lineNumbers: true,
      matchBrackets: true,
      autoCloseBrackets: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      extraKeys: {{
        "Ctrl-Enter": () => runCode(),
        "Cmd-Enter": () => runCode(),
        "Tab": (cm) => {{
          if (cm.somethingSelected()) cm.indentSelection("add");
          else cm.replaceSelection("    ");
        }}
      }}
    }});
    cm.setValue(STARTER);

    let pyodide = null;
    (async () => {{
      try {{
        pyodide = await loadPyodide();
        document.getElementById('pyodide-status').textContent = '✅ Ready';
        document.getElementById('pyodide-status').style.color = '#a6e3a1';
        document.getElementById('run-btn').disabled = false;
      }} catch (e) {{
        document.getElementById('pyodide-status').textContent = '❌ Failed – use Evaluate below';
        document.getElementById('pyodide-status').style.color = '#f38ba8';
      }}
    }})();

    async function runCode() {{
      if (!pyodide) return;
      const btn = document.getElementById('run-btn');
      btn.disabled = true; btn.textContent = '⏳ Running...';
      const outputDiv = document.getElementById('output');
      outputDiv.innerHTML = '<span class="out-info">Running...</span>';

      const code = cm.getValue();
      let lines = [];

      pyodide.setStdout({{ batched: (t) => lines.push(esc(t)) }});
      pyodide.setStderr({{ batched: (t) => lines.push('<span class="out-error">' + esc(t) + '</span>') }});

      try {{
        await pyodide.runPythonAsync(code);
        const out = lines.join('').trim();
        outputDiv.innerHTML = out
          ? '<span class="out-normal">' + out + '</span>'
          : '<span class="out-info">(no output)</span>';
      }} catch (e) {{
        outputDiv.innerHTML = '<span class="out-error">' + esc(e.message) + '</span>';
      }}
      btn.disabled = false; btn.textContent = '▶ Run';
    }}

    function clearOutput() {{
      document.getElementById('output').innerHTML = '<span class="out-info">Cleared.</span>';
    }}

    function esc(s) {{
      return String(s)
        .replace(/&/g,'&amp;').replace(/</g,'&lt;')
        .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }}
  </script>
</body>
</html>"""
