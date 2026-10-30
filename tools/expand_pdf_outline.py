"""Add the actual body subheadings to an existing chapter/section PDF outline.

Reads rendered text and typography from the PDF, excludes the notes appendix,
and preserves all page content and existing link annotations. Use --scan-only
to inspect the detected headings before writing the PDF.
"""

import argparse
import ctypes
from datetime import datetime
import json
import math
import os
from pathlib import Path
import re
import shutil

import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit, IndirectObject, NameObject


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/GilbertStrang-Calculus.pdf"
WORK = ROOT / "tmp/pdfs/navigation"


def compact(value):
    return re.sub(r"[\s\u200b^_{}\\]", "", value)


def old_tree(reader, items, parent=None, depth=0):
    result = []
    previous = None
    for item in items:
        if isinstance(item, list):
            result.extend(old_tree(reader, item, previous, depth + 1))
        else:
            previous = {"title": item.title, "page": reader.get_destination_page_number(item),
                        "top": float(item.top) if item.top is not None else float(reader.pages[reader.get_destination_page_number(item)].mediabox.height),
                        "parent": parent, "depth": depth, "kind": "original"}
            result.append(previous)
    return result


def scan(document, stop):
    headings = []
    for page_index in range(2, stop):
        page = document[page_index]
        textpage = page.get_textpage()
        groups = []
        glyphs = []
        x, y = ctypes.c_double(), ctypes.c_double()
        flags = ctypes.c_int()
        buffer = ctypes.create_string_buffer(256)
        matrix = pdfium.raw.FS_MATRIX()
        for char_index in range(textpage.count_chars()):
            size = pdfium.raw.FPDFText_GetFontSize(textpage.raw, char_index)
            if size < 6:
                continue
            pdfium.raw.FPDFText_GetMatrix(textpage.raw, char_index, ctypes.byref(matrix))
            size *= math.hypot(matrix.c, matrix.d)
            if size < 6:
                continue
            code = pdfium.raw.FPDFText_GetUnicode(textpage.raw, char_index)
            if not code or chr(code).isspace():
                continue
            pdfium.raw.FPDFText_GetCharOrigin(textpage.raw, char_index, ctypes.byref(x), ctypes.byref(y))
            glyphs.append({"text": chr(code), "x": x.value, "y": y.value, "size": size, "index": char_index})
            if size < 11.5:
                continue
            length = pdfium.raw.FPDFText_GetFontInfo(textpage.raw, char_index, buffer, len(buffer), ctypes.byref(flags))
            name = buffer.value.decode("utf-8", errors="replace") if length else ""
            glyphs[-1]["fontname"] = name
            group = next((g for g in reversed(groups) if abs(g["baseline"] - y.value) < 1.5), None)
            if group is None:
                group = {"baseline": y.value, "left": x.value, "size": size, "bold": False, "characters": []}
                groups.append(group)
            group["left"] = min(group["left"], x.value)
            group["size"] = max(group["size"], size)
            group["bold"] |= "MicrosoftYaHei" in name and "Bold" in name
            group["characters"].append(chr(code))
        candidates = []
        for group in groups:
            if not group["bold"] or group["left"] > 75:
                continue
            baseline, size = group["baseline"], group["size"]
            title_glyphs = [glyph for glyph in glyphs if 45 <= glyph["x"] < 550
                            and baseline - .3 * size <= glyph["y"] <= baseline + .65 * size]
            title_glyphs.sort(key=lambda glyph: (glyph["x"], -glyph["y"]))
            parts, previous = [], None
            left, right, bottom, top = (ctypes.c_double() for _ in range(4))
            for glyph in title_glyphs:
                pdfium.raw.FPDFText_GetCharBox(textpage.raw, glyph["index"], ctypes.byref(left), ctypes.byref(right), ctypes.byref(bottom), ctypes.byref(top))
                function_gap = (previous and previous["text"].isascii() and previous["text"].isalpha()
                                and glyph["text"].isascii() and glyph["text"].isalpha()
                                and "KaTeX_Main" in previous["fontname"]
                                and "KaTeX_Math" in glyph.get("fontname", ""))
                if previous and (left.value - previous["right"] > .23 * min(glyph["size"], previous["size"]) or function_gap):
                    parts.append(" ")
                parts.append(glyph["text"])
                previous = {"right": right.value, "size": glyph["size"], "text": glyph["text"], "fontname": glyph.get("fontname", "")}
            title = "".join(parts)
            title = re.sub(r"^(\d+\.\d+)\s*(?=[^\d.])", r"\1 ", title)
            title = re.sub(r"^(第\d+章)\s*(?=.)", r"\1 ", title)
            if not title:
                continue
            candidates.append({"title": title, "page": page_index,
                               "top": min(page.get_height(), baseline + size + 10),
                               "baseline": baseline, "size": size, "kind": "subheading"})
        candidates.sort(key=lambda entry: -entry["baseline"])
        for entry in candidates:
            if headings and headings[-1]["page"] == page_index:
                previous = headings[-1]
                gap = previous["baseline"] - entry["baseline"]
                if abs(previous["size"] - entry["size"]) < .8 and gap < 1.8 * entry["size"]:
                    previous["title"] += " " + entry["title"]
                    previous["baseline"] = entry["baseline"]
                    continue
            headings.append(entry)
        textpage.close()
        page.close()
        if (page_index + 1) % 100 == 0:
            print(f"Scanned {page_index + 1}/{stop} body pages", flush=True)
    return headings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan-only", action="store_true")
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    original_stat = PDF.stat()
    reader = PdfReader(PDF)
    original = old_tree(reader, reader.outline)
    notes = next(entry for entry in original if entry["title"] == "译注汇总")
    stop = notes["page"]
    with pdfium.PdfDocument(PDF) as document:
        detected = scan(document, stop)
    (WORK / "detected-body-headings.json").write_text(json.dumps(detected, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"detected": len(detected), "notes_start_page": stop + 1,
                      "continuity": [h for h in detected if "连续函数" in h["title"]]}, ensure_ascii=False))
    if args.scan_only:
        return

    used = set()
    for entry in original:
        options = [(i, candidate) for i, candidate in enumerate(detected)
                   if candidate["page"] == entry["page"] and compact(candidate["title"]) == compact(entry["title"])]
        if not options:
            options = [(i, candidate) for i, candidate in enumerate(detected)
                       if candidate["page"] == entry["page"]
                       and compact(candidate["title"]).startswith(compact(entry["title"]))
                       and abs(candidate["top"] - entry["top"]) < 18]
        if not options:
            continue
        index, candidate = min(options, key=lambda pair: abs(pair[1]["top"] - entry["top"]))
        entry["top"] = candidate["top"]
        if entry["depth"] > 0 and not re.match(r"^\d+\.\d+", entry["title"]):
            entry["title"] = candidate["title"]
        used.add(index)
    ordered = sorted(original, key=lambda entry: (entry["page"], -entry["top"], entry["depth"]))
    additional = []
    per_parent = {}
    for index, candidate in enumerate(detected):
        if index in used:
            continue
        preceding = [entry for entry in ordered if (entry["page"], -entry["top"]) <= (candidate["page"], -candidate["top"])]
        if not preceding:
            continue
        parent = preceding[-1]
        if parent["page"] >= stop:
            continue
        key = id(parent)
        stack = per_parent.setdefault(key, [])
        while stack and stack[-1]["size"] <= candidate["size"] + .8:
            stack.pop()
        candidate["parent"] = stack[-1] if stack else parent
        candidate["depth"] = candidate["parent"]["depth"] + 1
        stack.append(candidate)
        additional.append(candidate)

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.root_object.pop(NameObject("/Outlines"), None)
    all_entries = sorted(original + additional, key=lambda entry: (entry["page"], -entry["top"], entry["depth"]))
    handles = {}
    def emit(entry):
        if id(entry) in handles:
            return handles[id(entry)]
        parent = emit(entry["parent"]) if entry["parent"] is not None else None
        handles[id(entry)] = writer.add_outline_item(entry["title"], entry["page"], parent=parent,
            fit=Fit.xyz(left=0, top=entry["top"], zoom=None), is_open=entry["depth"] == 0)
        return handles[id(entry)]
    for entry in all_entries:
        emit(entry)
    writer.page_mode = "/UseOutlines"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    staged = WORK / f"expanded-outline-{timestamp}.pdf"
    backup = WORK / f"GilbertStrang-Calculus.before-subheadings-{timestamp}.pdf"
    shutil.copy2(PDF, backup)
    writer.write(staged)
    result = PdfReader(staged)
    assert len(result.pages) == len(reader.pages)
    for before, after in zip(reader.pages, result.pages):
        assert before.get_contents().get_data() == after.get_contents().get_data()
    verified = old_tree(result, result.outline)
    assert len(verified) == len(all_entries)
    for entry in verified:
        if entry["title"] != "译注汇总":
            assert entry["page"] < stop
    with pdfium.PdfDocument(staged) as document:
        bookmarks = list(document.get_toc(max_depth=16))
        assert len(bookmarks) == len(all_entries)
        for bookmark, entry in zip(bookmarks, verified):
            assert bookmark.get_title() == entry["title"]
            assert bookmark.get_dest().get_index() == entry["page"]
    assert PDF.stat().st_mtime_ns == original_stat.st_mtime_ns and PDF.stat().st_size == original_stat.st_size, "PDF changed concurrently; staged output has not replaced it"
    os.replace(staged, PDF)
    report = {"pdf": str(PDF), "backup": str(backup), "pages": len(result.pages),
              "bookmarks": len(all_entries), "added_subheadings": len(additional),
              "notes_start_page": stop + 1, "page_content_streams_unchanged": True,
              "entries": [{key: value for key, value in entry.items() if key != "parent"} for entry in verified]}
    (WORK / "expanded-outline-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "entries"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
