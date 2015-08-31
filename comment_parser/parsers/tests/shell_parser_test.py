#!/usr/bin/python
"""Tests for comment_parser.parsers.shell_parser.py"""

from comment_parser.parsers import common as common
from comment_parser.parsers import shell_parser

import builtins
import unittest
from io import StringIO
from unittest import mock


class ShellParserTest(unittest.TestCase):

    @mock.patch.object(builtins, 'open')
    def ExtractComments(self, text, mock_open):
        mock_file = StringIO(text)
        mock_open.return_value = mock_file
        return shell_parser.extract_comments('filename')

    def testComment(self):
        text = '# comment'
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[1:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testEscapedComment(self):
        text = '\# not a comment'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testCommentInSingleQuotedString(self):
        text = "'this is # not a comment'"
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testCommentInDoubleQuotedString(self):
        text = '"this is # not a comment"'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testNestedStringSingleOutside(self):
        text = "'this is \"# not a comment\"'"
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testNestedStringDoubleOutside(self):
        text = '"this is \'# not a comment\'"'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testEscapedSingleQuote(self):
        text = "\\'# this is a comment"
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testEscapedDoubleQuote(self):
        text = '\\"# this is a comment'
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[3:], 1, multiline=False)]
        self.assertEqual(comments, expected)

