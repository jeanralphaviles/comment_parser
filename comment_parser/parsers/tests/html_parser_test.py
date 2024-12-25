#!/usr/bin/python
"""Tests for comment_parser.parsers.html_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import html_parser


class ShellParserTest(unittest.TestCase):

    def testComment(self):
        code = '<!--comment-->'
        comments = html_parser.extract_comments(code)
        expected = [common.Comment('comment', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testMultilineComment(self):
        code = '<!--multi-line\ncomment-->'
        comments = html_parser.extract_comments(code)
        expected = [common.Comment('multi-line\ncomment', 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testTwoSeparateSingleComment(self):
        code = '<!--comment1-->\n<!--comment2-->'
        comments = html_parser.extract_comments(code)
        expected = [
            common.Comment('comment1', 1, multiline=False),
            common.Comment('comment2', 2, multiline=False),
        ]
        self.assertEqual(comments, expected)

    def testLayeredComment(self):
        code = '<!-- comment<!-- -->'
        comments = html_parser.extract_comments(code)
        expected = [common.Comment(' comment<!-- ', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testNonGreedyComment(self):
        code = '<!--comment--> not a comment -->'
        comments = html_parser.extract_comments(code)
        expected = [common.Comment('comment', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testSideBySideComment(self):
        code = '<!--comment1--> ... <!--comment2-->'
        comments = html_parser.extract_comments(code)
        expected = [
            common.Comment('comment1', 1, multiline=False),
            common.Comment('comment2', 1, multiline=False),
        ]
        self.assertEqual(comments, expected)

    def testUnterminatedComment(self):
        code = '<!--invalid'
        self.assertRaises(common.UnterminatedCommentError,
                          html_parser.extract_comments, code)

    def testLonelyTerminator(self):
        code = 'not a comment-->'
        comments = html_parser.extract_comments(code)
        self.assertEqual(comments, [])
