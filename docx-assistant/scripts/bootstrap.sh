#!/usr/bin/env bash
# Copyright (c) 2026 Angelo D'Ambrosio
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJ="$SKILL_ROOT/tools/docxctl/docxctl.csproj"

need_cmd() { command -v "$1" >/dev/null 2>&1; }

echo "[word-docx-assistant] Bootstrapping from: $SKILL_ROOT"

if ! need_cmd dotnet; then
  echo "dotnet not found."
  if [[ "$(uname -s)" == "Darwin" ]] && need_cmd brew; then
    echo "Installing .NET SDK (v8) via Homebrew..."
    brew install dotnet@8 || {
      echo "Homebrew install failed. Install .NET SDK 8 manually, then re-run bootstrap."
      exit 1
    }
    export PATH="/opt/homebrew/opt/dotnet@8/bin:$PATH"
  else
    echo "Install .NET SDK 8 manually, then re-run bootstrap."
    exit 1
  fi
fi

echo "dotnet: $(dotnet --version)"
dotnet build "$PROJ" -c Release
echo "Bootstrap complete. Try: $SKILL_ROOT/scripts/docxctl.sh status --in your.docx"
