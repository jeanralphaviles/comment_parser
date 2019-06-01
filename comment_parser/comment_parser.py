#!/usr/bin/python
"""This program parses various source files and extracts the comment texts.

Currently supported languages:
    C
    C++
    Go
    Java
    Javascript
    Bash/Sh

Dependencies:
    python-magic: pip install python-magic
"""

import sys

import magic

from comment_parser.parsers import common as common
from comment_parser.parsers import c_parser
from comment_parser.parsers import go_parser
from comment_parser.parsers import html_parser
from comment_parser.parsers import js_parser
from comment_parser.parsers import shell_parser

MIME_MAP = {
    'application/javascript': js_parser,  # Javascript
    'text/html': html_parser,             # HTML
    'text/x-c': c_parser,                 # C
    'text/x-c++': c_parser,               # C++/C#
    'text/x-go': go_parser,               # Go
    'text/x-java-source': c_parser,       # Java
    'text/x-javascript': js_parser,       # Javascript
    'text/x-shellscript': shell_parser,   # Unix shell
    'text/xml': html_parser,              # XML
}


class Error(Exception):
    """Base Error class in this module."""
    pass


class UnsupportedError(Error):
    """Raised when trying to extract comments from an unsupported MIME type."""
    pass


class ParseError(Error):
    """Raised when a parser issue is encountered."""
    pass


def extract_comments(filename, mime=None):
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
    if not mime:
        mime = magic.from_file(filename, mime=True)
        if type(mime) == bytes:
            mime = mime.decode('utf-8')
    if mime not in MIME_MAP:
        raise UnsupportedError(
            'Unsupported MIME type %s for file %s' % (mime, filename))
    try:
        parser = MIME_MAP[mime]
    except common.Error as exception:
        raise ParseError(str(exception))
    return parser.extract_comments(filename)


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
