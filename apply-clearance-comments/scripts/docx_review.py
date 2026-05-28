#!/usr/bin/env python3
# Copyright (c) 2026 Angelo D'Ambrosio
"""Inspect and mark tracked changes/comments in DOCX review files.

This intentionally reads the DOCX package directly instead of using Word,
LibreOffice, or rendered text. Output is line-oriented text by default and JSON
with --json for automation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = f"{{{NS['w']}}}"
MARKS = (" _ R+", " _ R-", " _ R~")
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
WP14_NS = "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"
W16CID_NS = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
W16CEX_NS = "http://schemas.microsoft.com/office/word/2018/wordml/cex"
W14 = f"{{{W14_NS}}}"
WP14 = f"{{{WP14_NS}}}"
W15 = f"{{{W15_NS}}}"
W16CID = f"{{{W16CID_NS}}}"
W16CEX = f"{{{W16CEX_NS}}}"
MC = f"{{{MC_NS}}}"
COMMENTS_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
COMMENTS_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
COMMENTS_EXTENDED_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml"
COMMENTS_EXTENDED_REL_TYPE = "http://schemas.microsoft.com/office/2011/relationships/commentsExtended"
COMMENTS_IDS_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml"
COMMENTS_IDS_REL_TYPE = "http://schemas.microsoft.com/office/2016/09/relationships/commentsIds"
COMMENTS_EXTENSIBLE_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtensible+xml"
COMMENTS_EXTENSIBLE_REL_TYPE = "http://schemas.microsoft.com/office/2018/08/relationships/commentsExtensible"

ET.register_namespace("w", NS["w"])
ET.register_namespace("ct", CT_NS)
ET.register_namespace("mc", MC_NS)
ET.register_namespace("w14", W14_NS)
ET.register_namespace("wp14", WP14_NS)
ET.register_namespace("w15", W15_NS)
ET.register_namespace("w16cid", W16CID_NS)
ET.register_namespace("w16cex", W16CEX_NS)


def xml_bytes(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def xml_bytes_default_ns(root: ET.Element, namespace: str) -> bytes:
    ET.register_namespace("", namespace)
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def clean(text: str) -> str:
    return " ".join(text.split())


def local_name(node: ET.Element) -> str:
    if not isinstance(node.tag, str):
        return ""
    return node.tag.rsplit("}", 1)[-1] if "}" in node.tag else node.tag


def texts_by_name(node: ET.Element, *names: str) -> list[str]:
    wanted = set(names)
    return [child.text or "" for child in node.iter() if local_name(child) in wanted]


def node_text(node: ET.Element) -> str:
    return clean("".join(texts_by_name(node, "t", "delText")))


def accepted_text(paragraph: ET.Element) -> str:
    return clean("".join(texts_by_name(paragraph, "t")))


def original_text(paragraph: ET.Element) -> str:
    out: list[str] = []

    def walk(element: ET.Element, in_insert: bool = False) -> None:
        if not isinstance(element.tag, str):
            return
        tag = local_name(element)
        if tag == "ins":
            in_insert = True
        if tag == "del":
            out.extend(texts_by_name(element, "delText"))
            return
        if tag == "t" and not in_insert:
            out.append(element.text or "")
        for child in element:
            walk(child, in_insert)

    walk(paragraph)
    return clean("".join(out))


def is_marked(author: str | None) -> bool:
    return bool(author and any(mark in author for mark in MARKS))


def pstyle(paragraph: ET.Element) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    return style.get(W + "val") if style is not None else ""


def heading_level(style: str) -> int | None:
    normalized = re.sub(r"[\s_-]+", "", style.casefold())
    match = re.search(r"([1-6])$", normalized)
    if not match:
        return None
    heading_prefixes = (
        "heading",
        "titolo",
        "titre",
        "uberschrift",
        "encabezado",
        "rubrik",
        "overskrift",
        "kop",
    )
    if any(prefix in normalized for prefix in heading_prefixes):
        return int(match.group(1))
    return None


@dataclass
class ParagraphInfo:
    index: int
    h1: str
    h2: str
    h3: str
    paragraph: ET.Element

    @property
    def location(self) -> str:
        return " > ".join(part for part in (self.h1, self.h2, self.h3) if part)


def load_doc(path: Path) -> tuple[ET.Element, dict[str, ET.Element], ZipFile]:
    zf = ZipFile(path)
    doc = ET.fromstring(zf.read("word/document.xml"))
    comments: dict[str, ET.Element] = {}
    if "word/comments.xml" in zf.namelist():
        root = ET.fromstring(zf.read("word/comments.xml"))
        for comment in root.findall(".//w:comment", NS):
            cid = comment.get(W + "id")
            if cid is not None:
                comments[cid] = comment
    return doc, comments, zf


def iter_paragraphs(doc: ET.Element) -> Iterable[ParagraphInfo]:
    h1 = h2 = h3 = ""
    for index, paragraph in enumerate(doc.findall(".//w:p", NS), start=1):
        text = accepted_text(paragraph)
        style = pstyle(paragraph)
        level = heading_level(style)
        if level == 1:
            h1, h2, h3 = text, "", ""
        elif level == 2:
            h2, h3 = text, ""
        elif level is not None and level >= 3:
            h3 = text
        yield ParagraphInfo(index=index, h1=h1, h2=h2, h3=h3, paragraph=paragraph)


def parse_range(text: str) -> tuple[int | None, int | None]:
    if not text:
        return None, None
    if ":" in text:
        start, end = text.split(":", 1)
        return int(start), int(end)
    value = int(text)
    return value, value


def in_bounds(index: int, start: int | None, end: int | None) -> bool:
    return (start is None or index >= start) and (end is None or index <= end)


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False))


def iter_revisions(paragraph: ET.Element) -> Iterable[ET.Element]:
    for element in paragraph.iter():
        if local_name(element) in {"ins", "del"}:
            yield element


def comment_ids(paragraph: ET.Element) -> list[str]:
    ids = [
        element.get(W + "id")
        for element in paragraph.iter()
        if local_name(element) in {"commentRangeStart", "commentReference"}
    ]
    return [cid for cid in ids if cid is not None]


def marked_comment_paragraph(paragraph: ET.Element, cid: str) -> tuple[str, bool]:
    out: list[str] = []
    in_range = False
    saw_start = False
    saw_end = False

    def walk(element: ET.Element) -> None:
        nonlocal in_range, saw_start, saw_end
        if not isinstance(element.tag, str):
            return
        tag = local_name(element)
        if tag == "commentRangeStart" and element.get(W + "id") == cid:
            out.append("==")
            in_range = True
            saw_start = True
            return
        if tag == "commentRangeEnd" and element.get(W + "id") == cid:
            out.append("==")
            in_range = False
            saw_end = True
            return
        if tag == "t":
            out.append(element.text or "")
        for child in element:
            walk(child)

    walk(paragraph)
    text = clean("".join(out)).replace("== ", "==").replace(" ==", "==")
    if saw_start and saw_end:
        parts = text.split("==")
        if len(parts) == 3:
            before, marked, after = parts
            text = f"{clean(before)} =={clean(marked)}== {clean(after)}".strip()
        return text, True
    return accepted_text(paragraph), False


def comment_payload(comment: ET.Element) -> dict[str, str | None]:
    return {
        "id": comment.get(W + "id"),
        "author": comment.get(W + "author") or "",
        "date": comment.get(W + "date"),
        "text": clean("".join(texts_by_name(comment, "t"))),
    }


def default_author() -> str:
    for name in (
        os.environ.get("CLEARANCE_RESPONSE_AUTHOR"),
        os.environ.get("GIT_AUTHOR_NAME"),
        os.environ.get("USER_FULL_NAME"),
    ):
        if name and name.strip():
            return name.strip()
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.name"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except OSError:
        pass
    try:
        result = subprocess.run(["id", "-F"], check=False, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except OSError:
        pass
    return getpass.getuser() or "Reviewer response"


def initials(author: str) -> str:
    letters = [part[0].upper() for part in re.findall(r"[A-Za-z]+", author)]
    return "".join(letters[:3]) or "CR"


def next_id(elements: Iterable[ET.Element], attr: str) -> int:
    values = []
    for element in elements:
        value = element.get(attr)
        if value is not None and value.isdigit():
            values.append(int(value))
    return max(values, default=-1) + 1


def next_comment_id(doc: ET.Element, comments_root: ET.Element) -> int:
    values = []
    for element in comments_root.findall(".//w:comment", NS):
        value = element.get(W + "id")
        if value is not None and value.isdigit():
            values.append(int(value))
    for element in doc.iter():
        value = element.get(W + "id")
        if value is not None and value.isdigit():
            values.append(int(value))
    return max(values, default=-1) + 1


def ensure_comments_root(zin: ZipFile) -> ET.Element:
    if "word/comments.xml" in zin.namelist():
        return ET.fromstring(zin.read("word/comments.xml"))
    return ET.Element(W + "comments")


def unique_hex(existing: set[str], nbytes: int = 4) -> str:
    value = secrets.token_hex(nbytes).upper()
    while value in existing:
        value = secrets.token_hex(nbytes).upper()
    existing.add(value)
    return value


def first_child_by_name(node: ET.Element, name: str) -> ET.Element | None:
    for child in node:
        if local_name(child) == name:
            return child
    return None


def first_descendant_by_name(node: ET.Element, name: str) -> ET.Element | None:
    for child in node.iter():
        if local_name(child) == name:
            return child
    return None


def comment_by_id(comments_root: ET.Element, comment_id: str) -> ET.Element | None:
    for comment in comments_root.findall(".//w:comment", NS):
        if comment.get(W + "id") == comment_id:
            return comment
    return None


def ensure_comment_paragraph(comment: ET.Element) -> ET.Element:
    paragraph = first_child_by_name(comment, "p")
    if paragraph is None:
        paragraph = ET.SubElement(comment, W + "p")
    return paragraph


def existing_para_ids(*roots: ET.Element | None) -> set[str]:
    ids: set[str] = set()
    for root in roots:
        if root is None:
            continue
        for element in root.iter():
            value = element.get(W14 + "paraId") or element.get(W15 + "paraId") or element.get(W16CID + "paraId")
            if value:
                ids.add(value)
    return ids


def namespaces_used(root: ET.Element) -> set[str]:
    namespaces: set[str] = set()
    for element in root.iter():
        if isinstance(element.tag, str) and element.tag.startswith("{"):
            namespaces.add(element.tag[1:].split("}", 1)[0])
        for attr in element.attrib:
            if attr.startswith("{"):
                namespaces.add(attr[1:].split("}", 1)[0])
    return namespaces


def clean_ignorable(root: ET.Element) -> None:
    value = root.get(MC + "Ignorable")
    if not value:
        return
    namespace_to_prefix = {
        W14_NS: "w14",
        WP14_NS: "wp14",
        W15_NS: "w15",
        W16CID_NS: "w16cid",
        W16CEX_NS: "w16cex",
    }
    used_prefixes = {
        prefix
        for namespace, prefix in namespace_to_prefix.items()
        if namespace in namespaces_used(root)
    }
    kept = [prefix for prefix in value.split() if prefix in used_prefixes]
    if kept:
        root.set(MC + "Ignorable", " ".join(kept))
    else:
        root.attrib.pop(MC + "Ignorable", None)


def ensure_comments_ignorable(root: ET.Element) -> None:
    if W14_NS not in namespaces_used(root):
        return
    existing = root.get(MC + "Ignorable", "").split()
    if "w14" not in existing:
        existing.append("w14")
    root.set(MC + "Ignorable", " ".join(existing))


def ensure_para_id(paragraph: ET.Element, used: set[str]) -> str:
    para_id = paragraph.get(W14 + "paraId")
    if not para_id:
        para_id = unique_hex(used)
        paragraph.set(W14 + "paraId", para_id)
    else:
        used.add(para_id)
    if not paragraph.get(W14 + "textId"):
        paragraph.set(W14 + "textId", "77777777")
    return para_id


def ensure_content_types(zin: ZipFile, thread_parts: bool = False) -> bytes | None:
    if "[Content_Types].xml" not in zin.namelist():
        return None
    root = ET.fromstring(zin.read("[Content_Types].xml"))
    specs = [
        ("/word/comments.xml", COMMENTS_CONTENT_TYPE),
    ]
    if thread_parts:
        specs.extend(
            [
                ("/word/commentsExtended.xml", COMMENTS_EXTENDED_CONTENT_TYPE),
                ("/word/commentsIds.xml", COMMENTS_IDS_CONTENT_TYPE),
                ("/word/commentsExtensible.xml", COMMENTS_EXTENSIBLE_CONTENT_TYPE),
            ]
        )
    for part_name, content_type in specs:
        exists = [
            item
            for item in root.findall(f"{{{CT_NS}}}Override")
            if item.get("PartName") == part_name
        ]
        if not exists:
            override = ET.SubElement(root, f"{{{CT_NS}}}Override")
            override.set("PartName", part_name)
            override.set("ContentType", content_type)
    return xml_bytes_default_ns(root, CT_NS)


def ensure_relationships(zin: ZipFile, thread_parts: bool = False) -> bytes | None:
    rels_name = "word/_rels/document.xml.rels"
    if rels_name not in zin.namelist():
        root = ET.Element(f"{{{REL_NS}}}Relationships")
    else:
        root = ET.fromstring(zin.read(rels_name))
    specs = [
        (COMMENTS_REL_TYPE, "comments.xml"),
    ]
    if thread_parts:
        specs.extend(
            [
                (COMMENTS_EXTENDED_REL_TYPE, "commentsExtended.xml"),
                (COMMENTS_IDS_REL_TYPE, "commentsIds.xml"),
                (COMMENTS_EXTENSIBLE_REL_TYPE, "commentsExtensible.xml"),
            ]
        )
    for rel_type, target in specs:
        relationships = [item for item in root if local_name(item) == "Relationship"]
        exists = [
            item
            for item in relationships
            if item.get("Type") == rel_type and item.get("Target") == target
        ]
        if not exists:
            rel = ET.SubElement(root, f"{{{REL_NS}}}Relationship")
            existing_ids = {item.get("Id") for item in relationships}
            rid_num = 1
            while f"rId{rid_num}" in existing_ids:
                rid_num += 1
            rel.set("Id", f"rId{rid_num}")
            rel.set("Type", rel_type)
            rel.set("Target", target)
            relationships.append(rel)
    return xml_bytes_default_ns(root, REL_NS)


def ensure_comments_extended_root(zin: ZipFile) -> ET.Element:
    if "word/commentsExtended.xml" in zin.namelist():
        return ET.fromstring(zin.read("word/commentsExtended.xml"))
    root = ET.Element(W15 + "commentsEx")
    root.set(MC + "Ignorable", "w15")
    return root


def ensure_comments_ids_root(zin: ZipFile) -> ET.Element:
    if "word/commentsIds.xml" in zin.namelist():
        return ET.fromstring(zin.read("word/commentsIds.xml"))
    root = ET.Element(W16CID + "commentsIds")
    root.set(MC + "Ignorable", "w16cid")
    return root


def ensure_comments_extensible_root(zin: ZipFile) -> ET.Element:
    if "word/commentsExtensible.xml" in zin.namelist():
        return ET.fromstring(zin.read("word/commentsExtensible.xml"))
    root = ET.Element(W16CEX + "commentsExtensible")
    root.set(MC + "Ignorable", "w16cex")
    return root


def ensure_comment_ex(root: ET.Element, para_id: str, parent_para_id: str | None = None) -> None:
    for item in root.findall(f".//{W15}commentEx"):
        if item.get(W15 + "paraId") == para_id:
            if parent_para_id:
                item.set(W15 + "paraIdParent", parent_para_id)
            if not item.get(W15 + "done"):
                item.set(W15 + "done", "0")
            return
    item = ET.SubElement(root, W15 + "commentEx")
    item.set(W15 + "paraId", para_id)
    if parent_para_id:
        item.set(W15 + "paraIdParent", parent_para_id)
    item.set(W15 + "done", "0")


def ensure_comment_id(root: ET.Element, para_id: str, used_durable: set[str], durable_id: str | None = None) -> str:
    for item in root.findall(f".//{W16CID}commentId"):
        if item.get(W16CID + "paraId") == para_id:
            existing = item.get(W16CID + "durableId")
            if existing:
                used_durable.add(existing)
                return existing
            break
    durable_id = durable_id or unique_hex(used_durable)
    item = ET.SubElement(root, W16CID + "commentId")
    item.set(W16CID + "paraId", para_id)
    item.set(W16CID + "durableId", durable_id)
    return durable_id


def add_comment_extensible(root: ET.Element, durable_id: str, date_utc: str | None = None) -> None:
    for item in root.findall(f".//{W16CEX}commentExtensible"):
        if item.get(W16CEX + "durableId") == durable_id:
            if date_utc and not item.get(W16CEX + "dateUtc"):
                item.set(W16CEX + "dateUtc", date_utc)
            return
    item = ET.SubElement(root, W16CEX + "commentExtensible")
    item.set(W16CEX + "durableId", durable_id)
    item.set(W16CEX + "dateUtc", date_utc or dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"))


def migrate_comment_metadata(
    comments_root: ET.Element,
    comments_ex_root: ET.Element,
    comments_ids_root: ET.Element,
    comments_extensible_root: ET.Element,
    used_para_ids: set[str],
    used_durable_ids: set[str],
) -> None:
    for comment in comments_root.findall(".//w:comment", NS):
        paragraph = ensure_comment_paragraph(comment)
        para_id = ensure_para_id(paragraph, used_para_ids)
        ensure_comment_ex(comments_ex_root, para_id)
        durable_id = ensure_comment_id(comments_ids_root, para_id, used_durable_ids)
        add_comment_extensible(
            comments_extensible_root,
            durable_id,
            date_utc=comment.get(W + "date"),
        )


def comment_element(comment_id: int, author: str, text: str, para_id: str | None = None) -> ET.Element:
    comment = ET.Element(W + "comment")
    comment.set(W + "id", str(comment_id))
    comment.set(W + "author", author)
    comment.set(W + "initials", initials(author))
    comment.set(W + "date", dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
    paragraph = ET.SubElement(comment, W + "p")
    if para_id:
        paragraph.set(W14 + "paraId", para_id)
        paragraph.set(W14 + "textId", "77777777")
    ppr = ET.SubElement(paragraph, W + "pPr")
    pstyle_el = ET.SubElement(ppr, W + "pStyle")
    pstyle_el.set(W + "val", "CommentText")
    ref_run = ET.SubElement(paragraph, W + "r")
    ref_rpr = ET.SubElement(ref_run, W + "rPr")
    ref_rstyle = ET.SubElement(ref_rpr, W + "rStyle")
    ref_rstyle.set(W + "val", "CommentReference")
    ref = ET.SubElement(ref_run, W + "annotationRef")
    run = ET.SubElement(paragraph, W + "r")
    t = ET.SubElement(run, W + "t")
    t.text = text
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return comment


def add_paragraph_comment(paragraph: ET.Element, comment_id: int) -> None:
    start = ET.Element(W + "commentRangeStart")
    start.set(W + "id", str(comment_id))
    end = ET.Element(W + "commentRangeEnd")
    end.set(W + "id", str(comment_id))
    ref_run = ET.Element(W + "r")
    ref = ET.SubElement(ref_run, W + "commentReference")
    ref.set(W + "id", str(comment_id))

    insert_at = 1 if len(paragraph) and local_name(paragraph[0]) == "pPr" else 0
    paragraph.insert(insert_at, start)
    paragraph.append(end)
    paragraph.append(ref_run)


def comment_reference_id(run: ET.Element) -> str | None:
    ref = first_descendant_by_name(run, "commentReference")
    return ref.get(W + "id") if ref is not None else None


def add_threaded_comment_reference(paragraph: ET.Element, parent_comment_id: str, reply_comment_id: int) -> None:
    children = list(paragraph)
    parent_start_idx = None
    for idx, child in enumerate(children):
        if local_name(child) == "commentRangeStart" and child.get(W + "id") == parent_comment_id:
            parent_start_idx = idx
            break
    if parent_start_idx is None:
        parent_start_idx = 1 if len(paragraph) and local_name(paragraph[0]) == "pPr" else 0
        start = ET.Element(W + "commentRangeStart")
        start.set(W + "id", parent_comment_id)
        paragraph.insert(parent_start_idx, start)

    insert_start_at = parent_start_idx + 1
    children = list(paragraph)
    while insert_start_at < len(children) and local_name(children[insert_start_at]) == "commentRangeStart":
        insert_start_at += 1
    start = ET.Element(W + "commentRangeStart")
    start.set(W + "id", str(reply_comment_id))
    paragraph.insert(insert_start_at, start)

    children = list(paragraph)
    insert_end_at = None
    for idx, child in enumerate(children):
        if local_name(child) == "commentRangeEnd" and child.get(W + "id") == parent_comment_id:
            insert_end_at = idx + 1
            break
    if insert_end_at is None:
        insert_end_at = len(paragraph)

    children = list(paragraph)
    while insert_end_at < len(children) and local_name(children[insert_end_at]) == "commentRangeEnd":
        insert_end_at += 1

    end = ET.Element(W + "commentRangeEnd")
    end.set(W + "id", str(reply_comment_id))
    paragraph.insert(insert_end_at, end)

    children = list(paragraph)
    insert_ref_at = insert_end_at + 1
    while insert_ref_at < len(children) and local_name(children[insert_ref_at]) == "r" and comment_reference_id(children[insert_ref_at]):
        insert_ref_at += 1

    ref_run = ET.Element(W + "r")
    reply_ref = ET.SubElement(ref_run, W + "commentReference")
    reply_ref.set(W + "id", str(reply_comment_id))
    paragraph.insert(insert_ref_at, ref_run)


def paragraphs_for_comment(doc: ET.Element, comment_id: str) -> list[ParagraphInfo]:
    rows = []
    for info in iter_paragraphs(doc):
        if comment_id in comment_ids(info.paragraph):
            rows.append(info)
    return rows


def paragraphs_for_feedback(doc: ET.Element, args: argparse.Namespace) -> list[ParagraphInfo]:
    if args.comment_id:
        rows = []
        for cid in args.comment_id:
            rows.extend(paragraphs_for_comment(doc, cid))
        unique: dict[int, ParagraphInfo] = {row.index: row for row in rows}
        return list(unique.values())
    start, end = parse_range(args.paragraphs)
    return [info for info in iter_paragraphs(doc) if in_bounds(info.index, start, end)]


def cmd_headings(args: argparse.Namespace) -> None:
    doc, _, zf = load_doc(args.docx)
    with zf:
        for info in iter_paragraphs(doc):
            style = pstyle(info.paragraph)
            text = accepted_text(info.paragraph)
            if style or text in args.extra:
                print(f"{info.index}\t{style or '-'}\t{text}")


def cmd_edits(args: argparse.Namespace) -> None:
    start, end = parse_range(args.paragraphs)
    doc, _, zf = load_doc(args.docx)
    rows = []
    with zf:
        for info in iter_paragraphs(doc):
            if not in_bounds(info.index, start, end):
                continue
            revisions = []
            for change in iter_revisions(info.paragraph):
                author = change.get(W + "author") or ""
                if args.unmarked_only and is_marked(author):
                    continue
                if args.marked_only and not is_marked(author):
                    continue
                revisions.append(
                    {
                        "type": local_name(change),
                        "author": author,
                        "text": node_text(change),
                    }
                )
            if not revisions:
                continue
            row = {
                "paragraph": info.index,
                "location": info.location,
                "original": original_text(info.paragraph),
                "accepted": accepted_text(info.paragraph),
                "revisions": revisions,
            }
            rows.append(row)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for row in rows:
        print(f"\nP {row['paragraph']} | {row['location']}")
        print(f"ORIG: {row['original']}")
        print(f"ACC : {row['accepted']}")
        for revision in row["revisions"]:
            print(f"{revision['type']}\t{revision['author']}\t{revision['text']!r}")


def cmd_comments(args: argparse.Namespace) -> None:
    start, end = parse_range(args.paragraphs)
    author_filter = (args.author or "").lower()
    doc, comments, zf = load_doc(args.docx)
    rows = []
    with zf:
        for info in iter_paragraphs(doc):
            if not in_bounds(info.index, start, end):
                continue
            ids = comment_ids(info.paragraph)
            for cid in dict.fromkeys(ids):
                comment = comments.get(cid)
                if comment is None:
                    continue
                payload = comment_payload(comment)
                author = str(payload["author"])
                if author_filter and author_filter not in author.lower():
                    continue
                if args.exclude_author and args.exclude_author.lower() in author.lower():
                    continue
                marked_paragraph, range_ok = marked_comment_paragraph(info.paragraph, cid)
                row = {
                    "id": cid,
                    "paragraph": info.index,
                    "location": info.location,
                    "range_identified": range_ok,
                    "anchor_paragraph": marked_paragraph,
                    **payload,
                }
                rows.append(row)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for row in rows:
        print(f"\nCOMMENT {row['id']} | P {row['paragraph']} | {row['location']}")
        print(f"AUTHOR: {row['author']}")
        print(f"RANGE_IDENTIFIED: {row['range_identified']}")
        print("PARAGRAPH:")
        print(wrap(str(row["anchor_paragraph"]), args.width))
        print("COMMENT:")
        print(wrap(str(row["text"]), args.width))


def cmd_mark(args: argparse.Namespace) -> None:
    if args.marker not in {"R+", "R-", "R~"}:
        raise SystemExit("--marker must be one of R+, R-, R~")
    suffix = f" _ {args.marker}"
    start, end = parse_range(args.paragraphs)
    target_comments = set(args.comment_id or [])
    target_texts = args.text or []
    changed = 0

    with ZipFile(args.docx, "r") as zin:
        doc = ET.fromstring(zin.read("word/document.xml"))
        comments_root = None
        if "word/comments.xml" in zin.namelist():
            comments_root = ET.fromstring(zin.read("word/comments.xml"))

        if args.kind in {"revision", "both"}:
            for info in iter_paragraphs(doc):
                if not in_bounds(info.index, start, end):
                    continue
                for change in iter_revisions(info.paragraph):
                    author = change.get(W + "author") or ""
                    if is_marked(author) and not args.force:
                        continue
                    text = node_text(change)
                    if target_texts and not any(target in text for target in target_texts):
                        continue
                    change.set(W + "author", author + suffix)
                    changed += 1

        if comments_root is not None and args.kind in {"comment", "both"}:
            for comment in comments_root.findall(".//w:comment", NS):
                cid = comment.get(W + "id")
                if target_comments and cid not in target_comments:
                    continue
                author = comment.get(W + "author") or ""
                if is_marked(author) and not args.force:
                    continue
                comment.set(W + "author", author + suffix)
                changed += 1

        if args.dry_run:
            print(f"would_mark\t{changed}")
            return

        clean_ignorable(doc)
        if comments_root is not None:
            ensure_comments_ignorable(comments_root)
        new_doc = xml_bytes(doc)
        new_comments = (
            xml_bytes(comments_root)
            if comments_root is not None
            else None
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp_path = Path(tmp.name)
        with ZipFile(args.docx, "r") as zin2, ZipFile(tmp_path, "w", ZIP_DEFLATED) as zout:
            for item in zin2.infolist():
                if item.filename == "word/document.xml":
                    data = new_doc
                elif item.filename == "word/comments.xml" and new_comments is not None:
                    data = new_comments
                else:
                    data = zin2.read(item.filename)
                zout.writestr(item, data)
        with ZipFile(tmp_path, "r") as ztest:
            bad = ztest.testzip()
            if bad:
                raise SystemExit(f"bad zip member after write: {bad}")
        shutil.move(str(tmp_path), args.docx)
    print(f"marked\t{changed}")


def cmd_feedback(args: argparse.Namespace) -> None:
    if not args.text.strip():
        raise SystemExit("--text must not be empty")
    author = args.author or default_author()
    with ZipFile(args.docx, "r") as zin:
        doc = ET.fromstring(zin.read("word/document.xml"))
        comments_root = ensure_comments_root(zin)
        comments_ex_root = ensure_comments_extended_root(zin)
        comments_ids_root = ensure_comments_ids_root(zin)
        comments_extensible_root = ensure_comments_extensible_root(zin)
        used_para_ids = existing_para_ids(doc, comments_root, comments_ex_root, comments_ids_root)
        durable_root = comments_ids_root if comments_ids_root is not None else ET.Element("empty")
        used_durable_ids = {
            item.get(W16CID + "durableId")
            for item in durable_root.iter()
            if item.get(W16CID + "durableId")
        }

        migrate_comment_metadata(
            comments_root,
            comments_ex_root,
            comments_ids_root,
            comments_extensible_root,
            used_para_ids,
            used_durable_ids,
        )

        next_comment = next_comment_id(doc, comments_root)
        added = 0
        if args.comment_id:
            for parent_id in args.comment_id:
                parent_comment = comment_by_id(comments_root, parent_id)
                if parent_comment is None:
                    raise SystemExit(f"comment id not found: {parent_id}")
                parent_paragraphs = paragraphs_for_comment(doc, parent_id)
                if not parent_paragraphs:
                    raise SystemExit(f"no anchor paragraph found for comment id: {parent_id}")
                if len(parent_paragraphs) > 1 and not args.all:
                    matches = ", ".join(str(info.index) for info in parent_paragraphs)
                    raise SystemExit(f"comment id {parent_id} matched multiple paragraphs ({matches}); pass --all")
                parent_comment_p = ensure_comment_paragraph(parent_comment)
                parent_para_id = ensure_para_id(parent_comment_p, used_para_ids)
                ensure_comment_ex(comments_ex_root, parent_para_id)
                parent_durable_id = ensure_comment_id(comments_ids_root, parent_para_id, used_durable_ids)
                add_comment_extensible(
                    comments_extensible_root,
                    parent_durable_id,
                    date_utc=parent_comment.get(W + "date"),
                )

                for info in parent_paragraphs:
                    reply_para_id = unique_hex(used_para_ids)
                    reply_id = next_comment
                    next_comment += 1
                    reply_comment = comment_element(reply_id, author, args.text, reply_para_id)
                    comments_root.append(reply_comment)
                    add_threaded_comment_reference(info.paragraph, parent_id, reply_id)
                    ensure_comment_ex(comments_ex_root, reply_para_id, parent_para_id)
                    durable_id = ensure_comment_id(comments_ids_root, reply_para_id, used_durable_ids)
                    add_comment_extensible(
                        comments_extensible_root,
                        durable_id,
                        date_utc=reply_comment.get(W + "date"),
                    )
                    added += 1
        else:
            paragraphs = paragraphs_for_feedback(doc, args)
            if not paragraphs:
                raise SystemExit("no matching paragraph found for feedback")
            if not args.all and len(paragraphs) > 1:
                matches = ", ".join(str(info.index) for info in paragraphs)
                raise SystemExit(f"feedback target matched multiple paragraphs ({matches}); pass --all or narrow the target")
            for info in paragraphs:
                comment_id = next_comment
                next_comment += 1
                comment_para_id = unique_hex(used_para_ids)
                feedback_comment = comment_element(comment_id, author, args.text, comment_para_id)
                comments_root.append(feedback_comment)
                add_paragraph_comment(info.paragraph, comment_id)
                ensure_comment_ex(comments_ex_root, comment_para_id)
                durable_id = ensure_comment_id(comments_ids_root, comment_para_id, used_durable_ids)
                add_comment_extensible(
                    comments_extensible_root,
                    durable_id,
                    date_utc=feedback_comment.get(W + "date"),
                )
                added += 1

        if args.dry_run:
            print(f"would_add_feedback\t{added}\tauthor\t{author}")
            return

        clean_ignorable(doc)
        ensure_comments_ignorable(comments_root)
        new_doc = xml_bytes(doc)
        new_comments = xml_bytes(comments_root)
        new_comments_ex = xml_bytes(comments_ex_root)
        new_comments_ids = xml_bytes(comments_ids_root)
        new_comments_extensible = xml_bytes(comments_extensible_root)
        new_content_types = ensure_content_types(zin, thread_parts=True)
        new_rels = ensure_relationships(zin, thread_parts=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp_path = Path(tmp.name)
        written = set()
        with ZipFile(args.docx, "r") as zin2, ZipFile(tmp_path, "w", ZIP_DEFLATED) as zout:
            for item in zin2.infolist():
                written.add(item.filename)
                if item.filename == "word/document.xml":
                    data = new_doc
                elif item.filename == "word/comments.xml":
                    data = new_comments
                elif item.filename == "word/commentsExtended.xml" and new_comments_ex is not None:
                    data = new_comments_ex
                elif item.filename == "word/commentsIds.xml" and new_comments_ids is not None:
                    data = new_comments_ids
                elif item.filename == "word/commentsExtensible.xml" and new_comments_extensible is not None:
                    data = new_comments_extensible
                elif item.filename == "[Content_Types].xml" and new_content_types is not None:
                    data = new_content_types
                elif item.filename == "word/_rels/document.xml.rels" and new_rels is not None:
                    data = new_rels
                else:
                    data = zin2.read(item.filename)
                zout.writestr(item, data)
            if "word/comments.xml" not in written:
                zout.writestr("word/comments.xml", new_comments)
            if "word/commentsExtended.xml" not in written and new_comments_ex is not None:
                zout.writestr("word/commentsExtended.xml", new_comments_ex)
            if "word/commentsIds.xml" not in written and new_comments_ids is not None:
                zout.writestr("word/commentsIds.xml", new_comments_ids)
            if "word/commentsExtensible.xml" not in written and new_comments_extensible is not None:
                zout.writestr("word/commentsExtensible.xml", new_comments_extensible)
            if "word/_rels/document.xml.rels" not in written and new_rels is not None:
                zout.writestr("word/_rels/document.xml.rels", new_rels)
        with ZipFile(tmp_path, "r") as ztest:
            bad = ztest.testzip()
            if bad:
                raise SystemExit(f"bad zip member after write: {bad}")
        shutil.move(str(tmp_path), args.docx)
    print(f"feedback\t{added}\tauthor\t{author}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("headings", help="List paragraph numbers for Word headings")
    p.add_argument("docx", type=Path)
    p.add_argument("--extra", action="append", default=[], help="Also print exact text matches")
    p.set_defaults(func=cmd_headings)

    p = sub.add_parser("edits", help="List tracked insertions/deletions")
    p.add_argument("docx", type=Path)
    p.add_argument("--paragraphs", default="", help="Paragraph number or range, e.g. 342:462")
    p.add_argument("--unmarked-only", action="store_true")
    p.add_argument("--marked-only", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_edits)

    p = sub.add_parser("comments", help="List comments with highlighted anchor paragraphs")
    p.add_argument("docx", type=Path)
    p.add_argument("--paragraphs", default="", help="Paragraph number or range, e.g. 342:462")
    p.add_argument("--author")
    p.add_argument("--exclude-author")
    p.add_argument("--width", type=int, default=78)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_comments)

    p = sub.add_parser("mark", help="Append R+/R-/R~ to revision or comment author metadata")
    p.add_argument("docx", type=Path)
    p.add_argument("--kind", choices=["revision", "comment", "both"], default="revision")
    p.add_argument("--marker", required=True, help="R+, R-, or R~")
    p.add_argument("--paragraphs", default="", help="Paragraph number or range")
    p.add_argument("--comment-id", action="append")
    p.add_argument("--text", action="append", help="Only mark revisions containing this text")
    p.add_argument("--force", action="store_true", help="Also append marker to already marked items")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_mark)

    p = sub.add_parser("feedback", help="Add reviewer-facing response comments to the DOCX")
    p.add_argument("docx", type=Path)
    p.add_argument("--paragraphs", default="", help="Paragraph number or range")
    p.add_argument("--comment-id", action="append", help="Anchor feedback to the paragraph containing this comment")
    p.add_argument("--text", required=True, help="Feedback comment text to add")
    p.add_argument("--author", help="Author shown on the response comment")
    p.add_argument("--all", action="store_true", help="Allow adding the same feedback to multiple matched paragraphs")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_feedback)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
