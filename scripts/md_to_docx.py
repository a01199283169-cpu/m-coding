#!/usr/bin/env python3
"""Markdown → DOCX converter (stdlib only, no external deps)."""
import re, sys, os, zipfile, io
from datetime import datetime

# ── DOCX XML templates ─────────────────────────────────────────────────────

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    Target="styles.xml"/>
  <Relationship Id="rId2"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"
    Target="settings.xml"/>
</Relationships>'''

SETTINGS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="708"/>
  <w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>
</w:settings>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="맑은 고딕" w:hAnsi="맑은 고딕" w:cs="맑은 고딕"/>
      <w:sz w:val="22"/><w:szCs w:val="22"/>
      <w:lang w:val="ko-KR" w:eastAsia="ko-KR"/>
    </w:rPr></w:rPrDefault>
  </w:docDefaults>

  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120"/></w:pPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:numPr><w:ilvl w:val="0"/></w:numPr>
      <w:spacing w:before="240" w:after="120"/>
      <w:jc w:val="left"/>
      <w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="1F3A8A"/></w:pBdr>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="맑은 고딕" w:hAnsi="맑은 고딕"/>
      <w:b/><w:sz w:val="36"/><w:szCs w:val="36"/>
      <w:color w:val="1F3A8A"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/>
      <w:pBdr><w:left w:val="single" w:sz="12" w:space="8" w:color="1565C0"/></w:pBdr>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="맑은 고딕" w:hAnsi="맑은 고딕"/>
      <w:b/><w:sz w:val="28"/><w:szCs w:val="28"/>
      <w:color w:val="1565C0"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="맑은 고딕" w:hAnsi="맑은 고딕"/>
      <w:b/><w:sz w:val="24"/><w:szCs w:val="24"/>
      <w:color w:val="1976D2"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Code">
    <w:name w:val="Code"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:shd w:val="clear" w:color="auto" w:fill="F4F4F4"/>
      <w:spacing w:before="80" w:after="80"/>
      <w:ind w:left="200" w:right="200"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>
      <w:sz w:val="18"/><w:szCs w:val="18"/>
      <w:color w:val="C62828"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="BlockQuote">
    <w:name w:val="BlockQuote"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:ind w:left="400"/>
      <w:shd w:val="clear" w:color="auto" w:fill="E3F2FD"/>
      <w:pBdr><w:left w:val="single" w:sz="16" w:space="8" w:color="1565C0"/></w:pBdr>
    </w:pPr>
    <w:rPr><w:i/><w:color w:val="1A237E"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="440" w:hanging="220"/><w:spacing w:after="60"/></w:pPr>
  </w:style>

  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top    w:val="single" w:sz="4" w:color="BBBBBB"/>
        <w:left   w:val="single" w:sz="4" w:color="BBBBBB"/>
        <w:bottom w:val="single" w:sz="4" w:color="BBBBBB"/>
        <w:right  w:val="single" w:sz="4" w:color="BBBBBB"/>
        <w:insideH w:val="single" w:sz="4" w:color="BBBBBB"/>
        <w:insideV w:val="single" w:sz="4" w:color="BBBBBB"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''

# ── Helpers ────────────────────────────────────────────────────────────────

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def esc(text):
    return (text.replace("&","&amp;").replace("<","&lt;")
                .replace(">","&gt;").replace('"',"&quot;"))

def inline_xml(text):
    """Convert inline markdown to runs XML."""
    runs = []
    i = 0
    buf = ""

    def flush(buf, bold=False, italic=False, code=False):
        if not buf: return ""
        rpr = "<w:rPr>"
        if bold:   rpr += "<w:b/>"
        if italic: rpr += "<w:i/>"
        if code:
            rpr += '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>'
            rpr += "<w:sz w:val=\"18\"/><w:color w:val=\"C62828\"/>"
        rpr += "</w:rPr>"
        safe = esc(buf).replace("\n","<w:br/>")
        return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{safe}</w:t></w:r>"

    # Simple state machine for *** ** * `
    pattern = re.compile(r'(`[^`]+`|\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|\[([^\]]+)\]\(([^)]+)\))')
    pos = 0
    result = ""
    for m in pattern.finditer(text):
        # flush literal text before match
        result += flush(text[pos:m.start()])
        s = m.group(0)
        if s.startswith('`'):
            result += flush(s[1:-1], code=True)
        elif s.startswith('***'):
            result += flush(s[3:-3], bold=True, italic=True)
        elif s.startswith('**'):
            result += flush(s[2:-2], bold=True)
        elif s.startswith('*'):
            result += flush(s[1:-1], italic=True)
        elif s.startswith('['):
            link_text = m.group(2)
            link_url  = m.group(3)
            result += f'<w:r><w:rPr><w:rStyle w:val="Hyperlink"/><w:color w:val="1565C0"/><w:u w:val="single"/></w:rPr><w:t>{esc(link_text)}</w:t></w:r>'
        pos = m.end()
    result += flush(text[pos:])
    return result

def para(text, style="Normal", indent=None, shd=None):
    ppr = f'<w:pStyle w:val="{style}"/>'
    if indent: ppr += indent
    if shd: ppr += shd
    body = inline_xml(text)
    return f"<w:p><w:pPr>{ppr}</w:pPr>{body}</w:p>"

def hr():
    return '''<w:p><w:pPr>
      <w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="CCCCCC"/></w:pBdr>
      <w:spacing w:before="60" w:after="60"/>
    </w:pPr></w:p>'''

# ── Table builder ──────────────────────────────────────────────────────────

def build_table(rows):
    xml = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9360" w:type="dxa"/><w:tblLook w:val="04A0"/></w:tblPr><w:tblGrid>'
    cols = max(len(r) for r in rows)
    col_w = 9360 // cols
    xml += f'<w:gridCol w:w="{col_w}"/>' * cols
    xml += '</w:tblGrid>'
    for i, row in enumerate(rows):
        xml += '<w:tr>'
        for cell in row:
            is_header = (i == 0)
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="1F3A8A"/>' if is_header else ''
            tc_pr = f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>{shd}</w:tcPr>'
            rpr = "<w:rPr><w:b/><w:color w:val=\"FFFFFF\"/></w:rPr>" if is_header else "<w:rPr/>"
            cell_body = f"<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(cell.strip())}</w:t></w:r>"
            jc = '<w:jc w:val="center"/>' if is_header else '<w:jc w:val="left"/>'
            ppr = f'<w:pPr><w:pStyle w:val="Normal"/>{jc}</w:pPr>'
            xml += f'<w:tc>{tc_pr}<w:p>{ppr}{cell_body}</w:p></w:tc>'
        xml += '</w:tr>'
    xml += '</w:tbl><w:p/>'
    return xml

# ── Markdown parser ────────────────────────────────────────────────────────

def parse_md(md_text):
    lines = md_text.split('\n')
    body_xml = ""
    i = 0
    in_code = False
    code_buf = []
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            body_xml_parts = build_table(table_rows)
            table_rows = []
            return body_xml_parts
        return ""

    parts = []

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                for cl in code_buf:
                    parts.append(para(cl, style="Code"))
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # HR
        if re.match(r'^-{3,}$', line.strip()):
            parts.append(flush_table())
            parts.append(hr())
            i += 1
            continue

        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            parts.append(flush_table())
            lvl = len(m.group(1))
            style = {1:"Heading1",2:"Heading2",3:"Heading3"}.get(lvl,"Heading3")
            parts.append(para(m.group(2), style=style))
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            parts.append(flush_table())
            parts.append(para(line[1:].strip(), style="BlockQuote"))
            i += 1
            continue

        # Table
        if '|' in line:
            # Check if next line is separator
            if i+1 < len(lines) and re.match(r'^[\|\s\-:]+$', lines[i+1]):
                # Header row
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                table_rows = [cells]
                i += 2  # skip separator
                continue
            elif table_rows:
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                table_rows.append(cells)
                i += 1
                continue

        # Flush table if pipe line ended
        if table_rows and '|' not in line:
            parts.append(flush_table())

        # List item
        m = re.match(r'^\s*[-*+]\s+(.*)', line)
        if m:
            bullet = "•  " + m.group(1)
            parts.append(para(bullet, style="ListBullet"))
            i += 1
            continue

        m = re.match(r'^\s*\d+\.\s+(.*)', line)
        if m:
            parts.append(para(m.group(1), style="ListBullet"))
            i += 1
            continue

        # Empty
        if line.strip() == '':
            parts.append('<w:p/>')
            i += 1
            continue

        # Normal paragraph
        parts.append(para(line, style="Normal"))
        i += 1

    parts.append(flush_table())
    return "".join(p for p in parts if p)

# ── Document assembler ─────────────────────────────────────────────────────

def build_docx(md_path, out_path):
    with open(md_path, encoding='utf-8') as f:
        md = f.read()

    body = parse_md(md)
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
    {body}
  </w:body>
</w:document>'''

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/settings.xml', SETTINGS)

    with open(out_path, 'wb') as f:
        f.write(buf.getvalue())

    print(f"✓ DOCX saved: {out_path}")
    print(f"  Size: {os.path.getsize(out_path):,} bytes")

# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_docx.py <input.md> [output.docx]")
        sys.exit(1)
    md_in = sys.argv[1]
    docx_out = sys.argv[2] if len(sys.argv) > 2 else md_in.replace('.md', '.docx')
    build_docx(md_in, docx_out)
