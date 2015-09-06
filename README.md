# Comment Parser
---
Python module used to extract comments from source code files of various types.
## Installation
---
### Linux/Unix
To install run 'sudo pip3 install comment_parser'.
### OSX and Windows
Complete the special installation requirements for [python-magic](https://github.com/ahupp/python-magic).
## Usage
---
To use, simply run:

```python
>>> from comment_parser import comment_parser
>>> comment_parser.extract_comments('/path/to/source_file')  # Returns a list of comment_parser.parsers.common.Comments
```
### extract_comments Signature
---
```python
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
```
### Comments Interface
---
```python
class Comment(object):
    """Represents comments found in source files."""
    def text(self):
        """Returns the comment's text.
        Returns:
            String
        """
        pass

    def line_number(self):
        """Returns the line number the comment was found on.
        Returns:
            Int
        """
        pass

    def is_multiline(self):
        """Returns whether this comment was a multiline comment.
        Returns:
            True if comment was a multiline comment, False if not.
        """
       pass

    def __str__(self):
        pass

    def __eq__(self, other):
        pass
```

## Supported Programming Languages
---
1. C
2. C++
3. Go
4. Java
5. Javascript
6. Shell scripts (Bash, sh, etc.)
7. More to come!

*Check comment_parser.py for corresponding MIME types.*
