#!/usr/bin/python
"""Tests for comment_parser.parsers.go_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import go_parser


class GoParserTest(unittest.TestCase):

    def testSingleLineComment(self):
        code = '// single line comment'
        comments = go_parser.extract_comments(code)
        expected = [common.Comment(code[2:], 1, multiline=False)]
        self.assertEqual(comments, expected)

    def testSingleLineCommentInRuneLiteral(self):
        code = "msg := '// this is not a comment'"
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testSingleLineCommentInBackTickedLiteral(self):
        code = "msg := `// this is not a comment`"
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testSingleLineCommentInQuotedLiteral(self):
        code = 'msg := "// this is not a comment"'
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineComment(self):
        code = '/* multiline\ncomment */'
        comments = go_parser.extract_comments(code)
        expected = [common.Comment(code[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentWithStars(self):
        code = "/***************/"
        comments = go_parser.extract_comments(code)
        expected = [common.Comment(code[2:-2], 1, multiline=True)]
        self.assertEqual(comments, expected)

    def testMultiLineCommentInRuneLiteral(self):
        code = "msg := '/* This is not a\\nmultiline comment */'"
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineCommentInQuotedLiteral(self):
        code = 'msg := "/* This is not a\\nmultiline comment */"'
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineCommentInBackTickedLiteral(self):
        code = 'msg := `/* This is not a\\nmultiline comment */`'
        comments = go_parser.extract_comments(code)
        self.assertEqual(comments, [])

    def testMultiLineCommentUnterminated(self):
        code = 'a := 1 /* Unterminated\\n comment'
        self.assertRaises(common.UnterminatedCommentError,
                          go_parser.extract_comments, code)
