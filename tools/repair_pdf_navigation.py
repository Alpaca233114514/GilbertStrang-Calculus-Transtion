"""Rebuild navigation in the legacy merged PDF without retypesetting its pages.

Usage: python tools/repair_pdf_navigation.py [--source PDF] [--output PDF]
Requires the existing pypdf and pdfplumber packages. The original is backed up
under tmp/pdfs/navigation before the output is replaced.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import Fit, IndirectObject, NameObject


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output/pdf/GilbertStrang-Calculus.pdf"


def plain_title(value: str) -> str:
    value = value.replace("$", "").replace("\\,", " ")
    for command, symbol in {"theta": "θ", "pi": "π", "sin": "sin", "cos": "cos"}.items():
        value = value.replace("\\" + command, symbol)
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", value).strip()


def heading_lines(page):
    chars = page.filter(lambda obj: obj.get("object_type") == "char"
                        and obj.get("size", 0) >= 15
                        and "Bold" in obj.get("fontname", ""))
    lines = []
    for word in chars.extract_words():
        if not lines or abs(lines[-1]["top"] - word["top"]) > 3:
            lines.append({"text": word["text"], "top": word["top"]})
        else:
            lines[-1]["text"] += " " + word["text"]
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    work = ROOT / "tmp/pdfs/navigation"
    work.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(source)
    old_outline = reader.outline
    files = sorted(p for p in (ROOT / "translation_draft").glob("*.zh-CN.md")
                   if not p.name.startswith(("00_", "96_", "97_")))
    # Legacy builder order is fixed; reject other layouts instead of guessing.
    # 旧合并器的顺序固定；遇到其他结构时停止，避免猜测定位。
    assert all(isinstance(item, dict) for item in old_outline), "Use the original flat-outline PDF as --source"
    assert len(old_outline) == len(files) + 5, "Unexpected source outline count"
    starts = [item["/Page"] if isinstance(item.get("/Page"), int)
              else reader.get_destination_page_number(item) for item in old_outline]
    assert all(page is not None and 0 <= page < len(reader.pages) for page in starts)
    assert starts == sorted(starts), "Source sections are out of order"

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.root_object.pop(NameObject("/Outlines"), None)
    writer.add_metadata({"/Title": "微积分 · 中文译稿", "/Author": "Gilbert Strang"})
    writer.page_mode = "/UseOutlines"
    entries, targets = [], {}
    chapters, parts = {}, {}

    with pdfplumber.open(source) as document:
        cache = {}

        def lines(page_index):
            if page_index not in cache:
                page = document.pages[page_index]
                cache[page_index] = heading_lines(page)
                page.close()
            return cache[page_index]

        def locate(start, end, pattern):
            for index in range(start, end):
                for line in lines(index):
                    if re.search(pattern, line["text"]):
                        return index, line["top"], line["text"]
            raise ValueError(f"Heading {pattern!r} not found on pages {start + 1}-{end}")

        def add(title, location, parent=None, key=None, level=0):
            page, top, evidence = location
            coordinate = min(float(writer.pages[page].mediabox.height),
                             float(writer.pages[page].mediabox.height) - top + 12)
            fit = Fit.xyz(left=0, top=coordinate, zoom=None)
            node = writer.add_outline_item(title, page, parent=parent, fit=fit, is_open=False)
            item = {"title": title, "level": level, "page": page + 1,
                    "top": coordinate, "heading": evidence, "key": key}
            entries.append(item)
            if key is not None:
                assert key not in targets, f"Duplicate navigation key: {key}"
                targets[key] = item
            return node

        add("封面", (0, 0, "封面"))
        for index, title in [(1, "前言"), (2, "目录"), (3, "公式速查表（书前）")]:
            add(title, locate(starts[index], starts[index + 1], "^" + re.escape(title)))

        for index, path in enumerate(files, 4):
            start = starts[index]
            end = starts[index + 1]
            headings = re.findall(r"^#{1,2}\s+(.+)", path.read_text(encoding="utf-8-sig"), re.M)
            match = re.search(r"_ch(\d+)_sec(\d+)", path.name)
            if match:
                chapter, section = map(int, match.groups())
                key = f"{chapter}.{section}"
                if section == 1:
                    chapter_title = plain_title(headings[0])
                    location = locate(start, end, rf"^第\s*{chapter}\s*章")
                    chapters[chapter] = add(chapter_title, location, key=f"ch{chapter}")
                title = next(plain_title(h) for h in headings if re.match(rf"{re.escape(key)}(?!\d)", h))
                location = locate(start, end, rf"^{re.escape(key)}(?!\d)")
                if key == "0.4":
                    if key not in parts:
                        parts[key] = add("0.4 视频讲座概要与练习题", location,
                                         parent=chapters[chapter], key=key, level=1)
                    add(title, location, parent=parts[key], level=2)
                else:
                    add(title, location, parent=chapters[chapter], key=key, level=1)
            else:
                title = plain_title(headings[0])
                chapter_match = re.match(r"第\s*(\d+)\s*章", title)
                pattern = (rf"^第\s*{chapter_match[1]}\s*章" if chapter_match
                           else "^" + re.escape(title))
                add(title, locate(start, end, pattern),
                    key=f"ch{chapter_match[1]}" if chapter_match else None)

        add("译注汇总", locate(starts[-1], len(reader.pages), "^译注汇总"))
        expected_sections = {f"{int(m[1])}.{int(m[2])}" for path in files
                             if (m := re.search(r"_ch(\d+)_sec(\d+)", path.name))}
        assert expected_sections <= targets.keys()
        assert {f"ch{i}" for i in range(17)} <= targets.keys()

        links = []
        for page_index in range(starts[2], starts[3]):
            page = document.pages[page_index]
            words = page.extract_words()
            for word in words:
                if word["x0"] >= 100:
                    continue
                token = word["text"]
                chapter_match = re.fullmatch(r"第(\d+)章", token)
                key = f"ch{chapter_match[1]}" if chapter_match else token
                if key not in targets:
                    continue
                target = targets[key]
                row = [w for w in words if abs(w["top"] - word["top"]) < 4]
                top = min(w["top"] for w in row) - 5
                bottom = max(w["bottom"] for w in row) + 5
                rect = (48, float(page.height) - bottom, float(page.width) - 48, float(page.height) - top)
                annotation = writer.add_annotation(page_index, Link(rect=rect,
                    target_page_index=target["page"] - 1,
                    fit=Fit.xyz(left=0, top=target["top"], zoom=None)))
                annotation["/Dest"][0] = writer.pages[target["page"] - 1].indirect_reference
                links.append({"page": page_index + 1, "key": key,
                              "target_page": target["page"], "rect": rect})
            page.close()
        assert {link["key"] for link in links} == set(targets), "Printed TOC is incomplete"
        assert len(links) == len(targets), "Duplicate printed TOC rows"

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = work / f"GilbertStrang-Calculus.before-navigation-{timestamp}.pdf"
    shutil.copy2(source, backup)
    staged = work / f"repaired-{timestamp}.pdf"
    writer.write(staged)
    result = PdfReader(staged)
    assert len(result.pages) == len(reader.pages)

    def walk(items):
        for item in items:
            if isinstance(item, list):
                yield from walk(item)
            else:
                yield item

    actual_entries = list(walk(result.outline))
    assert len(actual_entries) == len(entries)
    for actual, expected in zip(actual_entries, entries):
        assert actual.title == expected["title"]
        assert isinstance(actual.raw_get("/Page"), IndirectObject)
        assert result.get_destination_page_number(actual) + 1 == expected["page"]
        assert actual.typ == "/XYZ" and abs(float(actual.top) - expected["top"]) < .01
    # Navigation-only repair: preserve every rendered page content stream.
    # 仅修复导航：逐页确认渲染内容流完全保留。
    for before, after in zip(reader.pages, result.pages):
        assert before.mediabox == after.mediabox
        assert before.get_contents().get_data() == after.get_contents().get_data()
    checked_links = 0
    for page in result.pages:
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            if annotation.get("/Subtype") == "/Link" and "/Dest" in annotation:
                assert isinstance(annotation["/Dest"][0], IndirectObject)
                checked_links += 1
    assert checked_links >= len(links)
    if output != source and output.exists():
        shutil.copy2(output, work / f"output-before-navigation-{timestamp}.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged, output)
    report = {"source": str(source), "output": str(output), "backup": str(backup),
              "pages": len(result.pages), "bookmarks": len(entries),
              "chapters": 17, "sections": len(expected_sections),
              "toc_links": len(links), "page_content_streams_unchanged": True,
              "entries": entries, "links": links}
    (work / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"entries", "links"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
