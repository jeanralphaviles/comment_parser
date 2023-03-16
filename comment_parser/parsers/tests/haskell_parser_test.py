#!/usr/bin/python
"""Tests for comment_parser.parsers.haskell_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import haskell_parser


class HaskellParserTest(unittest.TestCase):

  def testSimpleMain(self):
    code = "-- this is a comment\nmodule main where\nmain = putStrLn \"Hello, World!\""
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(code[2:20], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineComment(self):
    code = "-- single line comment"
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(code[2:], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInStringLiteral(self):
    code = 'a = "-- this is not a comment"'
    comments = haskell_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '{- multiline\ncomment -}'
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentsWithDashes(self):
    code = "{----------------------}"
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultilineCommentInStringLiteral(self):
    code = 'a = "{- this is not a comment -}"'
    comments = haskell_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'int a = 1; {- Unterminated\\n comment'
    self.assertRaises(common.UnterminatedCommentError,
                      haskell_parser.extract_comments, code)

  def testMultipleMultilineComments(self):
    code = '{- abc -} {- 123 -}'
    expected = [
        common.Comment(' abc ', 1, multiline=True),
        common.Comment(' 123 ', 1, multiline=True)
    ]
    comments = haskell_parser.extract_comments(code)
    self.assertEqual(comments, expected)

  def tetStringThenComment(self):
    code = r'"" {- "abc -}'
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(' "abc ', 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testStringEscapedBackslashCharacter(self):
    code = r'"\\"'
    comments = haskell_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testTwoStringsFollowedByComment(self):
    code = r'"""" -- foo'
    comments = haskell_parser.extract_comments(code)
    expected = [common.Comment(' foo', 1)]
    self.assertEqual(comments, expected)

  def testCommentedMultilineComment(self):
    code = '''-- What if i start a {- here
    int main(){return 0;}
    -- and ended it here -}'''
    comments = haskell_parser.extract_comments(code)
    expected = [
        common.Comment(" What if i start a {- here", 1, False),
        common.Comment(" and ended it here -}", 3, False)
    ]
    self.assertEqual(comments, expected)

  def testMultilineCommentedComment(self):
    code = '''{--- here
    int main(){return 0;}
    -}-- and ended it here -}'''
    comments = haskell_parser.extract_comments(code)
    expected = [
        common.Comment('-- here\n    int main(){return 0;}\n    ', 1,
                        True),
        common.Comment(' and ended it here -}', 3, False)
    ]
    self.assertEqual(comments, expected)