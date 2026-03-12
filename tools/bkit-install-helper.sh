#!/usr/bin/env bash
set -euo pipefail

BASE="/Users/master/.openclaw/workspace/tools"
CLAUDE_REPO="$BASE/bkit-claude-code"
GEMINI_REPO="$BASE/bkit-gemini"

echo "[bkit helper] checking environment..."

if command -v claude >/dev/null 2>&1; then
  echo "- Claude CLI detected"
  echo "  Run inside Claude Code:"
  echo "  /plugin marketplace add popup-studio-ai/bkit-claude-code"
  echo "  /plugin install bkit"
else
  echo "- Claude CLI not found (skip direct plugin install)"
fi

if command -v gemini >/dev/null 2>&1; then
  echo "- Gemini CLI detected"
  echo "  installing bkit-gemini extension..."
  gemini extensions install "$GEMINI_REPO" || true
  echo "  verify in Gemini CLI with /extensions"
else
  echo "- Gemini CLI not found (skip extension install)"
fi

echo "\nLocal repos prepared:"
echo "  $CLAUDE_REPO"
echo "  $GEMINI_REPO"
