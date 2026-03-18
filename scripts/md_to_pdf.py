#!/usr/bin/env python3
"""Markdown to HTML converter (no external deps), then uses Chrome headless for PDF."""
import re
import sys
import os
import subprocess
import tempfile

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    in_code = False
    in_blockquote = False
    table_header_done = False
    i = 0

    def inline(text):
        # Bold italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        # Images
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%">', text)
        return text

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith('```'):
            if not in_code:
                lang = line.strip()[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code = True
            else:
                html_lines.append('</code></pre>')
                in_code = False
            i += 1
            continue

        if in_code:
            html_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue

        # HR
        if re.match(r'^---+$', line.strip()) or re.match(r'^===+$', line.strip()):
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            html_lines.append('<hr>')
            i += 1
            continue

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            content = inline(m.group(2))
            anchor = re.sub(r'[^a-z0-9가-힣\s-]', '', m.group(2).lower()).strip().replace(' ', '-')
            html_lines.append(f'<h{level} id="{anchor}">{content}</h{level}>')
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            content = inline(line[1:].strip())
            html_lines.append(f'<blockquote><p>{content}</p></blockquote>')
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.match(r'^[\|\s\-:]+$', lines[i+1]):
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            html_lines.append('<table><thead><tr>')
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            for cell in cells:
                html_lines.append(f'<th>{inline(cell)}</th>')
            html_lines.append('</tr></thead><tbody>')
            in_table = True
            i += 2  # skip separator line
            continue

        if in_table and '|' in line:
            html_lines.append('<tr>')
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            for cell in cells:
                html_lines.append(f'<td>{inline(cell)}</td>')
            html_lines.append('</tr>')
            i += 1
            continue

        if in_table and '|' not in line:
            html_lines.append('</tbody></table>')
            in_table = False

        # Unordered list
        m = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if m:
            html_lines.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue

        # Ordered list
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            html_lines.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue

        # Empty line
        if line.strip() == '':
            html_lines.append('<br>')
            i += 1
            continue

        # Normal paragraph
        html_lines.append(f'<p>{inline(line)}</p>')
        i += 1

    if in_table:
        html_lines.append('</tbody></table>')
    if in_code:
        html_lines.append('</code></pre>')

    return '\n'.join(html_lines)


def wrap_html(body, title="Report"):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Sans KR', 'Malgun Gothic', '맑은 고딕', sans-serif;
    font-size: 13px;
    line-height: 1.8;
    color: #1a1a2e;
    padding: 20mm 20mm 20mm 20mm;
    max-width: 900px;
    margin: 0 auto;
  }}
  h1 {{ font-size: 24px; color: #0d47a1; border-bottom: 3px solid #0d47a1; padding-bottom: 8px; margin: 20px 0 12px; }}
  h2 {{ font-size: 18px; color: #1565c0; border-left: 4px solid #1565c0; padding-left: 10px; margin: 20px 0 10px; }}
  h3 {{ font-size: 15px; color: #1976d2; margin: 16px 0 8px; }}
  h4 {{ font-size: 13px; color: #1e88e5; margin: 12px 0 6px; }}
  p {{ margin: 6px 0; }}
  blockquote {{
    background: #e3f2fd;
    border-left: 4px solid #1565c0;
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 4px;
    font-style: italic;
  }}
  blockquote p {{ margin: 0; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 12px;
  }}
  th {{
    background: #1565c0;
    color: white;
    padding: 8px 10px;
    text-align: center;
    font-weight: bold;
  }}
  td {{
    padding: 6px 10px;
    border: 1px solid #ddd;
    text-align: center;
  }}
  tr:nth-child(even) td {{ background: #f5f8ff; }}
  tr:hover td {{ background: #e3f2fd; }}
  code {{
    background: #f4f4f4;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #c62828;
  }}
  pre {{
    background: #1a1a2e;
    color: #e0e0e0;
    padding: 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 12px 0;
  }}
  pre code {{
    background: none;
    color: inherit;
    font-size: 12px;
    padding: 0;
  }}
  a {{ color: #1565c0; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 16px 0; }}
  li {{ margin: 4px 0 4px 20px; }}
  img {{ max-width: 100%; margin: 10px 0; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
  strong {{ color: #0d47a1; }}
  @media print {{
    body {{ padding: 0; }}
    a {{ color: #1565c0; text-decoration: none; }}
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def convert(md_path, output_pdf=None):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    title = os.path.basename(md_path).replace('.md', '')
    body = md_to_html(md_text)
    html = wrap_html(body, title)

    # Save HTML temp file (WSL path → Windows path for Chrome)
    html_tmp = md_path.replace('.md', '_tmp.html')
    with open(html_tmp, 'w', encoding='utf-8') as f:
        f.write(html)

    if output_pdf is None:
        output_pdf = md_path.replace('.md', '.pdf')

    # Convert WSL path to Windows path
    wsl_to_win = subprocess.run(['wslpath', '-w', html_tmp], capture_output=True, text=True)
    win_html = wsl_to_win.stdout.strip()
    wsl_to_win2 = subprocess.run(['wslpath', '-w', output_pdf], capture_output=True, text=True)
    win_pdf = wsl_to_win2.stdout.strip()

    chrome_paths = [
        '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
        '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    ]
    chrome = next((p for p in chrome_paths if os.path.exists(p)), None)

    if not chrome:
        print(f"HTML saved to: {html_tmp}")
        print("Chrome not found. Please open the HTML file and print to PDF manually.")
        return

    print(f"Converting: {md_path} → {output_pdf}")
    cmd = [
        chrome,
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--run-all-compositor-stages-before-draw',
        '--print-to-pdf-no-header',
        f'--print-to-pdf={win_pdf}',
        f'file:///{win_html}',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0 and os.path.exists(output_pdf):
        print(f"PDF saved: {output_pdf}")
        print(f"Windows path: {win_pdf}")
        os.remove(html_tmp)
    else:
        print(f"Chrome error: {result.stderr[:300]}")
        print(f"HTML available at: {html_tmp}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    md_path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    convert(md_path, out)
