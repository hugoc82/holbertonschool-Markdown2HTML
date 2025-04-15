#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re


def convert_markdown_to_html(input_path, output_path):
    """Converts Markdown to HTML (headings, unordered & ordered lists)."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    html_lines = []
    in_ul = False
    in_ol = False

    for line in lines:
        line = line.rstrip()

        # Headings: #
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Unordered list: -
        ul_match = re.match(r'^-\s+(.*)', line)
        if ul_match:
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item = ul_match.group(1)
            html_lines.append(f"<li>{item}</li>")
            continue

        # Ordered list: *
        ol_match = re.match(r'^\*\s+(.*)', line)
        if ol_match:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            item = ol_match.group(1)
            html_lines.append(f"<li>{item}</li>")
            continue

        # If line is empty or unrecognized and we're in a list, close it
        if line == '':
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False

    # If file ends while in a list, close it
    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

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
