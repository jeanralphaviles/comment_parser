#!/usr/bin/python
"""This module provides methods for parsing comments from Python scripts."""

import io
import tokenize
from comment_parser.parsers import common

def extract_comments(code):
  """Extracts a list of comments from the given Python script.

  Comments are identified using the tokenize module.
    - Single-lined comments which begin with the '#' character and end with a line-break.
    - Multi-lined comments or docstrings, which are just triple-quoted strings (start 
      and end with ''' or 3 of these "), are told apart from regular strings by the 
      type of the previous token which should be a line-break or an indentation (NEWLINE, 
      NL, INDENT or DEDENT) or no token at all (it would mean it's the fisrt thing in 
      the script). Even in cases like this: 
        
        my_string = \
        '''this should not be considered a comment'''

        my_string = \
          '''this should not either''' # <- notice the increasing indentation

        my_string = \
            '''weird syntax anyway''' # <- but still valid indentation
      
      the previous token to the string is the '=' operator and not a line-break or an  
      indentation. That way, only triple-quoted strings preceded by a line-break, an 
      indentation, or no token, will be considered intended as comments.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code.
  Raises:
    tokenize.TokenError
  """
  triplequotes = ['"""', "'''"]
  multicommprevnums = [tokenize.ENCODING, tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT]
  prevtoknum = None # Stores the previous token's type.
  comments = []
  tokens = tokenize.tokenize(io.BytesIO(code.encode()).readline)
  for toknum, tokstring, tokloc, _, _ in tokens:
    # Single-lined comment.
    if toknum is tokenize.COMMENT:
      # Removes leading '#' character.
      tokstring = tokstring[1:]
      comments.append(common.Comment(tokstring, tokloc[0], False))
      continue
    # Multi-lined comment.
    if toknum is tokenize.STRING:
      if tokstring[:3] in triplequotes and tokstring[-3:] in triplequotes:
        if (not prevtoknum) or prevtoknum in multicommprevnums:
          # Removes the leading and preceding 3ple quotes (""" or ''').
          tokstring = tokstring[3:-3]
          comments.append(common.Comment(tokstring, tokloc[0], True))
    prevtoknum = toknum
  return comments
