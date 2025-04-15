#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re


def convert_markdown_to_html(input_path, output_path):
    """Converts Markdown to HTML: handles headings, unordered and ordered lists."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    html_lines = []
    list_type = None  # can be 'ul' or 'ol'

    for line in lines:
        line = line.rstrip()

        # Match heading
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            # Close open list
            if list_type:
                html_lines.append(f"</{list_type}>")
                list_type = None
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Match unordered list (-)
        ul_match = re.match(r'^-\s+(.*)', line)
        if ul_match:
            if list_type == 'ol':
                html_lines.append("</ol>")
                list_type = None
            if list_type != 'ul':
                html_lines.append("<ul>")
                list_type = 'ul'
            item = ul_match.group(1)
            html_lines.append(f"<li>{item}</li>")
            continue

        # Match ordered list (*)
        ol_match = re.match(r'^\*\s+(.*)', line)
        if ol_match:
            if list_type == 'ul':
                html_lines.append("</ul>")
                list_type = None
            if list_type != 'ol':
                html_lines.append("<ol>")
                list_type = 'ol'
            item = ol_match.group(1)
            html_lines.append(f"<li>{item}</li>")
            continue

        # Any other line or empty line ends a list
        if list_type:
            html_lines.append(f"</{list_type}>")
            list_type = None

    # Close list at EOF if needed
    if list_type:
        html_lines.append(f"</{list_type}>")

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
