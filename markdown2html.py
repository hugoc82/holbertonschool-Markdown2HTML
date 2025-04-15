#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os

if __name__ == "__main__":
    # Check if there are exactly 2 arguments (excluding the script name)
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input markdown file exists
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # If everything is OK, exit silently
    sys.exit(0)
