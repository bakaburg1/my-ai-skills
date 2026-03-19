#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 4 ]]; then
  echo "Usage: $0 <input.ppt|input.pptx> <output_dir> [dpi=150] [prefix=slide]" >&2
  exit 1
fi

input="$1"
out_dir="$2"
dpi="${3:-150}"
prefix="${4:-slide}"

if [[ ! -f "$input" ]]; then
  echo "Input file not found: $input" >&2
  exit 1
fi

if ! command -v soffice >/dev/null 2>&1; then
  echo "Missing required command: soffice" >&2
  exit 1
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "Missing required command: pdftoppm" >&2
  exit 1
fi

mkdir -p "$out_dir"

tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/pptx-export.XXXXXX")"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

soffice --headless --convert-to pdf --outdir "$tmp_dir" "$input" >/dev/null 2>&1

pdf_path="$(find "$tmp_dir" -maxdepth 1 -type f -iname '*.pdf' | head -n 1 || true)"
if [[ -z "$pdf_path" ]]; then
  echo "PDF conversion failed for: $input" >&2
  exit 1
fi

pdftoppm -png -r "$dpi" "$pdf_path" "$tmp_dir/$prefix" >/dev/null 2>&1

count=0
while IFS= read -r img; do
  count=$((count + 1))
  printf -v idx "%02d" "$count"
  cp "$img" "$out_dir/${prefix}_${idx}.png"
done < <(find "$tmp_dir" -maxdepth 1 -type f -name "$prefix-*.png" | sort -V)

if [[ "$count" -eq 0 ]]; then
  echo "No PNG files produced from: $input" >&2
  exit 1
fi

echo "Exported $count slide image(s) to: $out_dir"
