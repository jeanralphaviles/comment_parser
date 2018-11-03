#!/usr/bin/python
"""Tests for comment_parser.parsers.html_parser.py"""

import builtins
import unittest
from io import StringIO
from unittest import mock

from comment_parser.parsers import common
from comment_parser.parsers import html_parser



class ShellParserTest(unittest.TestCase):

    @mock.patch.object(builtins, 'open')
    def ExtractComments(self, text, mock_open):
        mock_file = StringIO(text)
        mock_open.return_value = mock_file
        return html_parser.extract_comments('filename')

    def testComment(self):
        text = '<!--comment-->'
        comments = self.ExtractComments(text)
        expected = [common.Comment('comment', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testMultilineComment(self):
        text = '<!--multi-line\ncomment-->'
        comments = self.ExtractComments(text)
        expected = [common.Comment('multi-line\ncomment', 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testTwoSeparateSingleComment(self):
        text = '<!--comment1-->\n<!--comment2-->'
        comments = self.ExtractComments(text)
        expected = [
            common.Comment('comment1', 1, multiline=False),
            common.Comment('comment2', 2, multiline=False),
        ]
        self.assertEqual(comments, expected)

    def testLayeredComment(self):
        text = '<!-- comment<!-- -->'
        comments = self.ExtractComments(text)
        expected = [common.Comment(' comment<!-- ', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testNonGreedyComment(self):
        text = '<!--comment--> not a comment -->'
        comments = self.ExtractComments(text)
        expected = [common.Comment('comment', 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testSideBySideComment(self):
        text = '<!--comment1--> ... <!--comment2-->'
        comments = self.ExtractComments(text)
        expected = [
            common.Comment('comment1', 1, multiline=False),
            common.Comment('comment2', 1, multiline=False),
        ]
        self.assertEqual(comments, expected)

    def testUnterminatedComment(self):
        text = '<!--invalid'
        self.assertRaises(
            common.UnterminatedCommentError, self.ExtractComments, text)

    def testLonelyTerminator(self):
        text = 'not a comment-->'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])
