"""
Generate LMS-ready HTML files for each course (02-21).
Combines handout overview + full lesson content into one HTML per course.
Run: python scripts/gen_lms_html.py
"""

import re
import sys
from pathlib import Path

import markdown

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
COURSES_DIR = PROJECT_DIR / "Detailed Course Content"
HANDOUTS_DIR = PROJECT_DIR / "Handouts"
LMS_DIR = HANDOUTS_DIR / "LMS"

# Course metadata keyed by number
COURSE_META = {
    2:  ("The Context Architect", "Teaching Claude Your Role, Categories, and Data"),
    3:  ("The Skill Builder", "Saving RFP and Bid-Scoring Methods as Reusable Templates"),
    4:  ("The Command Engineer", "One-Line Commands for Monthly Spend and Anomaly Reports"),
    5:  ("The Orchestrator", "Scoring 50 Suppliers in Parallel with Sub-Agents"),
    6:  ("The Guardian", "Auto-Checking Contracts and Outputs Before They Save"),
    7:  ("The Pipeline Automator", "Overnight Spend Scans with Slack Alerts"),
    8:  ("The Project Architect", "Giving Claude Memory Across Sessions for Savings Programs"),
    9:  ("The Integration Architect", "Connecting Claude to Live ERP and Spend Data"),
    10: ("The Negotiation Intelligence System", "Full Contract Prep from Intel to Counter-Proposal"),
    11: ("The Category Management System", "Quarterly Reviews Across All Categories at Once"),
    12: ("The Team Deployment Architect", "Rolling Out Claude to Your Procurement Team with Audit Trails"),
    13: ("Contract Intelligence", "Extracting Terms, Mapping Obligations, and Tracking Renewals"),
    14: ("Supplier Lifecycle Management", "Onboarding, Risk Alerts, and Exit Planning for 30 Suppliers"),
    15: ("Purchase to Pay Intelligence", "Approval Checks, Three-Way Match, and Maverick Spend Detection"),
    16: ("Sourcing Sprint", "Running an RFP from Category Analysis to Award Recommendation"),
    17: ("Market Intelligence", "Commodity Tracking, Demand Consolidation, and Sourcing Briefs"),
    18: ("Savings Program Management", "Validating $12M in Claims and Writing the CFO Memo"),
    19: ("Supply Chain Risk", "Single-Source Mapping, Disruption Scenarios, and Board Briefs"),
    20: ("ESG and Sustainable Procurement", "Scope 3 Estimates, Supplier Scores, and Action Plans"),
    21: ("Compliance, Policy, and Audit Readiness", "Encoding Rules, Scanning Transactions, and Packaging Evidence"),
}

CHAPTER_MAP = {
    2: (1, "S2P Foundation"), 3: (1, "S2P Foundation"), 4: (1, "S2P Foundation"),
    5: (2, "S2P Architecture"), 6: (2, "S2P Architecture"), 7: (2, "S2P Architecture"), 8: (2, "S2P Architecture"),
    9: (3, "S2P Integration"), 10: (3, "S2P Integration"), 11: (3, "S2P Integration"), 12: (3, "S2P Integration"),
    13: (4, "Upstream Procurement"), 14: (4, "Upstream Procurement"), 16: (4, "Upstream Procurement"), 17: (4, "Upstream Procurement"),
    15: (5, "Downstream and Governance"), 18: (5, "Downstream and Governance"), 19: (5, "Downstream and Governance"),
    20: (5, "Downstream and Governance"), 21: (5, "Downstream and Governance"),
}

CSS = """
  body {
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 24px;
    background: #ffffff;
  }
  .course-header {
    text-align: center;
    border-bottom: 3px solid #1a3a5c;
    padding-bottom: 24px;
    margin-bottom: 36px;
  }
  .course-header .brand {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: #6b7280;
    margin-bottom: 4px;
  }
  .course-header .academy {
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #1a3a5c;
    margin-bottom: 2px;
  }
  .course-header .series {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 12px;
  }
  .course-header h1 {
    font-size: 30px;
    font-weight: 700;
    color: #1a3a5c;
    margin: 8px 0 4px 0;
    letter-spacing: -0.5px;
    border: none;
    padding: 0;
  }
  .course-header .subtitle {
    font-size: 16px;
    color: #4b5563;
    font-style: italic;
    margin-bottom: 8px;
  }
  .course-header .meta {
    font-size: 14px;
    color: #6b7280;
  }

  /* Table of contents */
  .toc {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px 28px;
    margin: 24px 0 36px 0;
  }
  .toc h2 {
    margin-top: 0;
    font-size: 18px;
    color: #1a3a5c;
    border: none;
  }
  .toc ol {
    margin: 0;
    padding-left: 20px;
  }
  .toc li {
    margin-bottom: 6px;
  }
  .toc a {
    color: #2563eb;
    text-decoration: none;
  }
  .toc a:hover {
    text-decoration: underline;
  }

  /* Headings */
  h1 {
    font-size: 24px;
    font-weight: 700;
    color: #1a3a5c;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 8px;
    margin-top: 48px;
    margin-bottom: 16px;
  }
  h2 {
    font-size: 19px;
    font-weight: 600;
    color: #1e40af;
    margin-top: 32px;
    margin-bottom: 12px;
  }
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin-top: 24px;
    margin-bottom: 8px;
  }
  p { margin: 0 0 14px 0; }
  ul, ol { margin: 0 0 14px 0; padding-left: 24px; }
  li { margin-bottom: 6px; }

  /* Lesson containers */
  .lesson {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 28px 32px;
    margin: 32px 0;
    background: #fafbfc;
  }
  .lesson-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 2px solid #2563eb;
  }
  .lesson-number {
    background: #1a3a5c;
    color: #fff;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
    flex-shrink: 0;
  }
  .lesson-title {
    font-size: 20px;
    font-weight: 700;
    color: #1a3a5c;
    margin: 0;
  }
  .lesson-time {
    font-size: 13px;
    color: #6b7280;
    margin-left: auto;
    white-space: nowrap;
  }

  /* Code blocks */
  pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px 20px;
    border-radius: 8px;
    font-family: 'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace;
    font-size: 13.5px;
    line-height: 1.6;
    overflow-x: auto;
    margin: 12px 0 16px 0;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  code {
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace;
    font-size: 13.5px;
  }
  pre code {
    background: none;
    color: inherit;
    padding: 0;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 20px 0;
    font-size: 14px;
  }
  thead th {
    background: #1a3a5c;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 10px 14px;
  }
  tbody td {
    border: 1px solid #d1d5db;
    padding: 10px 14px;
    vertical-align: top;
  }
  tbody tr:nth-child(even) { background: #f8fafc; }

  /* Callout boxes */
  .what-you-see {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
  }
  .troubleshooting {
    background: #fffbeb;
    border-left: 4px solid #d97706;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
  }
  .behind-the-scenes {
    background: #faf5ff;
    border-left: 4px solid #7c3aed;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
  }
  .done-check {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
  }

  /* Separator between sections */
  hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 32px 0;
  }
"""


def find_course_dir(course_num):
    """Find the Detailed Course Content folder for a given course number."""
    pattern = f"Course_{course_num:02d}_*"
    matches = list(COURSES_DIR.glob(pattern))
    return matches[0] if matches else None


def get_lesson_files(course_dir):
    """Return lesson .md files sorted by lesson number."""
    lessons_dir = course_dir / "lessons"
    if not lessons_dir.exists():
        return []
    files = list(lessons_dir.glob("Lesson_*.md"))
    # Sort by the numeric part after Lesson_
    def sort_key(f):
        m = re.search(r'Lesson_(\d+)', f.name)
        return int(m.group(1)) if m else 99
    return sorted(files, key=sort_key)


def extract_lesson_time(md_text):
    """Extract the time estimate from the lesson markdown."""
    m = re.search(r'\*\*Time:\*\*\s*(.+?)\.?\s*$', md_text, re.MULTILINE)
    return m.group(1).strip().rstrip('.') if m else ""


def extract_lesson_title(md_text):
    """Extract the H1 title from the lesson markdown."""
    m = re.match(r'#\s+(.+)', md_text.strip())
    return m.group(1).strip() if m else "Untitled Lesson"


def md_to_html(md_text):
    """Convert markdown to HTML with fenced code blocks and tables."""
    return markdown.markdown(
        md_text,
        extensions=['fenced_code', 'tables', 'sane_lists'],
        output_format='html5',
    )


def post_process_lesson_html(html_text):
    """Add styling classes to known patterns in the converted HTML."""
    # Wrap "What you should see" paragraphs
    html_text = re.sub(
        r'<p><strong>What you should see\.?</strong>(.+?)</p>',
        r'<div class="what-you-see"><strong>What you should see.</strong>\1</div>',
        html_text,
        flags=re.DOTALL,
    )
    # Wrap "What Claude Code did" sections
    html_text = re.sub(
        r'<p><strong>What Claude Code did,? behind the scenes\.?</strong></p>',
        r'<div class="behind-the-scenes"><strong>What Claude Code did, behind the scenes.</strong></div>',
        html_text,
    )
    # Wrap troubleshooting / "if you see" patterns
    html_text = re.sub(
        r'<p><strong>If you see',
        r'<div class="troubleshooting"><strong>If you see',
        html_text,
    )
    # Wrap "You are done with Lesson" sections
    html_text = re.sub(
        r'<h2>You are done with Lesson',
        r'<div class="done-check"><h2>You are done with Lesson',
        html_text,
    )
    return html_text


def _is_tree_or_code_line(text):
    """Return True if text looks like a folder tree or terminal command."""
    tree_chars = ('├', '└', '│', '─')
    if any(c in text for c in tree_chars):
        return True
    # Lines that look like a folder path with / at end
    if re.match(r'^[A-Za-z_][A-Za-z0-9_\-]*/\s*$', text.split('\n')[0]):
        return True
    # Terminal prompts
    if re.match(r'^(cd |claude\s*$|ls\s*$|> |mkdir |python |#\s)', text):
        return True
    return False


def _escape_html(text):
    """Escape HTML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def get_handout_overview(course_num):
    """Extract overview sections from the handout .docx (sections 1-4 roughly)."""
    try:
        from docx import Document
        pattern = f"Course_{course_num:02d}_*Handout*.docx"
        matches = list(HANDOUTS_DIR.glob(pattern))
        if not matches:
            return ""
        doc = Document(str(matches[0]))

        # First pass: collect raw paragraphs with metadata
        raw = []
        current_section = 0
        for p in doc.paragraphs:
            if p.style.name == "Heading 1":
                current_section += 1
                if current_section > 4:
                    break
                raw.append(("h1", p.text.strip(), p.style.name))
            elif 1 <= current_section <= 4:
                text = p.text.strip()
                if not text:
                    continue
                raw.append(("para", text, p.style.name))

        # Second pass: group consecutive tree/code lines into <pre> blocks
        parts = []
        i = 0
        while i < len(raw):
            kind, text, style = raw[i]

            if kind == "h1":
                parts.append(f"<h2>{text}</h2>")
                i += 1
                continue

            if _is_tree_or_code_line(text):
                # Collect consecutive tree/code lines
                pre_lines = []
                while i < len(raw) and raw[i][0] == "para" and _is_tree_or_code_line(raw[i][1]):
                    pre_lines.append(raw[i][1])
                    i += 1
                parts.append(f"<pre><code>{_escape_html(chr(10).join(pre_lines))}</code></pre>")
                continue

            if style == "Heading 2":
                parts.append(f"<h3>{text}</h3>")
            elif style == "Heading 3":
                parts.append(f"<h3>{text}</h3>")
            elif style and "List" in style:
                parts.append(f"<li>{text}</li>")
            else:
                parts.append(f"<p>{text}</p>")
            i += 1

        return "\n".join(parts)
    except Exception as e:
        print(f"  Warning: could not read handout for Course {course_num:02d}: {e}")
        return ""


def build_toc(lesson_titles):
    """Build an HTML table of contents."""
    items = []
    for i, title in enumerate(lesson_titles, 1):
        # Clean the title (remove "Lesson N:" prefix if present)
        clean = re.sub(r'^Lesson\s+\d+:\s*', '', title)
        items.append(f'<li><a href="#lesson-{i}">Lesson {i}: {clean}</a></li>')
    return f"""
<div class="toc">
  <h2>Course Contents</h2>
  <ol>
    {"".join(items)}
  </ol>
</div>
"""


def build_course_html(course_num):
    """Build the complete LMS HTML for one course."""
    name, subtitle = COURSE_META[course_num]
    ch_num, ch_name = CHAPTER_MAP[course_num]

    course_dir = find_course_dir(course_num)
    if not course_dir:
        print(f"  SKIP: no course dir for Course {course_num:02d}")
        return None

    lesson_files = get_lesson_files(course_dir)
    if not lesson_files:
        print(f"  SKIP: no lesson files for Course {course_num:02d}")
        return None

    # Read all lessons
    lessons = []
    for lf in lesson_files:
        md_text = lf.read_text(encoding="utf-8")
        title = extract_lesson_title(md_text)
        time_est = extract_lesson_time(md_text)
        # Remove the H1 line and Time line from the body (we render them in the header)
        body = re.sub(r'^#\s+.+\n+', '', md_text.strip(), count=1)
        body = re.sub(r'\*\*Time:\*\*\s*.+\n*', '', body, count=1)
        html_body = md_to_html(body.strip())
        html_body = post_process_lesson_html(html_body)
        lessons.append({
            "num": len(lessons) + 1,
            "title": title,
            "time": time_est,
            "html": html_body,
        })

    # Get handout overview
    overview_html = get_handout_overview(course_num)

    # Build TOC
    toc_html = build_toc([l["title"] for l in lessons])

    # Count total lesson words (rough)
    total_words = sum(len(lf.read_text(encoding="utf-8").split()) for lf in lesson_files)

    # Build lesson sections
    lesson_sections = []
    for l in lessons:
        time_badge = f'<span class="lesson-time">{l["time"]}</span>' if l["time"] else ""
        # Clean the title
        clean_title = re.sub(r'^Lesson\s+\d+:\s*', '', l["title"])
        lesson_sections.append(f"""
<div class="lesson" id="lesson-{l['num']}">
  <div class="lesson-header">
    <div class="lesson-number">{l['num']}</div>
    <div class="lesson-title">{clean_title}</div>
    {time_badge}
  </div>
  {l['html']}
</div>
""")

    # Assemble full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Course {course_num:02d}: {name}</title>
<style>{CSS}</style>
</head>
<body>

<div class="course-header">
  <div class="brand">U2xAI</div>
  <div class="academy">PROCUREAI ACADEMY</div>
  <div class="series">Chapter {ch_num}: {ch_name} | Course {course_num:02d}</div>
  <h1>{name}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="meta">{len(lessons)} lessons | ~{total_words:,} words | Complete course with step-by-step activities</div>
</div>

{toc_html}

{"<h1>Course Overview</h1>" + overview_html if overview_html else ""}

<hr>
<h1>Lessons</h1>
<p>Work through each lesson in order. Every lesson has a scenario, step-by-step instructions, and a "done when" checklist at the end.</p>

{"".join(lesson_sections)}

<hr>
<div class="done-check">
<h2>Course Complete</h2>
<p>You have finished all {len(lessons)} lessons of <strong>{name}</strong>. Review any lesson you want to revisit, then move to the next course in the series.</p>
</div>

</body>
</html>
"""
    return html


def main():
    LMS_DIR.mkdir(parents=True, exist_ok=True)
    course_nums = sorted(COURSE_META.keys())
    generated = 0
    for cn in course_nums:
        print(f"Generating Course {cn:02d}...", end=" ")
        html = build_course_html(cn)
        if html is None:
            continue
        name = re.sub(r'[^A-Za-z0-9_]', '_', COURSE_META[cn][0].replace(" ", "_"))
        name = re.sub(r'_+', '_', name).strip('_')
        out_path = LMS_DIR / f"Course_{cn:02d}_{name}_LMS.html"
        out_path.write_text(html, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        print(f"OK ({size_kb:.0f} KB)")
        generated += 1
    print(f"\nDone. Generated {generated} LMS HTML files in {LMS_DIR}")


if __name__ == "__main__":
    main()
