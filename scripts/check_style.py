"""Style and structure linter for course content.

Enforces the language AND structural rules in the course CLAUDE.md:

Style rules (checked on every save):
- no em-dashes or en-dashes
- no banned AI tells
- no banned procurement filler
- no vague figure phrases ("significant savings" etc)
- no AI-style openers or closers
- no British spellings (aluminium, organisation, etc.)
- no GBP / pound references (USD and US context required)

Structural rules (checked on handout/lesson .md and .docx files):
- every section must have at least one code block (terminal example)
- Day in the Life must NOT be a course lesson walkthrough
- worked examples must have four parts (prompt, folder, what you see, behind the scenes)
- rhetorical questions must not open sections

Modes:
    python scripts/check_style.py <file>       lint one file by path
    python scripts/check_style.py --hook        read tool-use JSON from stdin
    python scripts/check_style.py --all         lint all .md and .docx in project

Exit codes:
    0   clean
    1   internal error
    2   violations found (used by PostToolUse hook to block Claude)

The script is deliberately defensive: any unexpected condition exits 0
(silent pass) so a misbehaving hook never blocks unrelated work.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable, List, Tuple

# ---------------------------------------------------------------------------
# Paths where the rules are *defined* (so banned words appearing here are not
# violations, they are the rule book itself). The linter skips these.
# ---------------------------------------------------------------------------

SKIP_PATH_FRAGMENTS = (
    "/CLAUDE.md",
    "\\CLAUDE.md",
    "/docs/",
    "\\docs\\",
    "/scripts/",
    "\\scripts\\",
    "/.claude/",
    "\\.claude\\",
    "/MEMORY.md",
    "\\MEMORY.md",
    "/memory/",
    "\\memory\\",
)


# ---------------------------------------------------------------------------
# Style rules
# ---------------------------------------------------------------------------

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# Each entry: (regex, label).
# Patterns are matched case-insensitive against full lines/paragraphs.
BANNED_PATTERNS: List[Tuple[str, str]] = [
    # General AI tells
    (r"\bdive into\b",                 "AI tell: 'dive into'"),
    (r"\bdelv\w+\b",                   "AI tell: 'delve' family"),
    (r"\bunlock\b",                    "AI tell: 'unlock'"),
    (r"\bunleash\b",                   "AI tell: 'unleash'"),
    (r"\bsupercharge\b",              "AI tell: 'supercharge'"),
    (r"\bharness\b",                   "AI tell: 'harness'"),
    (r"\bleverage\b",                  "AI tell: 'leverage'"),
    (r"\belevate\b",                   "AI tell: 'elevate'"),
    (r"\bempower\b",                   "AI tell: 'empower'"),
    (r"\brevoluti(?:s|z)e\w*\b",       "AI tell: 'revolutionise'"),
    (r"\bgame[- ]changer\b",          "AI tell: 'game-changer'"),
    (r"\bcutting[- ]edge\b",          "AI tell: 'cutting-edge'"),
    (r"\bstate[- ]of[- ]the[- ]art\b", "AI tell: 'state-of-the-art'"),
    (r"\bseamless(?:ly)?\b",          "AI tell: 'seamless'"),
    (r"\brobust(?:ly)?\b",            "AI tell: 'robust'"),
    (r"\bholistic(?:ally)?\b",        "AI tell: 'holistic'"),
    (r"\bsynerg(?:y|ies|ic|istic)\b", "AI tell: 'synergy/synergies'"),
    (r"\bin today'?s fast-paced\b",   "AI tell: 'in today's fast-paced ...'"),
    (r"\bever-evolving\b",            "AI tell: 'ever-evolving'"),
    (r"\bin the realm of\b",          "AI tell: 'in the realm of'"),
    (r"\bit'?s important to note that\b", "AI tell: 'it's important to note that'"),
    (r"\bit'?s worth mentioning\b",   "AI tell: 'it's worth mentioning'"),
    (r"\bneedless to say\b",          "AI tell: 'needless to say'"),
    (r"\bwhether you'?re a beginner or an expert\b",
                                       "AI tell: false-inclusivity opener"),
    # Procurement-specific filler
    (r"\bholistic approach\b",         "Procurement filler: 'holistic approach'"),
    (r"\brobust framework\b",         "Procurement filler: 'robust framework'"),
    (r"\bdeep dive\b",                "Procurement filler: 'deep dive'"),
    # Vague figure phrases
    (r"\bsignificant savings\b",       "Vague figure: 'significant savings' (use a number)"),
    (r"\bmaterial reduction\b",        "Vague figure: 'material reduction' (use a number)"),
    (r"\bconsiderable improvement\b", "Vague figure: 'considerable improvement' (use a number)"),
    (r"\bmeaningful uplift\b",        "Vague figure: 'meaningful uplift' (use a number)"),
    (r"\bstep change\b",              "Vague figure: 'step change' (use a number)"),
    # AI greetings/closers (only at the start or end of a paragraph)
    (r"^(?:Certainly|Absolutely|Great question)!",
                                       "AI opener: 'Certainly! / Absolutely! / Great question!'"),
    (r"\bI hope this helps\b",        "AI closer: 'I hope this helps'"),
    (r"\bLet me know if you have any other questions\b",
                                       "AI closer: 'Let me know if you have any other questions'"),
]

# British spellings that should be American English
BRITISH_SPELLING_PATTERNS: List[Tuple[str, str]] = [
    (r"\baluminium\b",                "British spelling: 'aluminium' -> 'aluminum'"),
    (r"\borganise[ds]?\b",           "British spelling: 'organise' -> 'organize'"),
    (r"\bsummarise[ds]?\b",          "British spelling: 'summarise' -> 'summarize'"),
    (r"\banalyse[ds]?\b",            "British spelling: 'analyse' -> 'analyze'"),
    (r"\bbehaviour\b",               "British spelling: 'behaviour' -> 'behavior'"),
    (r"\bcolour\b",                  "British spelling: 'colour' -> 'color'"),
    (r"\bcentre\b",                  "British spelling: 'centre' -> 'center'"),
    (r"\bprogramme\b",               "British spelling: 'programme' -> 'program'"),
    (r"\brecognise[ds]?\b",          "British spelling: 'recognise' -> 'recognize'"),
    (r"\bminimise[ds]?\b",           "British spelling: 'minimise' -> 'minimize'"),
    (r"\bmaximise[ds]?\b",           "British spelling: 'maximise' -> 'maximize'"),
    (r"\bcustomise[ds]?\b",          "British spelling: 'customise' -> 'customize'"),
    (r"\bpersonalise[ds]?\b",        "British spelling: 'personalise' -> 'personalize'"),
    (r"\blabelled\b",                "British spelling: 'labelled' -> 'labeled'"),
    (r"\bcatalogue\b",               "British spelling: 'catalogue' -> 'catalog'"),
    (r"\bartefact\b",                "British spelling: 'artefact' -> 'artifact'"),
    (r"\bmemorise[ds]?\b",           "British spelling: 'memorise' -> 'memorize'"),
    (r"\bgalvanised\b",              "British spelling: 'galvanised' -> 'galvanized'"),
    (r"\banodising\b",               "British spelling: 'anodising' -> 'anodizing'"),
    (r"\bmoulding\b",                "British spelling: 'moulding' -> 'molding'"),
    (r"\bPrioritised\b",             "British spelling: 'Prioritised' -> 'Prioritized'"),
]

# Currency and geography violations
CURRENCY_GEO_PATTERNS: List[Tuple[str, str]] = [
    (r"\bGBP\b",                     "Currency: use USD, not GBP"),
    (r"\xa3\d",                      "Currency: use $ not pound sign"),
    (r"\b_gbp\b",                    "Column name: use _usd, not _gbp"),
    (r"\bAcme Plc\b",               "Company: use 'Acme Inc', not 'Acme Plc'"),
    (r"\bBritish English\b",         "Language: use 'American English', not 'British English'"),
]


# ---------------------------------------------------------------------------
# Reading text out of supported file types
# ---------------------------------------------------------------------------

def _open_docx_with_retry(file_path: Path, attempts: int = 4, delay_s: float = 0.5):
    """Open a .docx, retrying briefly when a sync client holds the lock."""
    from docx import Document  # type: ignore

    last_exc: Exception | None = None
    for _ in range(attempts):
        try:
            return Document(str(file_path))
        except (PermissionError, OSError) as exc:
            last_exc = exc
            time.sleep(delay_s)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            break
    raise last_exc if last_exc else RuntimeError("unknown docx open failure")


def read_text_lines(file_path: Path) -> List[Tuple[int, str]]:
    """Return [(line_or_para_number, text), ...] for a supported file."""
    suffix = file_path.suffix.lower()
    if suffix in (".md", ".txt"):
        try:
            with file_path.open("r", encoding="utf-8", errors="replace") as f:
                return [(i + 1, line.rstrip("\n")) for i, line in enumerate(f)]
        except OSError as exc:
            print(f"check_style.py: cannot read {file_path}: {exc}", file=sys.stderr)
            return []
    if suffix == ".docx":
        try:
            from docx import Document  # noqa: F401
        except ImportError:
            print(
                "check_style.py: python-docx not installed; cannot lint .docx",
                file=sys.stderr,
            )
            return []
        try:
            d = _open_docx_with_retry(file_path)
        except Exception as exc:  # noqa: BLE001
            print(
                f"check_style.py: cannot open {file_path} after retry: {exc}. "
                f"If OneDrive is syncing or Word has the file open, pause sync "
                f"or close Word and re-run this lint.",
                file=sys.stderr,
            )
            return []
        out: List[Tuple[int, str]] = []
        n = 0
        for p in d.paragraphs:
            n += 1
            if p.text.strip():
                out.append((n, p.text))
        for t in d.tables:
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        n += 1
                        if p.text.strip():
                            out.append((n, p.text))
        return out
    return []


def read_full_text(file_path: Path) -> str:
    """Return the full text of a file as a single string for structural checks."""
    lines = read_text_lines(file_path)
    return "\n".join(text for _, text in lines)


# ---------------------------------------------------------------------------
# Style checks (line-by-line)
# ---------------------------------------------------------------------------

# Lines that are *teaching* the rules legitimately mention banned words.
RULE_CONTEXT_PATTERNS = [
    re.compile(r"^\s*(?:never use|do not use|don'?t use|banned\s*(?:words?|phrases?|terms?)?|stop using|avoid|words?\s+to\s+avoid|forbidden|disallowed)\s*[:\-]", re.I),
    re.compile(r"\binstead of\s+['\"]?\$?\d", re.I),
    re.compile(r"\b(?:not|rather than)\s+['\"][^'\"]+['\"]", re.I),
    re.compile(r"\b(?:phrases?|things?|words?|terms?)\s+like\b", re.I),
    re.compile(r"\bmark(?:s|ed)?\s+the output as AI", re.I),
]


def is_rule_context_line(text: str) -> bool:
    return any(rx.search(text) for rx in RULE_CONTEXT_PATTERNS)


def find_style_violations(
    lines: Iterable[Tuple[int, str]],
) -> List[Tuple[int, str]]:
    """Return [(line_number, message), ...] for any style rule hits."""
    violations: List[Tuple[int, str]] = []
    compiled_banned = [(re.compile(pat, re.IGNORECASE | re.MULTILINE), label)
                       for pat, label in BANNED_PATTERNS]
    compiled_british = [(re.compile(pat, re.IGNORECASE), label)
                        for pat, label in BRITISH_SPELLING_PATTERNS]
    compiled_currency = [(re.compile(pat, re.IGNORECASE), label)
                         for pat, label in CURRENCY_GEO_PATTERNS]

    for ln, text in lines:
        # Em-dash and en-dash checks always apply
        if EM_DASH in text:
            violations.append((ln, f"em-dash (U+2014) found: {snippet(text)}"))
        if EN_DASH in text:
            violations.append((ln, f"en-dash (U+2013) found: {snippet(text)}"))

        # British spellings always apply
        for rx, label in compiled_british:
            if rx.search(text):
                violations.append((ln, f"{label}: {snippet(text)}"))

        # Currency/geo always apply
        for rx, label in compiled_currency:
            if rx.search(text):
                violations.append((ln, f"{label}: {snippet(text)}"))

        # Banned-phrase checks skip lines that are teaching the rules
        if is_rule_context_line(text):
            continue
        for rx, label in compiled_banned:
            if rx.search(text):
                violations.append((ln, f"{label}: {snippet(text)}"))
    return violations


# ---------------------------------------------------------------------------
# Structural checks (whole-file)
# ---------------------------------------------------------------------------

def find_structural_violations(
    file_path: Path,
    lines: List[Tuple[int, str]],
) -> List[Tuple[int, str]]:
    """Check structural rules from CLAUDE.md. Only applies to handout and
    lesson files (not solutions, scripts, starters, or CLAUDE.md files)."""
    violations: List[Tuple[int, str]] = []
    fname = file_path.name.lower()
    fstr = str(file_path).lower()

    # Only check handout/lesson content files
    is_handout = "handout" in fname
    is_lesson = "lesson" in fname and fname.endswith(".md")
    is_course_overview = "course_overview" in fname
    # Skip solution files, build scripts, starter files, CSVs
    if not (is_handout or is_lesson or is_course_overview):
        return []

    full_text = "\n".join(text for _, text in lines)
    all_text_lower = full_text.lower()

    # ---- Check 1: Lessons must open with a day-to-day scenario ----
    if is_lesson:
        # First 10 lines after the title should contain a time/scenario marker
        first_chunk = "\n".join(text for _, text in lines[:15]).lower()
        scenario_markers = ["it is", "your cpo", "you open", "your inbox",
                           "you sit", "the cpo", "morning", "afternoon",
                           "tuesday", "wednesday", "thursday", "friday", "monday"]
        has_scenario = any(m in first_chunk for m in scenario_markers)
        if not has_scenario:
            violations.append((1,
                "STRUCTURE: Lesson must open with a day-to-day scenario "
                "(e.g., 'It is 09:30 Tuesday. Your CPO Slacks...'). "
                "Found no scenario marker in the opening."))

    # ---- Check 2: Day in the Life must NOT be a course walkthrough ----
    if is_handout:
        # Find the Day in the Life section
        ditl_start = None
        ditl_text = ""
        for i, (ln, text) in enumerate(lines):
            if re.search(r"day in the life|day-in-the-life", text, re.I):
                ditl_start = i
            if ditl_start is not None:
                ditl_text += text + "\n"
                # Stop at the next top-level heading or after ~200 lines
                if i > ditl_start + 3 and re.match(r"^(?:\d+\.|#\s)", text):
                    if not re.search(r"day in the life", text, re.I):
                        break
                if i > ditl_start + 200:
                    break

        if ditl_start is not None and ditl_text:
            ditl_lower = ditl_text.lower()
            # Count lesson-walkthrough indicators
            lesson_refs = len(re.findall(r"\blesson \d\b", ditl_lower))
            if lesson_refs >= 4:
                violations.append((lines[ditl_start][0],
                    f"STRUCTURE: Day in the Life references 'Lesson N' {lesson_refs} times. "
                    "This reads like a course walkthrough, not a real analyst workday. "
                    "CLAUDE.md requires genuine procurement scenarios (CPO deadline, "
                    "new bids arriving, CFO rule change, etc.), not lesson-by-lesson narration."))

    # ---- Check 3: Handout sections need code blocks (terminal examples) ----
    if is_handout:
        # Parse sections (lines starting with a number and period, or heading markers)
        sections: List[Tuple[str, int, int]] = []
        current_section = None
        current_start = 0
        for i, (ln, text) in enumerate(lines):
            # Detect section headings (e.g., "2. What this course teaches" or "# Section")
            if re.match(r"^\d+\.\s+\w", text) or re.match(r"^#{1,2}\s+\d+\.", text):
                if current_section:
                    sections.append((current_section, current_start, i))
                current_section = text.strip()
                current_start = i
        if current_section:
            sections.append((current_section, current_start, len(lines)))

        # Check each section for code blocks
        for sec_name, start, end in sections:
            # Skip meta sections (how to use, done checklist, troubleshooting)
            skip_patterns = ["how to use", "you are done", "troubleshooting",
                           "quick reference", "first week", "pattern:"]
            if any(p in sec_name.lower() for p in skip_patterns):
                continue
            sec_text = "\n".join(text for _, text in lines[start:end])
            # Look for code block indicators
            has_code = bool(re.search(
                r"```|cd\s+[\"']|claude\b.*\n|^\s*>|terminal|type this|type:|prompt:",
                sec_text, re.I | re.MULTILINE
            ))
            if not has_code and (end - start) > 5:
                violations.append((lines[start][0],
                    f"STRUCTURE: Section '{sec_name[:60]}' has no Claude Code terminal "
                    "example (no code block, no prompt, no cd command). "
                    "CLAUDE.md requires every section to include at least one "
                    "terminal example connecting the concept to Claude Code."))

    # ---- Check 4: Rhetorical questions as section openers ----
    # Only flag questions that follow a markdown heading (# or ##), not
    # numbered list items.  Numbered lists like "1. What is the scope?"
    # are prompts or test questions the learner types, not section openers.
    for i, (ln, text) in enumerate(lines):
        # Only match real markdown headings, not numbered list items
        if re.match(r"^#{1,3}\s+", text):
            # Look at the next non-empty line
            for j in range(i + 1, min(i + 4, len(lines))):
                next_text = lines[j][1].strip()
                if next_text and next_text.endswith("?") and not next_text.startswith("**"):
                    violations.append((lines[j][0],
                        f"STRUCTURE: Rhetorical question opens a section: "
                        f"'{snippet(next_text)}'. "
                        "CLAUDE.md forbids rhetorical questions as section openers."))
                    break
                if next_text:
                    break

    return violations


def snippet(text: str, width: int = 90) -> str:
    text = text.strip().replace("\n", " ")
    text = text.replace(EM_DASH, "[em-dash]").replace(EN_DASH, "[en-dash]")
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


# ---------------------------------------------------------------------------
# Path filter
# ---------------------------------------------------------------------------

def should_skip(file_path: Path) -> bool:
    p = str(file_path)
    return any(frag in p for frag in SKIP_PATH_FRAGMENTS)


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

SUPPORTED_SUFFIXES = (".md", ".txt", ".docx")


def lint_file(file_path: Path) -> int:
    if not file_path.exists():
        return 0
    if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        return 0
    if should_skip(file_path):
        return 0

    lines = read_text_lines(file_path)
    if not lines:
        return 0

    violations = find_style_violations(lines)
    violations.extend(find_structural_violations(file_path, lines))

    if not violations:
        return 0

    # Group by type for cleaner output
    style_v = [v for v in violations if not v[1].startswith("STRUCTURE:")]
    struct_v = [v for v in violations if v[1].startswith("STRUCTURE:")]

    print(f"\n{'='*70}", file=sys.stderr)
    print(f"STYLE CHECK: {file_path.name}", file=sys.stderr)
    print(f"{'='*70}", file=sys.stderr)

    if style_v:
        print(f"\n  STYLE VIOLATIONS ({len(style_v)}):", file=sys.stderr)
        for ln, msg in style_v:
            print(f"    line {ln}: {msg}", file=sys.stderr)

    if struct_v:
        print(f"\n  STRUCTURAL VIOLATIONS ({len(struct_v)}):", file=sys.stderr)
        for ln, msg in struct_v:
            print(f"    line {ln}: {msg}", file=sys.stderr)

    print(
        f"\n  Fix these before continuing. Rules live in CLAUDE.md.",
        file=sys.stderr,
    )
    print(f"{'='*70}\n", file=sys.stderr)
    return 2


def lint_all(project_root: Path) -> int:
    """Lint every .md and .docx file in the project (excluding skipped paths)."""
    exit_code = 0
    count = 0
    for suffix in SUPPORTED_SUFFIXES:
        for f in sorted(project_root.rglob(f"*{suffix}")):
            if should_skip(f):
                continue
            result = lint_file(f)
            if result == 2:
                exit_code = 2
                count += 1
    if exit_code == 0:
        print("All files clean.", file=sys.stderr)
    else:
        print(f"\n{count} file(s) with violations.", file=sys.stderr)
    return exit_code


def hook_mode() -> int:
    """Read a Claude Code tool-use JSON payload from stdin and lint the
    file it touched. Always exit 0 on parse error so a malformed hook
    payload never blocks unrelated work."""
    try:
        raw = sys.stdin.read()
    except Exception:  # noqa: BLE001
        return 0
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path")
    if not file_path:
        return 0

    return lint_file(Path(file_path))


def main(argv: List[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--hook":
        return hook_mode()
    if len(argv) >= 2 and argv[1] == "--all":
        # Find project root (parent of scripts/)
        project_root = Path(__file__).resolve().parent.parent
        return lint_all(project_root)
    if len(argv) >= 2:
        return lint_file(Path(argv[1]))
    print(
        "Usage:\n"
        "  check_style.py <file>    lint one file\n"
        "  check_style.py --hook    read tool-use JSON from stdin\n"
        "  check_style.py --all     lint all .md and .docx in project",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
