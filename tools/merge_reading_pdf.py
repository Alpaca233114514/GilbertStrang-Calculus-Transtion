"""Merge the reviewed section PDFs and resolve heading/contents links."""

from pathlib import Path
import io
import json
import re

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, Fit, FloatObject, NameObject
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp/pdfs/faithfulness-20261029/build"
PREFIX = "https://calculus.invalid/"


def main():
    manifest = json.loads((WORK / "manifest.json").read_text(encoding="utf-8"))
    assert not json.loads((WORK / "math_errors.json").read_text(encoding="utf-8"))
    assert not any(s["layout"]["badImages"] for s in manifest)
    readers = [PdfReader(s["pdf"]) for s in manifest]
    total = sum(len(r.pages) for r in readers)
    buffer = io.BytesIO()
    footer = canvas.Canvas(buffer)
    for index in range(total):
        footer.setPageSize((595.28, 841.89))
        if index:
            footer.setFillColorRGB(.35, .40, .44)
            footer.setFont("Helvetica", 9)
            footer.drawCentredString(297.64, 25, str(index))
        footer.showPage()
    footer.save()
    numbers = PdfReader(buffer)
    writer = PdfWriter()
    locations, pending = {}, []
    offset = 0
    for section, reader in zip(manifest, readers):
        section["start_page"] = offset + 1
        section["page_count"] = len(reader.pages)
        for page in reader.pages:
            page.merge_page(numbers.pages[offset])
            writer.add_page(page)
            offset += 1

    # Resolve links only after every destination page exists. / 全部页面加入后再解析跳转。
    for page_index, page in enumerate(writer.pages):
        retained = []
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            uri = str(annotation.get("/A", {}).get("/URI", ""))
            if uri.startswith(PREFIX + "heading/"):
                key = uri.rsplit("/", 1)[1]
                top = float(annotation["/Rect"][3])
                if key not in locations or page_index < locations[key][0] or (page_index == locations[key][0] and top > locations[key][1]):
                    locations[key] = (page_index, top)
            elif uri.startswith(PREFIX + "target/"):
                pending.append((page, annotation, uri.rsplit("/", 1)[1]))
                retained.append(ref)
            else:
                retained.append(ref)
        page[NameObject("/Annots")] = ArrayObject(retained)

    chapters, targets, entries = {}, {}, []
    labels = {"cover": "封面", "title": "扉页", "title_third": "第三版扉页"}
    for section in manifest:
        headings = section["layout"]["headings"]
        if not headings:
            title = labels.get(section["name"], section["name"])
            page = section["start_page"] - 1
            writer.add_outline_item(title, page)
            entries.append({"title": title, "page": page + 1, "kind": "front"})
            continue
        section_match = re.search(r"ch(\d+)_sec(\d+)", section.get("file", ""))
        section_key = (str(int(section_match[1])) + "." + str(int(section_match[2]))) if section_match else None
        chapter_handle = chapters.get(int(section_match[1])) if section_match else None
        anchor, stack, got_section = chapter_handle, [], False
        for heading in headings:
            page, top = locations[heading["id"]]
            title, level = heading["title"], heading["level"]
            chapter = re.match(r"^第\s*(\d+)\s*章", title)
            section_heading = re.match(r"^(\d+\.\d+)(?!\d)", title)
            if chapter:
                handle = writer.add_outline_item(title, page, fit=Fit.xyz(0, top, None))
                chapters[int(chapter[1])] = handle
                targets["ch" + str(int(chapter[1]))] = (page, top)
                anchor, chapter_handle, stack = handle, handle, []
                kind = "chapter"
            elif section_key and section_heading and section_heading[1] == section_key and not got_section:
                if section_key == "0.4":
                    if "0.4" not in targets:
                        anchor = writer.add_outline_item("0.4 视频讲座概要与练习题", page, parent=chapter_handle, fit=Fit.xyz(0, top, None))
                        chapters["part04"] = anchor
                    else:
                        anchor = chapters["part04"]
                    handle = writer.add_outline_item(title, page, parent=anchor, fit=Fit.xyz(0, top, None))
                else:
                    handle = writer.add_outline_item(title, page, parent=chapter_handle, fit=Fit.xyz(0, top, None))
                targets.setdefault(section_key, (page, top))
                anchor, stack, got_section = handle, [], True
                kind = "section"
            else:
                while stack and stack[-1][0] >= level:
                    stack.pop()
                parent = stack[-1][1] if stack else anchor
                handle = writer.add_outline_item(title, page, parent=parent, fit=Fit.xyz(0, top, None))
                stack.append((level, handle))
                kind = "subheading" if parent is not None else "front"
            entries.append({"title": title, "page": page + 1, "top": top, "kind": kind})

    for page, annotation, key in pending:
        target_page, top = targets[key]
        annotation.pop(NameObject("/A"), None)
        annotation[NameObject("/Dest")] = ArrayObject([
            writer.pages[target_page].indirect_reference,
            NameObject("/XYZ"), FloatObject(0), FloatObject(top), FloatObject(0),
        ])
    writer.add_metadata({"/Title": "微积分 · 中文译稿", "/Author": "Gilbert Strang", "/Subject": "Calculus 第三版中文译稿"})
    writer.page_mode = "/UseOutlines"
    output = WORK / "GilbertStrang-Calculus.pdf"
    writer.write(output)
    result = PdfReader(output)
    assert len(result.pages) == total
    def verify_outline(items):
        count = 0
        for item in items:
            if isinstance(item, list):
                count += verify_outline(item)
            else:
                assert 0 <= result.get_destination_page_number(item) < total
                count += 1
        return count
    bookmarks = verify_outline(result.outline)
    report = {"pdf": str(output), "pages": total, "bookmarks": bookmarks,
              "toc_links": len(pending), "sections": manifest, "entries": entries,
              "chapter_targets": {key: {"page": value[0] + 1, "top": value[1]} for key, value in targets.items()}}
    (WORK / "pdf_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pages": total, "bookmarks": bookmarks, "toc_links": len(pending), "output": str(output)}))


if __name__ == "__main__":
    main()
