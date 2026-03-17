#!/usr/bin/python
"""This module provides support for parsing the Lisp family of languages

Works with:
  Lisp
  Scheme
  Racket
  Clojure (not including the (comment) form
  ... and other languages which use the leading ; as the comment form
"""

import re
from bisect import bisect_left
from typing import List 
from comment_parser.parsers import common 

def extract_comments(code: str) -> List[common.Comment]:
  """Extracts a list of comments from a given Lisp family source code.
  
  Comments are represented with the Comment class found in the common module.
  Lisp family comments come in a single form. Any string of characters begun with
  `;` it is considered to be a comment. Note that various languages in the lisp 
  family use multiple `;` to denote certain types of comments. For example, a 
  comment using a single `;` may just mean an inline comment, but two (`;;`) or 
  more `;`'s may be considered official documentation. This parser does not 
  differentiate between the various types of comments, but will consume many `;`
  characters and return the comment text

  Args:
    code (str): String containing code to extract comments from.
  Returns:
    List[common.Comment]: list of comments in the order that they appear in the 
      code
  """
  pattern = r"""
    (?P<literal> (\"([^\"\n])*\")+) |
    (?P<single> ;+(?P<single_content>.*)?$)
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