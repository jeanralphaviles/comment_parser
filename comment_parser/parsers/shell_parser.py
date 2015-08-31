#!/usr/bin/python
"""This module provides methods for parsing comments from shell scripts."""

from comment_parser.parsers import common as common


def extract_comments(filename):
    """Extracts a list of comments from the given shell script.

    Comments are represented with the Comment class found in the common module.
    Shell script comments only come in one form, single-line. Single line
    comments start with an unquoted or unescaped '#' and continue on until the
    end of the line. A quoted '#' is one that is located within a pair of
    matching single or double quote marks. An escaped '#' is one that is
    immediately preceeded by a backslash '\'

    Args:
        filename: String name of the file to extract comments from.
    Returns:
        Python list of common.Comment in the order that they appear in the file.
    Raises:
        common.FileError: File was unable to be open or read.
    """
    try:
        with open(filename, 'r') as source_file:
            state = 0
            string_char = ''
            current_comment = ''
            comments = []
            line_counter = 1
            while True:
                char = source_file.read(1)
                if not char:
                    # EOF
                    if state is 1:
                        # Was in single line comment. Create comment.
                        comment = common.Comment(current_comment, line_counter)
                        comments.append(comment)
                    return comments
                if state is 0:
                    # Waiting for comment start character, beginning of string,
                    # or escape character.
                    if char == '#':
                        state = 1
                    elif char == '"' or char == "'":
                        string_char = char
                        state = 2
                    elif char == '\\':
                        state = 4
                elif state is 1:
                    # Found comment start character. Read comment until EOL.
                    if char == '\n':
                        comment = common.Comment(current_comment, line_counter)
                        comments.append(comment)
                        current_comment = ''
                        state = 0
                    else:
                        current_comment += char
                elif state is 2:
                    # In string literal, wait for string end or escape char.
                    if char == string_char:
                        state = 0
                    elif char == '\\':
                        state = 3
                elif state is 3:
                    # Escaping current char, inside of string.
                    state = 2
                elif state is 4:
                    # Escaping current char, outside of string.
                    state = 0
                if char == '\n':
                    line_counter += 1
    except OSError as exception:
        raise common.FileError(str(exception))

