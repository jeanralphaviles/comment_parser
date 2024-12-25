#!/usr/bin/python
"""This module provides methods for parsing comments from Python scripts."""

import io
import tokenize
from typing import List
from comment_parser.parsers import common


def extract_comments(code: str) -> List[common.Comment]:
    """Extracts a list of comments from the given Python script.

  Comments are identified using the tokenize module. Does not include function,
  class, or module docstrings. All comments are single line comments.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code.
  Raises:
    tokenize.TokenError
  """
    comments = []
    tokens = tokenize.tokenize(io.BytesIO(code.encode()).readline)
    for toknum, tokstring, tokloc, _, _ in tokens:
        if toknum is tokenize.COMMENT:
            # Removes leading '#' character.
            tokstring = tokstring[1:]
            comments.append(common.Comment(tokstring, tokloc[0], False))
    return comments
