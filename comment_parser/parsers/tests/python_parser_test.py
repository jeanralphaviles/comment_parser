#!/usr/bin/python
"""Tests for comment_parser.parsers.python_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import python_parser


class PythonParserTest(unittest.TestCase):

  def testComment(self):
    code = '# comment'
    comments = python_parser.extract_comments(code)
    expected = [common.Comment(code[1:], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testCommentInSingleQuotedString(self):
    code = "'this is # not a comment'"
    comments = python_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testCommentInDoubleQuotedString(self):
    code = '"this is # not a comment"'
    comments = python_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testNestedStringSingleOutside(self):
    code = "'this is \"# not a comment\"'"
    comments = python_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testNestedStringDoubleOutside(self):
    code = '"this is \'# not a comment\'"'
    comments = python_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testEscapedSingleQuote(self):
    code = "\\'# this is a comment"
    comments = python_parser.extract_comments(code)
    expected = [common.Comment(code[3:], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testEscapedDoubleQuote(self):
    code = '\\"# this is a comment'
    comments = python_parser.extract_comments(code)
    expected = [common.Comment(code[3:], 1, multiline=False)]
    self.assertEqual(comments, expected)
