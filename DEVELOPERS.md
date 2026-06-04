# S2P Platform (private)

The dev workspace for the S2P course product: course content, build tooling, student clients, and the license server contract. The server code itself lives in the sibling repo `hellou2xai/s2p_1` and deploys to Render at `https://api.u2xai.academy`.

## Layout

```
courses/                 the 20 courses, canonical source (lessons, practice
                         data, solutions, regenerators)
docs/                    lesson template, folder structure, prompt library,
                         use cases: read before editing any course content
scripts/                 check_style.py (the style gate) and build utilities
CLAUDE.md                the authoring rules; every lesson edit must pass them
Platform/
  License_Server_Spec.md the client-server contract; change server and
                         clients together, never one side alone
  build_pack.py          builds the public zip and the 20 gated bundles
                         from courses/ into Platform/dist/ (gitignored)
  upload_bundles.py      pushes bundles to the R2 bucket with sha256 metadata
  client/                what students receive: fetch.py, check_license.py,
                         u2xai_config.json, START_HERE.md
```

## The split that must never break

The public zip carries lessons only. Practice data, solutions, and regenerator scripts ship exclusively through the license server as per-course bundles. If a data file ever lands in the public zip, the license gate is decoration. `build_pack.py` enforces the split; after changing it, verify with the leak check (zero `.csv`, `.db`, `.docx`, `solutions/`, or course `scripts/` entries in the public zip).

## Working on course content

1. Edit under `courses/`. Follow `CLAUDE.md` and `docs/Lesson_Template.md` in full.
2. Run the style gate on anything you touched: `python scripts/check_style.py <file>` (zero output means clean). Wire it as a PostToolUse hook in your own `.claude/settings.json` with an absolute path; Claude Code does not expand variables in hook commands, so each developer sets their own path.
3. Rebuild and ship: `python Platform/build_pack.py`, then `python Platform/upload_bundles.py` (needs the R2 credentials), then publish the new public zip wherever students download it.

## Working on the platform

Server changes happen in `s2p_1` (push to main deploys via Render). Client changes happen here in `Platform/client/`, then a rebuild. The contract in `Platform/License_Server_Spec.md` is the source of truth for both; update it first, then the code on each side.

## Credentials

Nothing in this repo holds a secret. R2 credentials and the Resend key live in the Render dashboard (Environment tab) and are entered at upload time for `upload_bundles.py`. Keep it that way.
