#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree
from PIL import Image, ImageChops


OOXML_EXTENSIONS = {
    ".docx",
    ".docm",
    ".dotx",
    ".dotm",
    ".pptx",
    ".pptm",
    ".potx",
    ".potm",
    ".ppsx",
    ".ppsm",
    ".xlsx",
    ".xlsm",
    ".xltx",
    ".xltm",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare Office/PDF files by text extraction first, then package or metadata "
            "inspection, then optional visual rendering."
        )
    )
    parser.add_argument("--old", help="Baseline file path.")
    parser.add_argument("--new", help="Changed file path.")
    parser.add_argument(
        "--git-path",
        help=(
            "Path to the changed file in the working tree. The baseline is materialized from "
            "the given git revision."
        ),
    )
    parser.add_argument(
        "--git-rev",
        default="HEAD",
        help="Revision to use for --git-path mode. Defaults to HEAD.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for artifacts. Defaults to a temp directory.",
    )
    parser.add_argument(
        "--render-visual",
        choices=("auto", "always", "never"),
        default="auto",
        help="Whether to render page images and compare them.",
    )
    args = parser.parse_args()

    if args.git_path:
        if args.old:
            parser.error("--old cannot be used with --git-path")
        if not args.new:
            args.new = args.git_path
    elif not (args.old and args.new):
        parser.error("Provide either --git-path or both --old and --new")

    return args


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    binary: bool = False,
) -> str | bytes:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            check=check,
            capture_output=True,
            text=not binary,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Required tool not found: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", "replace") if binary else exc.stderr
        raise RuntimeError(
            f"Command failed ({' '.join(args)}): {stderr.strip() or 'no stderr'}"
        ) from exc

    return completed.stdout


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def make_diff(old_text: str, new_text: str, old_label: str, new_label: str) -> str:
    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile=old_label,
        tofile=new_label,
        lineterm="",
    )
    return "\n".join(diff) + "\n"


def relabel(path: Path) -> str:
    return path.name


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def canonicalize_xml(data: bytes) -> bytes:
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    root = etree.fromstring(data, parser=parser)
    return etree.tostring(root, method="c14n", with_comments=False)


def serialize_xml_for_diff(data: bytes) -> str:
    try:
        return canonicalize_xml(data).decode("utf-8", "replace")
    except Exception:
        return data.decode("utf-8", "replace")


def extract_docprops(data: bytes) -> dict[str, str]:
    try:
        parser = etree.XMLParser(remove_blank_text=True, recover=True)
        root = etree.fromstring(data, parser=parser)
    except Exception:
        return {}

    result: dict[str, str] = {}
    for child in root:
        key = child.get("name") or local_name(child.tag)
        value = "".join(text.strip() for text in child.itertext()).strip()
        result[key] = value
    return result


def snapshot_ooxml(path: Path, out_dir: Path) -> dict:
    snapshot = {"members": {}, "properties": {}, "entry_count": 0}

    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue

            name = info.filename
            data = archive.read(name)
            is_xml = name.endswith(".xml") or name.endswith(".rels") or name == "[Content_Types].xml"
            kind = "xml" if is_xml else "binary"

            record = {
                "kind": kind,
                "size": len(data),
                "sha256": "",
            }

            if is_xml:
                normalized = serialize_xml_for_diff(data)
                write_text(out_dir / "normalized" / name, normalized)
                record["sha256"] = sha256_bytes(normalized.encode("utf-8"))
                if name.startswith("docProps/"):
                    snapshot["properties"][name] = extract_docprops(data)
            else:
                record["sha256"] = sha256_bytes(data)

            snapshot["members"][name] = record

    snapshot["entry_count"] = len(snapshot["members"])
    return snapshot


def diff_properties(old: dict[str, dict[str, str]], new: dict[str, dict[str, str]]) -> dict[str, dict[str, dict[str, str]]]:
    result: dict[str, dict[str, dict[str, str]]] = {}
    all_parts = sorted(set(old) | set(new))
    for part in all_parts:
        old_part = old.get(part, {})
        new_part = new.get(part, {})
        all_keys = sorted(set(old_part) | set(new_part))
        changed: dict[str, dict[str, str]] = {}
        for key in all_keys:
            if old_part.get(key) != new_part.get(key):
                changed[key] = {
                    "old": old_part.get(key, ""),
                    "new": new_part.get(key, ""),
                }
        if changed:
            result[part] = changed
    return result


def compare_ooxml(old_path: Path, new_path: Path, out_dir: Path) -> dict:
    old_snapshot = snapshot_ooxml(old_path, out_dir / "old")
    new_snapshot = snapshot_ooxml(new_path, out_dir / "new")

    old_names = set(old_snapshot["members"])
    new_names = set(new_snapshot["members"])
    added = sorted(new_names - old_names)
    removed = sorted(old_names - new_names)
    shared = sorted(old_names & new_names)
    changed = [
        name
        for name in shared
        if old_snapshot["members"][name]["sha256"] != new_snapshot["members"][name]["sha256"]
    ]

    changed_xml = [name for name in changed if old_snapshot["members"][name]["kind"] == "xml"]
    changed_binary = [name for name in changed if old_snapshot["members"][name]["kind"] == "binary"]

    diffs_dir = out_dir / "diffs"
    for name in changed_xml:
        old_text = (out_dir / "old" / "normalized" / name).read_text(encoding="utf-8")
        new_text = (out_dir / "new" / "normalized" / name).read_text(encoding="utf-8")
        diff_text = make_diff(old_text, new_text, f"old/{name}", f"new/{name}")
        write_text(diffs_dir / f"{name}.diff", diff_text)

    properties_diff = diff_properties(old_snapshot["properties"], new_snapshot["properties"])
    report = {
        "status": "changed" if added or removed or changed else "same",
        "entry_counts": {
            "old": old_snapshot["entry_count"],
            "new": new_snapshot["entry_count"],
        },
        "added_entries": added,
        "removed_entries": removed,
        "changed_xml_entries": changed_xml,
        "changed_binary_entries": changed_binary,
        "metadata_changes": properties_diff,
    }
    write_text(out_dir / "report.json", json.dumps(report, indent=2, sort_keys=True))
    return report


def capture_text_command(args: list[str], destination: Path) -> dict:
    try:
        output = run_command(args)
    except RuntimeError as exc:
        message = f"[unavailable] {exc}\n"
        write_text(destination, message)
        return {"status": "error", "path": str(destination), "error": str(exc)}

    write_text(destination, output)
    return {"status": "ok", "path": str(destination)}


def compare_pdf(old_path: Path, new_path: Path, out_dir: Path) -> dict:
    commands = {
        "pdfinfo.txt": ["pdfinfo", str(old_path)],
        "pdfinfo-box.txt": ["pdfinfo", "-box", str(old_path)],
        "metadata.txt": ["pdfinfo", "-meta", str(old_path)],
        "fonts.txt": ["pdffonts", str(old_path)],
        "images.txt": ["pdfimages", "-list", str(old_path)],
    }
    old_results = {}
    new_results = {}
    diffs: dict[str, str] = {}
    failures: list[str] = []

    for filename, command in commands.items():
        old_results[filename] = capture_text_command(command, out_dir / "old" / filename)
        new_command = command.copy()
        new_command[-1] = str(new_path)
        new_results[filename] = capture_text_command(new_command, out_dir / "new" / filename)

        if old_results[filename]["status"] != "ok" or new_results[filename]["status"] != "ok":
            failures.append(filename)

        old_text = (out_dir / "old" / filename).read_text(encoding="utf-8")
        new_text = (out_dir / "new" / filename).read_text(encoding="utf-8")
        diff_text = make_diff(old_text, new_text, f"old/{filename}", f"new/{filename}")
        if diff_text.strip():
            diffs[filename] = str(out_dir / "diffs" / f"{filename}.diff")
            write_text(out_dir / "diffs" / f"{filename}.diff", diff_text)

    report = {
        "status": "error" if failures else "changed" if diffs else "same",
        "artifacts": diffs,
        "failed_commands": failures,
        "old_commands": old_results,
        "new_commands": new_results,
    }
    write_text(out_dir / "report.json", json.dumps(report, indent=2, sort_keys=True))
    return report


def render_pdf(pdf_path: Path, render_dir: Path) -> list[Path]:
    render_dir.mkdir(parents=True, exist_ok=True)
    run_command(["pdftoppm", "-png", str(pdf_path), str(render_dir / "page")])
    return sorted(render_dir.glob("page-*.png"))


def convert_office_to_pdf(document_path: Path, pdf_dir: Path) -> Path:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    run_command(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(pdf_dir),
            str(document_path),
        ]
    )
    candidates = sorted(pdf_dir.glob("*.pdf"))
    if not candidates:
        raise RuntimeError(f"LibreOffice did not produce a PDF for {document_path}")
    return candidates[0]


def render_document(path: Path, render_dir: Path) -> list[Path]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return render_pdf(path, render_dir / "pages")
    pdf_path = convert_office_to_pdf(path, render_dir / "pdf")
    return render_pdf(pdf_path, render_dir / "pages")


def normalized_rgb(path: Path) -> Image.Image:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return rgb.copy()


def compare_page_images(old_image: Path, new_image: Path, diff_path: Path) -> dict:
    old_rgb = normalized_rgb(old_image)
    new_rgb = normalized_rgb(new_image)

    width = max(old_rgb.width, new_rgb.width)
    height = max(old_rgb.height, new_rgb.height)

    old_canvas = Image.new("RGB", (width, height), "white")
    new_canvas = Image.new("RGB", (width, height), "white")
    old_canvas.paste(old_rgb, (0, 0))
    new_canvas.paste(new_rgb, (0, 0))

    diff = ImageChops.difference(old_canvas, new_canvas)
    bbox = diff.getbbox()
    total_pixels = width * height
    changed_pixels = 0

    if bbox is not None:
        mask = diff.convert("L").point(lambda value: 255 if value else 0)
        changed_pixels = mask.histogram()[255]
        if changed_pixels:
            diff_path.parent.mkdir(parents=True, exist_ok=True)
            mask.save(diff_path)

    return {
        "changed": bool(changed_pixels),
        "old_size": [old_rgb.width, old_rgb.height],
        "new_size": [new_rgb.width, new_rgb.height],
        "changed_pixels": changed_pixels,
        "changed_percent": round((changed_pixels / total_pixels) * 100, 4) if total_pixels else 0.0,
        "diff_image": str(diff_path) if changed_pixels else "",
    }


def compare_visual(old_path: Path, new_path: Path, out_dir: Path) -> dict:
    old_pages = render_document(old_path, out_dir / "old")
    new_pages = render_document(new_path, out_dir / "new")

    max_pages = max(len(old_pages), len(new_pages))
    page_reports = []
    changed_pages = []

    for index in range(max_pages):
        page_number = index + 1
        record = {"page": page_number}
        old_page = old_pages[index] if index < len(old_pages) else None
        new_page = new_pages[index] if index < len(new_pages) else None

        if old_page is None or new_page is None:
            record["status"] = "added_or_removed_page"
            record["old_page"] = str(old_page) if old_page else ""
            record["new_page"] = str(new_page) if new_page else ""
            changed_pages.append(page_number)
        else:
            comparison = compare_page_images(
                old_page,
                new_page,
                out_dir / "diffs" / f"page-{page_number:03d}.png",
            )
            record.update(comparison)
            record["status"] = "changed" if comparison["changed"] else "same"
            record["old_page"] = str(old_page)
            record["new_page"] = str(new_page)
            if comparison["changed"]:
                changed_pages.append(page_number)

        page_reports.append(record)

    report = {
        "status": "changed" if changed_pages else "same",
        "old_page_count": len(old_pages),
        "new_page_count": len(new_pages),
        "changed_pages": changed_pages,
        "pages": page_reports,
    }
    write_text(out_dir / "report.json", json.dumps(report, indent=2, sort_keys=True))
    return report


def ensure_markitdown(path: Path) -> str:
    output = run_command(["markitdown", str(path)])
    return output.replace("\r\n", "\n")


def compare_markdown(old_path: Path, new_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        old_text = ensure_markitdown(old_path)
        new_text = ensure_markitdown(new_path)
    except RuntimeError as exc:
        message = f"[unavailable] {exc}\n"
        write_text(out_dir / "error.txt", message)
        return {
            "status": "error",
            "error": str(exc),
            "diff_path": "",
            "error_path": str(out_dir / "error.txt"),
        }
    write_text(out_dir / "old.md", old_text)
    write_text(out_dir / "new.md", new_text)
    diff_text = make_diff(old_text, new_text, relabel(old_path), relabel(new_path))
    write_text(out_dir / "text.diff", diff_text)
    return {
        "status": "changed" if diff_text.strip() else "same",
        "old_markdown": str(out_dir / "old.md"),
        "new_markdown": str(out_dir / "new.md"),
        "diff_path": str(out_dir / "text.diff"),
    }


def path_is_ooxml(path: Path) -> bool:
    if path.suffix.lower() not in OOXML_EXTENSIONS:
        return False
    if not zipfile.is_zipfile(path):
        return False
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    return "[Content_Types].xml" in names and any(name.startswith(("word/", "ppt/", "xl/")) for name in names)


def should_run_visual(mode: str, text_status: str, structure_status: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    return text_status != "changed" or structure_status == "changed"


def materialize_git_pair(git_path: str, git_rev: str, out_dir: Path) -> tuple[Path, Path, str]:
    working_path = Path(git_path).expanduser()
    if not working_path.is_absolute():
        working_path = (Path.cwd() / working_path).resolve()
    else:
        working_path = working_path.resolve()

    if not working_path.exists():
        raise RuntimeError(f"Changed file does not exist: {working_path}")

    repo_root = Path(
        run_command(["git", "-C", str(working_path.parent), "rev-parse", "--show-toplevel"]).strip()
    )
    relative_path = working_path.relative_to(repo_root).as_posix()
    baseline_bytes = run_command(
        ["git", "-C", str(repo_root), "show", f"{git_rev}:{relative_path}"],
        binary=True,
    )
    baseline_path = out_dir / f"baseline{working_path.suffix}"
    write_bytes(baseline_path, baseline_bytes)
    return baseline_path, working_path, relative_path


def build_summary(report: dict) -> str:
    lines = [
        f"Artifacts: {report['artifacts_dir']}",
        f"Compared: {report['old_file']} -> {report['new_file']}",
        f"Text tier: {report['text']['status']}",
    ]

    if report["text"]["status"] == "changed":
        lines.append(f"Text diff: {report['text']['diff_path']}")
    elif report["text"]["status"] == "error":
        lines.append(f"Text tier error: {report['text']['error']}")

    lines.append(f"Structure tier: {report['structure']['status']}")
    structure = report["structure"]
    if structure["status"] == "error":
        lines.append(f"Structure tier error: {structure['error']}")
    if "changed_xml_entries" in structure and structure["changed_xml_entries"]:
        preview = ", ".join(structure["changed_xml_entries"][:5])
        lines.append(f"Changed XML entries: {preview}")
    if "changed_binary_entries" in structure and structure["changed_binary_entries"]:
        preview = ", ".join(structure["changed_binary_entries"][:5])
        lines.append(f"Changed binary entries: {preview}")
    if "artifacts" in structure and structure["artifacts"]:
        lines.append(f"PDF metadata diffs: {len(structure['artifacts'])} report(s)")
    if "failed_commands" in structure and structure["failed_commands"]:
        lines.append(f"Failed PDF commands: {', '.join(structure['failed_commands'])}")

    lines.append(f"Visual tier: {report['visual']['status']}")
    if report["visual"]["status"] == "error":
        lines.append(f"Visual tier error: {report['visual']['error']}")
    if report["visual"]["status"] == "changed":
        page_list = ", ".join(str(page) for page in report["visual"]["changed_pages"][:10])
        lines.append(f"Changed pages: {page_list}")

    if report.get("git_relative_path"):
        lines.append(f"Git path: {report['git_relative_path']}")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    artifacts_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else Path(tempfile.mkdtemp(prefix="office-pdf-diff-"))
    )
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    report: dict = {
        "artifacts_dir": str(artifacts_dir),
        "git_relative_path": "",
    }

    try:
        if args.git_path:
            old_path, new_path, git_relative_path = materialize_git_pair(
                args.git_path,
                args.git_rev,
                artifacts_dir / "git",
            )
            report["git_relative_path"] = git_relative_path
        else:
            old_path = Path(args.old).expanduser().resolve()
            new_path = Path(args.new).expanduser().resolve()
            if not old_path.exists():
                raise RuntimeError(f"Baseline file does not exist: {old_path}")
            if not new_path.exists():
                raise RuntimeError(f"Changed file does not exist: {new_path}")

        report["old_file"] = str(old_path)
        report["new_file"] = str(new_path)

        try:
            text_report = compare_markdown(old_path, new_path, artifacts_dir / "markitdown")
        except Exception as exc:
            text_report = {"status": "error", "error": str(exc)}
        report["text"] = text_report

        try:
            if path_is_ooxml(old_path) and path_is_ooxml(new_path):
                structure_report = compare_ooxml(old_path, new_path, artifacts_dir / "package")
            elif old_path.suffix.lower() == ".pdf" and new_path.suffix.lower() == ".pdf":
                structure_report = compare_pdf(old_path, new_path, artifacts_dir / "pdf")
            else:
                structure_report = {
                    "status": "skipped",
                    "reason": "No OOXML/PDF package inspection path for this file type.",
                }
        except Exception as exc:
            structure_report = {"status": "error", "error": str(exc)}
        report["structure"] = structure_report

        if should_run_visual(args.render_visual, text_report["status"], structure_report["status"]):
            try:
                visual_report = compare_visual(old_path, new_path, artifacts_dir / "visual")
            except Exception as exc:
                visual_report = {"status": "error", "error": str(exc)}
        else:
            visual_report = {"status": "skipped", "reason": "Visual tier not requested."}
        report["visual"] = visual_report

        write_text(artifacts_dir / "report.json", json.dumps(report, indent=2, sort_keys=True))
        print(build_summary(report))
        return 0
    except Exception as exc:
        report["error"] = str(exc)
        write_text(artifacts_dir / "report.json", json.dumps(report, indent=2, sort_keys=True))
        print(f"Failed: {exc}", file=sys.stderr)
        print(f"Artifacts: {artifacts_dir}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
