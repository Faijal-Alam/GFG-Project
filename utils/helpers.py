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
    - Deep Navy & Electric Blue developer styling
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
      background:#172033; color:#F8FAFC;
      font-family:'Fira Code','Courier New',monospace;
      height:100vh; overflow:hidden;
      display:flex; flex-direction:column;
      border:1px solid #26344D; border-radius:12px;
    }}
    .toolbar {{
      background:#111827; padding:8px 16px;
      display:flex; justify-content:space-between; align-items:center;
      border-bottom:1px solid #26344D; flex-shrink:0;
      min-height: 42px;
    }}
    .toolbar-left {{ display:flex; align-items:center; gap:10px; }}
    .lang-badge {{
      background:rgba(59,130,246,0.15); color:#60A5FA;
      font-size:0.75rem; padding:3px 10px; border:1px solid rgba(59,130,246,0.3);
      border-radius:6px; font-weight:700; letter-spacing:0.04em;
    }}
    .editor-subtitle {{ color:#94A3B8; font-size:0.75rem; }}
    #pyodide-status {{ font-size:0.75rem; color:#F59E0B; font-weight:600; }}
    .btn {{
      border:none; padding:6px 14px; border-radius:6px;
      cursor:pointer; font-weight:700; font-size:0.78rem;
      font-family:inherit; transition:all 0.2s;
    }}
    .btn-run {{ background:#3B82F6; color:#FFFFFF; }}
    .btn-run:hover:not(:disabled) {{ background:#2563EB; transform:scale(1.02); }}
    .btn-clear {{ background:#1F293D; color:#CBD5E1; border:1px solid #26344D; margin-right:6px; }}
    .btn-clear:hover {{ background:#26344D; }}
    .btn:disabled {{ background:#1F293D; color:#64748B; cursor:not-allowed; transform:none !important; }}
    .editor-wrapper {{ flex:1; overflow:hidden; min-height:0; background:#0B1020; }}
    .CodeMirror {{ height:100% !important; font-size:0.85rem; line-height:1.55; background:#0B1020 !important; }}
    .output-panel {{
      background:#0B1020; border-top:1px solid #26344D;
      padding:10px 16px; max-height:135px; min-height:85px;
      overflow-y:auto; flex-shrink:0;
    }}
    .out-header {{ color:#64748B; font-size:0.7rem; font-weight:700; letter-spacing:0.07em; margin-bottom:5px; text-transform:uppercase; }}
    #output {{ font-size:0.82rem; line-height:1.6; white-space:pre-wrap; word-break:break-word; }}
    .out-normal {{ color:#F8FAFC; }}
    .out-error {{ color:#EF4444; }}
    .out-info {{ color:#94A3B8; font-style:italic; }}
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
        document.getElementById('pyodide-status').style.color = '#22C55E';
        document.getElementById('run-btn').disabled = false;
      }} catch (e) {{
        document.getElementById('pyodide-status').textContent = '❌ Failed – use Evaluate below';
        document.getElementById('pyodide-status').style.color = '#EF4444';
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
        outputDiv.innerHTML = lines.length ? lines.join('<br>') : '<span class="out-info">(Code executed with no output)</span>';
      }} catch (err) {{
        outputDiv.innerHTML = '<span class="out-error">' + esc(err.toString()) + '</span>';
      }} finally {{
        btn.disabled = false; btn.textContent = '▶ Run';
      }}
    }}

    function clearOutput() {{
      document.getElementById('output').innerHTML = '<span class="out-info">Output cleared.</span>';
    }}

    function esc(s) {{
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }}
  </script>
</body>
</html>"""
