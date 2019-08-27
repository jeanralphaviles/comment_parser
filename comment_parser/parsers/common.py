#!/usr/bin/python
"""This module provides constructs common to all comment parsers."""


class Error(Exception):
  """Base Error class for all comment parsers."""


class FileError(Error):
  """Raised if there is an issue reading a given file."""


class UnterminatedCommentError(Error):
  """Raised if an Unterminated multi-line comment is encountered."""


class Comment():
  """Represents comments found in source files."""

  def __init__(self, text, line_number, multiline=False):
    """Initializes Comment.

    Args:
      text: String text of comment.
      line_number: Line number (int) comment was found on.
      multiline: Boolean whether this comment was a multiline comment.
    """
    self._text = text
    self._line_number = line_number
    self._multiline = multiline

  def text(self):
    """Returns the comment's text.

    Returns:
      String
    """
    return self._text

  def line_number(self):
    """Returns the line number the comment was found on.

    Returns:
      Int
    """
    return self._line_number

  def is_multiline(self):
    """Returns whether this comment was a multiline comment.

    Returns:
      True if comment was a multiline comment, False if not.
    """
    return self._multiline

  def __str__(self):
    return self._text

  def __repr__(self):
    return 'Comment(%s, %d, %s)' % (self._text, self._line_number,
                                    self._multiline)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if self.__dict__ == other.__dict__:
        return True
    return False
