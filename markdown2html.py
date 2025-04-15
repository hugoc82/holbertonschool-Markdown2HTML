#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re


def convert_markdown_to_html(input_path, output_path):
    """Reads a Markdown file and writes converted HTML headings to output."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    html_lines = []

    for line in lines:
        # Remove trailing newline and spaces
        line = line.rstrip()
        # Match headings from # to ######
        match = re.match(r'^(#{1,6})\s+(.*)', line)
        if match:
            heading_level = len(match.group(1))
            content = match.group(2)
            html_lines.append(f"<h{heading_level}>{content}</h{heading_level}>")
        else:
            # If not a heading, ignore (for now)
            continue

    # Write the result to the output file
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
