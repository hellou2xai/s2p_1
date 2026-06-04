"""Regenerate Course 15 practice data.

Thin wrapper around build_course_data.main() so the LMS handout's reference to
`regenerate_data.py` resolves to a real script. Run this from the course root
or from inside scripts/:

    python scripts/regenerate_data.py
"""

from __future__ import annotations

from build_course_data import main

if __name__ == "__main__":
    main()
