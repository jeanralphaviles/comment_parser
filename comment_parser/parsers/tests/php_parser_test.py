#!/usr/bin/python
"""Tests for comment_parser.parsers.c_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import php_parser


class PHPParserTest(unittest.TestCase):

  def testSimpleSingleLineComment(self):
    code = """<?php
    // this is a comment
    echo "Hello World";"""
    comments = php_parser.extract_comments(code)
    expected = [common.Comment(" this is a comment", 2, multiline=False)]
    self.assertEqual(comments, expected)

  def testOtherSingleLineComment(self):
    code = """<?php
    # this is a comment
    echo "Hello World";"""
    comments = php_parser.extract_comments(code)
    expected = [common.Comment(" this is a comment", 2, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInStringLiteral(self):
    code = '''<?php
    echo "// this is not a comment";'''
    comments = php_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '''<?php
    /* multiline\ncomment */'''
    comments = php_parser.extract_comments(code)
    expected = [common.Comment(' multiline\ncomment ', 2, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = """<?php
    /***************/"""
    comments = php_parser.extract_comments(code)
    expected = [common.Comment("*************", 2, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInStringLiteral(self):
    code = '''<?php
    echo "/* This is not a\\nmultiline comment */";'''
    comments = php_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = '''<?php
    $a = 1; /* Unterminated\\n comment'''
    self.assertRaises(common.UnterminatedCommentError,
                      php_parser.extract_comments, code)

  def testMultipleMultilineComments(self):
    code = '''<?php
    /* abc */ /* 123 */'''
    comments = php_parser.extract_comments(code)
    expected = [
        common.Comment(' abc ', 2, multiline=True),
        common.Comment(' 123 ', 2, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testStringThenComment(self):
    code = '''<?php
    echo "" /* "abc */;'''
    comments = php_parser.extract_comments(code)
    expected = [
        common.Comment(' "abc ', 2, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    # TODO(#27): Re-enable test.
    # code = r'" \" /* \" "'
    # comments = c_parser.extract_comments(code)
    # self.assertEqual(comments, [])
    pass

  def testStringEscapedBackslashCharacter(self):
    code = r'''<?php
    echo "\\"; # This wouldn't be a comment, if the second " is misinterpreted as escaped
    '''
    comments = php_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testCommentedOtherComment(self):
    code = '''<?php
    //# double comment'''
    comments = php_parser.extract_comments(code)
    self.assertEqual(comments, [common.Comment('# double comment', 2)])

  def testOtherCommentedComment(self):
    code = '''<?php
    #// double comment'''
    comments = php_parser.extract_comments(code)
    self.assertEqual(comments, [common.Comment('// double comment', 2)])
