<!-- v1.0 2026-04-25 Initial. -->

# Onboarding Script (Reference Solution)

A shell script that sets up a new analyst workspace in under 10 minutes.

## The script

Save this as `scripts/onboard-analyst.sh`:

```bash
#!/usr/bin/env bash
# onboard-analyst.sh
# Sets up a new analyst workspace for Summit Procurement Group.
# Usage: bash scripts/onboard-analyst.sh "Sarah Kim" "Chicago" "IT services, raw materials"

set -e

ANALYST_NAME="$1"
OFFICE="$2"
CATEGORIES="$3"

if [ -z "$ANALYST_NAME" ] || [ -z "$OFFICE" ] || [ -z "$CATEGORIES" ]; then
    echo "Usage: bash scripts/onboard-analyst.sh \"Analyst Name\" \"Office\" \"Categories\""
    echo "Example: bash scripts/onboard-analyst.sh \"Sarah Kim\" \"Chicago\" \"IT services, raw materials\""
    exit 1
fi

# Create workspace folder name from analyst name (replace spaces with hyphens)
FOLDER_NAME=$(echo "$ANALYST_NAME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
WORKSPACE="workspaces/$FOLDER_NAME"

echo "Setting up workspace for $ANALYST_NAME ($OFFICE)..."
echo "  Workspace: $WORKSPACE"
echo "  Categories: $CATEGORIES"
echo ""

# Step 1: Create folder structure
echo "[1/6] Creating folder structure..."
mkdir -p "$WORKSPACE/.claude/commands"
mkdir -p "$WORKSPACE/data"
mkdir -p "$WORKSPACE/drafts"
mkdir -p "$WORKSPACE/outputs"
mkdir -p "$WORKSPACE/audit-logs"
mkdir -p "$WORKSPACE/notifications"

# Step 2: Copy shared CLAUDE.md
echo "[2/6] Copying shared context..."
cp shared/CLAUDE.md "$WORKSPACE/shared-CLAUDE.md"

# Step 3: Create analyst-specific CLAUDE.md from template
echo "[3/6] Creating analyst CLAUDE.md..."
sed -e "s/\[ANALYST NAME\]/$ANALYST_NAME/g" \
    -e "s/\[OFFICE\]/$OFFICE/g" \
    -e "s/\[ROLE\]/Category Analyst/g" \
    -e "s/\[CATEGORIES\]/$CATEGORIES/g" \
    analyst-workspace-template/CLAUDE.md > "$WORKSPACE/CLAUDE.md"

# Step 4: Copy shared skills and commands
echo "[4/6] Copying skills and commands..."
cp -r shared/skills "$WORKSPACE/.claude/skills"
cp shared/commands/*.md "$WORKSPACE/.claude/commands/"

# Step 5: Create settings.json with hooks
echo "[5/6] Configuring hooks..."
HOOKS_DIR=$(cd hooks && pwd)
cat > "$WORKSPACE/.claude/settings.json" << SETTINGS_EOF
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$HOOKS_DIR/review-gate.py\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$HOOKS_DIR/audit-log.py\""
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$HOOKS_DIR/team-notify.py\""
          }
        ]
      }
    ]
  }
}
SETTINGS_EOF

# Step 6: Set environment variables
echo "[6/6] Setting environment variables..."
echo "export CLAUDE_ANALYST_NAME=\"$ANALYST_NAME\"" >> "$WORKSPACE/.env"
echo "export CLAUDE_SESSION_ID=\"$(date +%Y%m%d-%H%M%S)\"" >> "$WORKSPACE/.env"

echo ""
echo "Workspace ready: $WORKSPACE"
echo ""
echo "To start Claude Code in this workspace:"
echo "  cd $WORKSPACE"
echo "  source .env"
echo "  claude"
echo ""
echo "Setup time: under 1 minute."
echo "The analyst should update their CLAUDE.md with current priorities."
```

## How it works

1. Creates the folder structure: `.claude/`, `data/`, `drafts/`, `outputs/`, `audit-logs/`.
2. Copies the shared CLAUDE.md as a reference file (`shared-CLAUDE.md`).
3. Generates an analyst-specific CLAUDE.md from the template, replacing placeholders with the analyst's name, office, and categories.
4. Copies all shared skills to `.claude/skills/` and all shared commands to `.claude/commands/`.
5. Creates a `settings.json` with the three hooks pre-registered (audit log, review gate, team notify).
6. Sets environment variables for audit trail identification.

## Key points

- The script uses `set -e` so it stops on any error.
- Hook paths use absolute paths (resolved with `pwd`) because Claude Code does not expand variables in hook commands.
- The analyst's CLAUDE.md inherits standards from the shared file but has space for personal context.
- The script takes three arguments: analyst name, office, and categories. No interactive prompts.
- Total setup time: under 1 minute for the script, plus 5 to 10 minutes for the analyst to customize their CLAUDE.md and run a test command.
