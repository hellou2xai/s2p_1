"""Insert a tailored "How it all connects" data-flow banner into every handout.

For each .docx in Handouts/ (recursive):

    1. Remove any existing data-flow banner (the heading paragraph
       "How it all connects: the data flow" and the two tables plus
       spacer paragraph that follow it).
    2. Scan the document text and decide which Claude Code primitives
       (CLAUDE.md, Skills, Commands, MCP, Sub-agents, Hooks, Projects,
       Routines) are actually discussed in this document. A primitive
       counts as "discussed" if at least three substantive keyword
       matches appear (see PRIMITIVE_KEYWORDS).
    3. If at least one primitive qualifies, insert a tailored banner
       just before the first Heading 1 (or first "1." paragraph). The
       banner shows only the qualifying primitives in canonical order,
       separated by arrows, each in a colored cell.
    4. If no primitive qualifies, leave the document with no banner.

Run from the project root:

    python scripts/add_data_flow_banner.py
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
HANDOUTS_DIR = _PROJECT_ROOT / "Handouts"

BANNER_TITLE = "How it all connects: the data flow"

# Canonical chain order. The banner always renders primitives in this
# left-to-right order regardless of how many qualified.
CANONICAL_ORDER = [
    "CLAUDE.md",
    "Skills",
    "Commands",
    "MCP",
    "Sub-agents",
    "Hooks",
    "Projects",
    "Routines",
]

PRIMITIVE_COLORS = {
    "CLAUDE.md":  "DCEAF6",
    "Skills":     "E6EFD3",
    "Commands":   "F4E9C8",
    "MCP":        "DBEEEE",
    "Sub-agents": "F4DDD1",
    "Hooks":      "F2D5D5",
    "Projects":   "F4E1CC",
    "Routines":   "ECE3C5",
}

# Patterns that constitute a "substantive" mention of each primitive.
# Each primitive is included when the total match count >= MENTION_THRESHOLD.
PRIMITIVE_KEYWORDS = {
    "CLAUDE.md": [
        r"CLAUDE\.md",
    ],
    "Skills": [
        r"SKILL\.md",
        r"\.claude/skills",
        r"\bskill library\b",
        r"\bskill files?\b",
        r"\bskill composition\b",
        r"\bskill versioning\b",
    ],
    "Commands": [
        r"\bslash command",
        r"\.claude/commands",
        r"\bcustom command",
        r"\bcommand library\b",
    ],
    "MCP": [
        r"\bMCP\b",
        r"\bModel Context Protocol\b",
    ],
    "Sub-agents": [
        r"\bsub-?agents?\b",
        r"\bTask tool\b",
        r"\borchestrator(?:\s+agent)?\b",
        r"\bworker\s+agents?\b",
    ],
    "Hooks": [
        r"\bPreToolUse\b",
        r"\bPostToolUse\b",
        r"\bStop hook",
        r"\.claude/hooks",
        r"\bnotification hooks?\b",
        r"\bvalidation hooks?\b",
    ],
    "Projects": [
        r"\bClaude Projects?\b",
        r"\bproject-level\b",
        r"\.claude/settings\.json",
        r"\bcross-session memory\b",
        r"\bproject sharing\b",
    ],
    "Routines": [
        r"\bClaude routines?\b",
        r"\bscheduled (?:task|agent|routine|run)",
        r"\bcron\b",
        r"/routines\b",
    ],
}

MENTION_THRESHOLD = 3
MIN_PRIMITIVES_FOR_FLOW = 2


# ---------------------------------------------------------------------------
# Removal of any existing banner
# ---------------------------------------------------------------------------

def _remove_existing_banner(doc) -> bool:
    """Walk the body in document order, find the banner heading paragraph,
    then remove it plus the next 3 elements (two tables and one spacer
    paragraph) that the original universal banner inserted.
    """
    body = doc.element.body
    children = list(body)
    for i, el in enumerate(children):
        # Only paragraphs carry the title text.
        if el.tag == qn("w:p"):
            text = "".join(t.text or "" for t in el.iter(qn("w:t")))
            if BANNER_TITLE in text:
                # Remove the heading and up to 3 following elements
                # (table, table, paragraph spacer). Stop early if a
                # following Heading 1 appears, so we never delete real
                # content.
                to_remove = [el]
                j = i + 1
                while j < len(children) and len(to_remove) < 4:
                    nxt = children[j]
                    if nxt.tag == qn("w:p"):
                        # If this paragraph is a Heading 1 we have hit
                        # the original document content; stop.
                        style_el = nxt.find(qn("w:pPr") + "/" + qn("w:pStyle"))
                        if style_el is not None:
                            style_val = style_el.get(qn("w:val")) or ""
                            if style_val.lower().startswith("heading"):
                                break
                    to_remove.append(nxt)
                    j += 1
                for r in to_remove:
                    body.remove(r)
                return True
    return False


# ---------------------------------------------------------------------------
# Detection of which primitives this document discusses
# ---------------------------------------------------------------------------

def _full_text(doc) -> str:
    parts: List[str] = []
    for p in doc.paragraphs:
        if p.text:
            parts.append(p.text)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text:
                        parts.append(p.text)
    return "\n".join(parts)


def detect_primitives(doc) -> List[str]:
    text = _full_text(doc)
    found: List[str] = []
    for name in CANONICAL_ORDER:
        count = 0
        for pat in PRIMITIVE_KEYWORDS[name]:
            count += len(re.findall(pat, text, flags=re.IGNORECASE))
            if count >= MENTION_THRESHOLD:
                break
        if count >= MENTION_THRESHOLD:
            found.append(name)
    return found


# ---------------------------------------------------------------------------
# Banner construction
# ---------------------------------------------------------------------------

def _shade_cell(cell, fill_hex: str) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def _set_cell_borders(cell, color: str = "FFFFFF") -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)


def _build_cells_def(primitives: List[str]):
    """Produce the (kind, text, width) triples for the banner table.

    Layout: pill, arrow, pill, arrow, ..., pill.
    Width per primitive cell is fixed at 0.95"; arrow cells are 0.4".
    """
    cells = []
    for i, name in enumerate(primitives):
        if i > 0:
            cells.append(("arrow", "→", Inches(0.4)))
        cells.append(("primitive", name, Inches(0.95)))
    return cells


def _build_banner_elements(doc, primitives: List[str]):
    """Create heading + one table + spacer, then detach them from the body
    so the caller can re-insert them at the right spot.
    """
    elements = []

    heading = doc.add_paragraph()
    heading.paragraph_format.space_before = Pt(6)
    heading.paragraph_format.space_after = Pt(4)
    run = heading.add_run(BANNER_TITLE)
    run.bold = True
    run.font.size = Pt(12)
    elements.append(heading._p)

    cells_def = _build_cells_def(primitives)
    table = doc.add_table(rows=1, cols=len(cells_def))
    table.autofit = False
    for cell, (kind, text, width) in zip(table.rows[0].cells, cells_def):
        cell.width = width
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if kind == "primitive":
            r = p.add_run(text)
            r.bold = True
            r.font.size = Pt(10)
            _shade_cell(cell, PRIMITIVE_COLORS[text])
        else:
            r = p.add_run(text)
            r.font.size = Pt(11)
        _set_cell_borders(cell)
    elements.append(table._tbl)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(6)
    elements.append(spacer._p)

    body = doc.element.body
    for el in elements:
        body.remove(el)
    return elements


def _find_insertion_point(doc):
    for p in doc.paragraphs:
        style_name = (p.style.name or "").lower() if p.style else ""
        if style_name == "heading 1":
            return p._p
    for p in doc.paragraphs:
        text = (p.text or "").strip()
        if text.startswith("1.") or text.startswith("1)"):
            return p._p
    return None


# ---------------------------------------------------------------------------
# Per-file orchestration
# ---------------------------------------------------------------------------

def process(docx_path: Path) -> str:
    doc = Document(str(docx_path))

    removed = _remove_existing_banner(doc)
    primitives = detect_primitives(doc)

    if len(primitives) < MIN_PRIMITIVES_FOR_FLOW:
        if removed:
            doc.save(str(docx_path))
            reason = (
                f"only {len(primitives)} primitive ({primitives[0]})"
                if primitives else "no primitives detected"
            )
            return f"removed banner ({reason}; needs {MIN_PRIMITIVES_FOR_FLOW}+)"
        return "skip (no flow to show)"

    target = _find_insertion_point(doc)
    if target is None:
        if removed:
            doc.save(str(docx_path))
        return f"skip insert (no insertion point); detected: {', '.join(primitives)}"

    elements = _build_banner_elements(doc, primitives)
    for el in elements:
        target.addprevious(el)

    doc.save(str(docx_path))
    action = "rebuilt banner" if removed else "inserted banner"
    return f"{action}: {', '.join(primitives)}"


def main() -> None:
    if not HANDOUTS_DIR.exists():
        print(f"Handouts directory not found: {HANDOUTS_DIR}")
        return

    files = sorted(HANDOUTS_DIR.rglob("*.docx"))
    files = [f for f in files if " - Copy" not in f.name]
    files = [f for f in files if not f.name.startswith("~$")]

    if not files:
        print("No .docx handouts found.")
        return

    for f in files:
        try:
            status = process(f)
        except Exception as exc:
            status = f"ERROR: {exc}"
        rel = f.relative_to(_PROJECT_ROOT)
        print(f"{rel}: {status}")


if __name__ == "__main__":
    main()
