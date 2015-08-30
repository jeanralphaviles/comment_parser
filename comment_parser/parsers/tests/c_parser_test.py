#!/usr/bin/python
"""Tests for comment_parser.parsers.c_parser.py"""

from comment_parser.parsers import common as common
from comment_parser.parsers import c_parser as c_parser

import unittest
import builtins
from unittest import mock
from io import StringIO

class CParserTest(unittest.TestCase):

    @mock.patch.object(builtins, 'open')
    def ExtractComments(self, text, mock_open):
        mock_file = StringIO(text)
        mock_open.return_value = mock_file
        return c_parser.extract_comments('filename')

    def testSingleLineComment(self):
        text = '// single line comment'
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[2:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testSingleLineCommentInStringLiteral(self):
        text = 'char* msg = "// this is not a comment"'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testMultiLineComment(self):
        text = '/* multiline\ncomment */'
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentWithStars(self):
        text = "/***************/"
        comments = self.ExtractComments(text)
        expected = [common.Comment(text[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentInStringLiteral(self):
        text = 'char* msg = "/* This is not a\\nmultiline comment */"'
        comments = self.ExtractComments(text)
        self.assertEqual(comments, [])

    def testMultiLineCommentUnterminated(self):
        text = 'int a = 1; /* Unterminated\\n comment'
        self.assertRaises(
            common.UnterminatedCommentError, self.ExtractComments, text)

    @mock.patch.object(builtins, 'open')
    def testExtractCommentsFileError(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        self.assertRaises(common.FileError, c_parser.extract_comments, '')

