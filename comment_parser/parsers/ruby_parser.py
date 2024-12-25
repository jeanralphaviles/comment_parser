#!/usr/bin/python
"""This module provides methods for parsing comments from Ruby code."""

import re
from bisect import bisect_left
from typing import List
from comment_parser.parsers import common


def extract_comments(code: str) -> List[common.Comment]:
    """Extracts a list of comments from the given Ruby source code.

  Comments are represented with the Comment class found in the common module.

  Ruby comments start with a '#' character and run to the end of the line,
  http://ruby-doc.com/docs/ProgrammingRuby.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code..
  """
    pattern = r"""
    (?P<literal> ([\"'])((?:\\\2|(?:(?!\2)).)*)(\2)) |
    (?P<single> \#(?P<single_content>.*?)$)
  """
    compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

    lines_indexes = []
    for match in re.finditer(r"$", code, re.M):
        lines_indexes.append(match.start())

    comments = []
    for match in compiled.finditer(code):
        kind = match.lastgroup

        start_character = match.start()
        line_no = bisect_left(lines_indexes, start_character)

        if kind == "single":
            comment_content = match.group("single_content")
            comment = common.Comment(comment_content, line_no + 1)
            comments.append(comment)

    return comments
