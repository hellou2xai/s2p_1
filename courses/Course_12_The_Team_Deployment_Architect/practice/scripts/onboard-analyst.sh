#!/usr/bin/env bash
# onboard-analyst.sh
# Creates a new analyst workspace from the template.
# Usage: bash scripts/onboard-analyst.sh <analyst_name> <office>
# Example: bash scripts/onboard-analyst.sh sarah_kim chicago

set -euo pipefail

ANALYST_NAME="${1:?Usage: onboard-analyst.sh <analyst_name> <office>}"
OFFICE="${2:?Usage: onboard-analyst.sh <analyst_name> <office>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")/practice"
TEMPLATE_DIR="$PROJECT_DIR/analyst-workspace-template"
TARGET_DIR="$PROJECT_DIR/workspaces/$ANALYST_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "Error: Workspace already exists at $TARGET_DIR"
    exit 1
fi

echo "Creating workspace for $ANALYST_NAME ($OFFICE office)..."

# Copy template
cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

# Copy shared files
cp "$PROJECT_DIR/shared/CLAUDE.md" "$TARGET_DIR/shared-context.md"
cp -r "$PROJECT_DIR/shared/skills" "$TARGET_DIR/skills"
cp -r "$PROJECT_DIR/shared/commands" "$TARGET_DIR/.claude/commands"
cp -r "$PROJECT_DIR/hooks" "$TARGET_DIR/hooks"

# Personalize CLAUDE.md
sed -i "s/\[Analyst Name\]/$ANALYST_NAME/g" "$TARGET_DIR/CLAUDE.md"
sed -i "s/\[Office\]/$OFFICE/g" "$TARGET_DIR/CLAUDE.md"

# Create audit directory
mkdir -p "$TARGET_DIR/audit"

echo "Workspace created at $TARGET_DIR"
echo "Next steps:"
echo "  1. Edit $TARGET_DIR/CLAUDE.md with your role and categories."
echo "  2. Open Claude Code in $TARGET_DIR."
echo "  3. Run /daily-check to verify everything works."
