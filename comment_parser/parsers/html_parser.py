#!/usr/bin/python
"""This module provides methods for parsing comments from HTML family languages.

Works with:
  HTML
  XML
"""

import re
from bisect import bisect_left
from typing import List
from comment_parser.parsers import common


def extract_comments(code: str) -> List[common.Comment]:
    """Extracts a list of comments from the given HTML family source code.

  Comments are represented with the Comment class found in the common module.
  HTML family comments come in one form, comprising all text within '<!--' and
  '-->' markers. Comments cannot be nested.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code..
  Raises:
    common.UnterminatedCommentError: Encountered an unterminated multi-line
      comment.
  """
    pattern = r"""
    (?P<literal> (\"([^\"\n])*\")+) |
    (?P<single> <!--(?P<single_content>.*?)-->) |
    (?P<multi> <!--(?P<multi_content>(.|\n)*?)?-->) |
    (?P<error> <!--(.*)?)
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
        elif kind == "multi":
            comment_content = match.group("multi_content")
            comment = common.Comment(comment_content,
                                     line_no + 1,
                                     multiline=True)
            comments.append(comment)
        elif kind == "error":
            raise common.UnterminatedCommentError()

    return comments
