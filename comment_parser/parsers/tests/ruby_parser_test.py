#!/usr/bin/python
"""Tests for comment_parser.parsers.ruby_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import ruby_parser


class ShellParserTest(unittest.TestCase):

    def testComment(self):
        code = '# comment'
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[1:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testCommentInSingleQuotedString(self):
        code = "'this is # not a comment'"
        comments = ruby_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testCommentInDoubleQuotedString(self):
        code = '"this is # not a comment"'
        comments = ruby_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testNestedStringSingleOutside(self):
        code = "'this is \"# not a comment\"'"
        comments = ruby_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testNestedStringDoubleOutside(self):
        code = '"this is \'# not a comment\'"'
        comments = ruby_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testEscapedSingleQuote(self):
        code = "\\'# this is a comment"
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testEscapedDoubleQuote(self):
        code = '\\"# this is a comment'
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testDoubleComment(self):
        code = '# this is not # another comment'
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[1:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testLiteralsSeparatedByComment(self):
        code = r"'This is' # 'a comment'"
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[11:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testDifferentLiteralsSeparatedByComment(self):
        code = r''''This is' # "a comment"'''
        comments = ruby_parser.extract_comments(code)
        expected = [common.Comment(code[11:], 1, multiline=False)]
        self.assertEqual(comments, expected)
