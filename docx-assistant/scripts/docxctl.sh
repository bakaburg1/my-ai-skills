#!/usr/bin/env bash
# Copyright (c) 2026 Angelo D'Ambrosio
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN="$SKILL_ROOT/tools/docxctl/bin/Release/net10.0/docxctl"

if [[ -x "$BIN" ]]; then
  exec "$BIN" "$@"
fi

PROJ="$SKILL_ROOT/tools/docxctl/docxctl.csproj"
exec dotnet run --project "$PROJ" -c Release -- "$@"
