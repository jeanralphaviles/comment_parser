#!/usr/bin/python
"""This program parses various source files and extracts the comment texts.

Currently supported languages:
  Bash/sh
  C
  C++
  Go
  HTML
  Java
  Javascript
  Ruby
  XML

Dependencies:
  python-magic: pip install python-magic (optional)
"""

import sys
from typing import List, Optional

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

from comment_parser.parsers import c_parser
from comment_parser.parsers import common
from comment_parser.parsers import go_parser
from comment_parser.parsers import html_parser
from comment_parser.parsers import js_parser
from comment_parser.parsers import python_parser
from comment_parser.parsers import ruby_parser
from comment_parser.parsers import shell_parser

MIME_MAP = {
    'application/javascript': js_parser,  # Javascript
    'text/html': html_parser,  # HTML
    'text/x-c': c_parser,  # C
    'text/x-c++': c_parser,  # C++/C#
    'text/x-go': go_parser,  # Go
    'text/x-java': c_parser,  # Java
    'text/x-java-source': c_parser,  # Java
    'text/x-javascript': js_parser,  # Javascript
    'text/x-python': python_parser,  # Python
    'text/x-ruby': ruby_parser,  # Ruby
    'text/x-script.python': python_parser,  # Python
    'text/x-shellscript': shell_parser,  # Unix shell
    'text/xml': html_parser,  # XML
}


class Error(Exception):
    """Base Error class in this module."""


class UnsupportedError(Error):
    """Raised when trying to extract comments from an unsupported MIME type."""


class ParseError(Error):
    """Raised when a parser issue is encountered."""


def extract_comments(filename: str,
                     mime: Optional[str] = None) -> List[common.Comment]:
    """Extracts and returns the comments from the given source file.

  Args:
    filename: String name of the file to extract comments from.
    mime: Optional MIME type for file (str). Note some MIME types accepted
      don't comply with RFC2045. If not given, an attempt to deduce the
      MIME type will occur.
  Returns:
    Python list of parsers.common.Comment in the order that they appear in
      the source file.
  Raises:
    UnsupportedError: If filename is of an unsupported MIME type.
  """
    with open(filename, 'r', encoding='utf-8') as code:
        return extract_comments_from_str(code.read(), mime)


def extract_comments_from_str(code: str,
                              mime: Optional[str] = None
                              ) -> List[common.Comment]:
    """Extracts and returns comments from the given source string.

  Args:
    code: String containing code to extract comments from.
    mime: Optional MIME type for code (str). Note some MIME types accepted
      don't comply with RFC2045. If not given, an attempt to deduce the
      MIME type will occur.
  Returns:
    Python list of parsers.common.Comment in the order that they appear in
      the source code.
  Raises:
    UnsupportedError: If code is of an unsupported MIME type.
  """
    if not mime:
        if not HAS_MAGIC:
            raise ImportError('python-magic was not imported')
        mime = magic.from_buffer(code, mime=True)
        if isinstance(mime, bytes):
            mime = mime.decode('utf-8')
    if mime not in MIME_MAP:
        raise UnsupportedError(f'Unsupported MIME type {mime}')
    try:
        parser = MIME_MAP[mime]
        return parser.extract_comments(code)
    except common.Error as e:
        raise ParseError() from e


def main(argv):
    """Extracts comments from files and prints them to stdout."""
    for filename in argv:
        try:
            comments = extract_comments(filename)
            for comment in comments:
                print(comment.text())
        except Error as exception:
            sys.stderr.write(str(exception))


if __name__ == '__main__':
    main(sys.argv[1:])
