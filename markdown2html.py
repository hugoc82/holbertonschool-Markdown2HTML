#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re


def convert_markdown_to_html(input_path, output_path):
    """Converts Markdown content to HTML (headings and unordered lists only)."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    html_lines = []
    in_list = False  # Flag to check if we're inside a <ul>

    for line in lines:
        line = line.rstrip()

        # Check for headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Check for list items
        list_match = re.match(r'^-\s+(.*)', line)
        if list_match:
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = list_match.group(1)
            html_lines.append(f"<li>{item}</li>")
            continue

        # If line is empty or unrelated, and we were in a list, close it
        if in_list and line == '':
            html_lines.append("</ul>")
            in_list = False

    # If file ends while in a list, close it
    if in_list:
        html_lines.append("</ul>")

    # Write result to output file
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
