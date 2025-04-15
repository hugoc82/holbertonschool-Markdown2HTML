#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re


def format_text(text):
    """Replace Markdown bold and emphasis with HTML equivalents."""
    # Replace **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Replace __emphasis__
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def convert_markdown_to_html(input_path, output_path):
    """Converts Markdown to HTML: headings, lists, paragraphs, bold/emphasis."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    html_lines = []
    list_type = None
    paragraph_lines = []

    def flush_paragraph():
        """Flush paragraph block into HTML output."""
        if paragraph_lines:
            html_lines.append("<p>")
            for i, pline in enumerate(paragraph_lines):
                if i != 0:
                    html_lines.append("<br/>")
                html_lines.append(format_text(pline))
            html_lines.append("</p>")
            paragraph_lines.clear()

    for line in lines:
        line = line.rstrip()

        # Heading
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            flush_paragraph()
            if list_type:
                html_lines.append(f"</{list_type}>")
                list_type = None
            level = len(heading_match.group(1))
            content = format_text(heading_match.group(2))
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Unordered list (-)
        ul_match = re.match(r'^-\s+(.*)', line)
        if ul_match:
            flush_paragraph()
            if list_type == 'ol':
                html_lines.append("</ol>")
                list_type = None
            if list_type != 'ul':
                html_lines.append("<ul>")
                list_type = 'ul'
            item = format_text(ul_match.group(1))
            html_lines.append(f"<li>{item}</li>")
            continue

        # Ordered list (*)
        ol_match = re.match(r'^\*\s+(.*)', line)
        if ol_match:
            flush_paragraph()
            if list_type == 'ul':
                html_lines.append("</ul>")
                list_type = None
            if list_type != 'ol':
                html_lines.append("<ol>")
                list_type = 'ol'
            item = format_text(ol_match.group(1))
            html_lines.append(f"<li>{item}</li>")
            continue

        # Empty line = block separation
        if line.strip() == '':
            if list_type:
                html_lines.append(f"</{list_type}>")
                list_type = None
            flush_paragraph()
            continue

        # Otherwise: part of a paragraph
        paragraph_lines.append(line)

    # Final flush
    if list_type:
        html_lines.append(f"</{list_type}>")
    flush_paragraph()

    # Write to output file
    with open(output_path, 'w') as f:
        for line in html_lines:
            f.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
