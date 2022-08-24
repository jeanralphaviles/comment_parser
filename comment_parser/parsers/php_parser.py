#!/usr/bin/python
"""This module provides methods for parsing comments from PHP.

Works with:
  PHP
"""

import re
from bisect import bisect_left
from comment_parser.parsers import common


def extract_comments(code):
  """Extracts a list of comments from the given PHP source code.

  Comments are represented with the Comment class found in the common module.
  PHP comments come in two forms, single and multi-line comments.
    - Single-line comments begin with '//' or '#' and continue to the end of line.
    - Multi-line comments begin with '/*' and end with '*/' and can span
      multiple lines of code. If a multi-line comment does not terminate
      before EOF is reached, then an exception is raised.

  Note that this doesn't take language-specific preprocessor directives into
  consideration.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code.
  Raises:
    common.UnterminatedCommentError: Encountered an unterminated multi-line
      comment.
  """
  pattern = r"""
    (?P<literal> (?:([\"'])((?:\\\2|(?:(?!\2)).|\n)*)(\2))|\?>((?!<\?php\s).|\n)*<\?php\s|<<<('?)(([a-zA-Z0-9_]|[^\x00-\x7F])([a-zA-Z0-9_]|[^\x00-\x7F])*)\6((?!^\7;?$)(.|\n))*^\7;?$) |
    (?P<single> (?://|\#)(?P<single_content>.*)?$) |
    (?P<multi> /\*(?P<multi_content>(.|\n)*?)?\*/) |
    (?P<error> /\*(.*)?)
  """

  compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)
  # The regex recognizes stuff between ?> and <?php as literal
  # The following wrapping sets the expectation to be outside of php tags at the start
  # and deals with the state, where the php tag is not open at the end of the file
  code = "?>\n" + code + "\n<?php "

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
      comment = common.Comment(comment_content,
                               line_no)  # Line number is increased by wrapping
      comments.append(comment)
    elif kind == "multi":
      comment_content = match.group("multi_content")
      comment = common.Comment(
          comment_content, line_no,
          multiline=True)  # Line number is increased by wrapping
      comments.append(comment)
    elif kind == "error":
      raise common.UnterminatedCommentError()

  return comments
