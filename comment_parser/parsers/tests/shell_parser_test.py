#!/usr/bin/python
"""Tests for comment_parser.parsers.shell_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import shell_parser


class ShellParserTest(unittest.TestCase):

    def testComment(self):
        code = '# comment'
        comments = shell_parser.extract_comments(code)
        expected = [common.Comment(code[1:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testEscapedComment(self):
        code = r'\# not a comment'
        comments = shell_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testCommentInSingleQuotedString(self):
        code = "'this is # not a comment'"
        comments = shell_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testCommentInDoubleQuotedString(self):
        code = '"this is # not a comment"'
        comments = shell_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testNestedStringSingleOutside(self):
        code = "'this is \"# not a comment\"'"
        comments = shell_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testNestedStringDoubleOutside(self):
        code = '"this is \'# not a comment\'"'
        comments = shell_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testEscapedSingleQuote(self):
        code = "\\'# this is a comment"
        comments = shell_parser.extract_comments(code)
        expected = [common.Comment(code[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testEscapedDoubleQuote(self):
        code = '\\"# this is a comment'
        comments = shell_parser.extract_comments(code)
        expected = [common.Comment(code[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)
