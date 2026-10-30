"""Normalize list punctuation and note headings for Scholar's computed outline.

Run after repair_pdf_navigation.py. Page positions, mathematical expressions,
and embedded bookmark destinations are retained. An original copy is saved.
"""

from datetime import datetime
import json
from pathlib import Path
import re
import shutil

from pypdf import PdfReader, PdfWriter
from pypdf._cmap import get_encoding
from pypdf.generic import ArrayObject, ByteStringObject, ContentStream, FloatObject, NameObject


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/GilbertStrang-Calculus.pdf"
WORK = ROOT / "tmp/pdfs/navigation"


def raw_bytes(value):
    return value.original_bytes if hasattr(value, "original_bytes") else bytes(value)


def glyph_width(font, code):
    descendant = font["/DescendantFonts"][0].get_object()
    widths = descendant.get("/W", [])
    index = 0
    while index < len(widths):
        start, second = int(widths[index]), widths[index + 1]
        if isinstance(second, list):
            if start <= code < start + len(second):
                return float(second[code - start])
            index += 2
        else:
            if start <= code <= int(second):
                return float(widths[index + 2])
            index += 3
    return float(descendant.get("/DW", 1000))


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    source = PdfReader(OUTPUT)
    writer = PdfWriter()
    writer.clone_document_from_reader(source)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = WORK / f"GilbertStrang-Calculus.before-scholar-{timestamp}.pdf"
    shutil.copy2(OUTPUT, backup)
    font_cache = {}
    fallback = {}

    def font_info(ref):
        font = ref.get_object()
        key = ref.idnum if hasattr(ref, "idnum") else id(font)
        if key not in font_cache:
            if "MicrosoftYaHei" not in str(font.get("/BaseFont", "")):
                font_cache[key] = None
            else:
                encoding, mapping = get_encoding(font)
                if encoding != "utf-16-be":
                    font_cache[key] = None
                    return None
                reverse = {value: ord(code) for code, value in mapping.items()
                           if isinstance(code, str) and len(code) == 1}
                font_cache[key] = (font, mapping, reverse)
        return font_cache[key]

    for page in writer.pages:
        for ref in page["/Resources"].get("/Font", {}).values():
            info = font_info(ref)
            if info and ")" in info[2]:
                kind = "Bold" if "Bold" in str(info[0]["/BaseFont"]) else "Regular"
                fallback.setdefault(kind, (ref, info))
        if len(fallback) == 2:
            break
    assert len(fallback) == 2

    edits, note_headings, first_section = [], 0, 0
    for page_index, page in enumerate(writer.pages):
        fonts = page["/Resources"].get("/Font", {})
        stream = ContentStream(page.get_contents(), writer)
        operations = stream.operations
        replacements = {}
        group_start = None
        font_name, font_size = None, None
        for index, (args, op) in enumerate(operations):
            if op == b"BT":
                group_start = index
            elif op == b"Tf":
                font_name, font_size = args
            elif op == b"ET" and group_start is not None:
                records, text, group_font = [], "", None
                for position in range(group_start, index):
                    values, operator = operations[position]
                    if operator == b"Tf":
                        group_font, group_size = values
                    if operator != b"Tj" or group_font not in fonts:
                        continue
                    info = font_info(fonts[group_font])
                    if not info:
                        continue
                    raw = raw_bytes(values[0])
                    assert len(raw) % 2 == 0
                    for byte_index in range(0, len(raw), 2):
                        code = int.from_bytes(raw[byte_index:byte_index + 2], "big")
                        char = info[1].get(chr(code), "\ufffd")
                        text += char
                        records.append((position, byte_index, group_font, group_size, info, code))
                if not records:
                    group_start = None
                    continue
                if page_index < 850 and (match := re.match(r"^(\d{1,2})\.(?!\d)", text)):
                    position, byte_index, name, size, info, dot = records[len(match[1])]
                    raw = raw_bytes(operations[position][0][0])
                    kind = "Bold" if "Bold" in str(info[0]["/BaseFont"]) else "Regular"
                    if ")" in info[2]:
                        destination_name, destination_info = name, info
                    else:
                        destination_name = NameObject("/Nav" + kind)
                        ref, destination_info = fallback[kind]
                        fonts[destination_name] = ref
                    parenthesis = destination_info[2][")"]
                    adjustment = glyph_width(destination_info[0], parenthesis) - glyph_width(info[0], dot)
                    patch = []
                    if byte_index:
                        patch.append(([ByteStringObject(raw[:byte_index])], b"Tj"))
                    if destination_name != name:
                        patch.append(([destination_name, size], b"Tf"))
                    patch.append(([ArrayObject([ByteStringObject(parenthesis.to_bytes(2, "big")),
                                                FloatObject(adjustment)])], b"TJ"))
                    if destination_name != name:
                        patch.append(([name, size], b"Tf"))
                    if byte_index + 2 < len(raw):
                        patch.append(([ByteStringObject(raw[byte_index + 2:])], b"Tj"))
                    replacements[position] = patch
                    edits.append({"page": page_index + 1, "before": text[:100],
                                  "after": text[:len(match[1])] + ")" + text[len(match[1]) + 1:100]})

                scale = None
                if page_index >= 850 and font_size and 20.9 < float(font_size) < 21.8:
                    scale = 14 / float(font_size)
                    note_headings += 1
                elif page_index == 16 and re.match(r"^0\.1\s*路程", text):
                    scale = 23 / 16
                    first_section += 1
                if scale is not None:
                    # Scale the whole text matrix; individual glyph spacing follows it.
                    # 整体缩放文字矩阵，让逐字定位随字体同步缩放。
                    for position in range(group_start, index):
                        values, operator = operations[position]
                        if operator == b"Tm":
                            operations[position] = ([FloatObject(float(v) * scale) for v in values[:4]] + list(values[4:]), operator)
                group_start = None
        if replacements:
            stream.operations = [item for index, operation in enumerate(operations)
                                 for item in replacements.get(index, [operation])]
        page.replace_contents(stream)
        if (page_index + 1) % 100 == 0:
            print(f"Normalized {page_index + 1}/{len(writer.pages)} pages", flush=True)
    assert first_section == 1 and note_headings >= 60
    staged = WORK / f"scholar-normalized-{timestamp}.pdf"
    writer.write(staged)
    check = PdfReader(staged)
    assert len(check.pages) == len(source.pages)
    assert len(list(check.outline)) == len(source.outline)
    shutil.copy2(staged, OUTPUT)
    summary = {"backup": str(backup), "pages": len(check.pages), "list_punctuation_changes": len(edits),
               "note_headings_demoted": note_headings, "first_section_heading_enlarged": first_section,
               "edits": edits}
    (WORK / "scholar-normalization.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "edits"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
