#!/usr/bin/python
"""Tests for comment_parser.parsers.c_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import c_parser


class CParserTest(unittest.TestCase):

  def testSimpleMain(self):
    code = "// this is a comment\nint main() {\nreturn 0;\n}\n"
    comments = c_parser.extract_comments(code)
    expected = [common.Comment(code[2:20], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = c_parser.extract_comments(code)
    expected = [common.Comment(code[2:], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInStringLiteral(self):
    code = 'char* msg = "// this is not a comment"'
    comments = c_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '/* multiline\ncomment */'
    comments = c_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = "/***************/"
    comments = c_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInStringLiteral(self):
    code = 'char* msg = "/* This is not a\\nmultiline comment */"'
    comments = c_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'int a = 1; /* Unterminated\\n comment'
    self.assertRaises(common.UnterminatedCommentError,
                      c_parser.extract_comments, code)

  def testMultipleMultilineComments(self):
    code = '/* abc */ /* 123 */'
    comments = c_parser.extract_comments(code)
    expected = [
        common.Comment(' abc ', 1, multiline=True),
        common.Comment(' 123 ', 1, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testStringThenComment(self):
    code = r'"" /* "abc */'
    comments = c_parser.extract_comments(code)
    expected = [
        common.Comment(' "abc ', 1, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    code = r'" \" /* \" "'
    comments = c_parser.extract_comments(code)
    self.assertEqual(comments, [])
