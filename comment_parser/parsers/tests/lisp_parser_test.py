#!/usr/bin/python
"""Tests for comment_parser.parsers.lisp_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import lisp_parser

class LispParerTest(unittest.TestCase):
    
  def testSimpleMain(self):
    code = "; this is a comment\n(format t \"Hello, World!\")"
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[1:19], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineComment(self):
    code = "; single line comment"
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[1:], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineCommentInStringLiteral(self):
    code = '(format t "; this is not a comment")'
    comments = lisp_parser.extract_comments(code)
    self.assertEqual(comments, [])
    
  def testMultipleCommentCharacters(self):
    code = ';; this is a comment'
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[2:], 1, False)]
    self.assertEqual(comments, expected)
  
  def testCommentsAfterLine(self):
    code = '(t format "Hello World") ; this is a comment'
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(' this is a comment', 1, False)]
    self.assertEqual(comments, expected)