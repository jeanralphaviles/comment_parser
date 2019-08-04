#!/usr/bin/python
"""Tests for comment_parser.parsers.js_parser.py"""

import unittest
from comment_parser.parsers import common as common
from comment_parser.parsers import js_parser as js_parser


class JsParserTest(unittest.TestCase):

    def testSingleLineComment(self):
        code = '// single line comment'
        comments = js_parser.extract_comments(code)
        expected = [common.Comment(code[2:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testSingleLineCommentInSingleQuotedStringLiteral(self):
        code = "msg = '// this is not a comment'"
        comments = js_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testSingleLineCommentInDoubleQuotedStringLiteral(self):
        code = 'msg = "// this is not a comment"'
        comments = js_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineComment(self):
        code = '/* multiline\ncomment */'
        comments = js_parser.extract_comments(code)
        expected = [common.Comment(code[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentWithStars(self):
        code = "/***************/"
        comments = js_parser.extract_comments(code)
        expected = [common.Comment(code[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentInSingleQuotedStringLiteral(self):
        code = "msg = '/* This is not a\\nmultiline comment */'"
        comments = js_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineCommentInDoubleQuotedStringLiteral(self):
        code = 'msg = "/* This is not a\\nmultiline comment */"'
        comments = js_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineCommentUnterminated(self):
        code = 'a = 1 /* Unterminated\\n comment'
        self.assertRaises(
            common.UnterminatedCommentError, js_parser.extract_comments, code)
