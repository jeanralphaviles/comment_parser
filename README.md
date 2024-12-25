# Comment Parser

[![Run Tests](https://github.com/jeanralphaviles/comment_parser/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/jeanralphaviles/comment_parser/actions/workflows/test.yml)
[![PyPI status](https://img.shields.io/pypi/status/comment_parser.svg)](https://pypi.python.org/pypi/comment_parser/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/comment_parser.svg)](https://pypi.python.org/pypi/comment_parser/)
[![PyPI license](https://img.shields.io/pypi/l/comment_parser.svg)](https://pypi.python.org/pypi/comment_parser/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/comment_parser.svg)](https://pypi.python.org/pypi/comment_parser/)

Python module used to extract comments from source code files of various types.

## Installation

### Prerequisites

* libmagic

### Linux/Unix

```shell
sudo pip3 install comment_parser
```

### OSX and Windows

Additionally, complete the special installation requirements for
[python-magic](https://github.com/ahupp/python-magic).

## Usage

To use, simply run:

```python
>>> from comment_parser import comment_parser
>>> # Returns a list of comment_parser.parsers.common.Comments
>>> comment_parser.extract_comments('/path/to/source_file')
>>> # Or
>>> comment_parser.extract_comments_from_str('...')
```

### extract_comments signatures

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
    pass


def extract_comments_from_str(code, mime=None):
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
    pass
```

### Comments Interface

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

## Development

### Install Dependencies

```shell
pip install -r requirements.txt -r requirements-dev.txt
```

### Running locally

Start python in the base of repository.

```python
from comment_parser import comment_parser
comment_parser.extract_comments('foo.c', mime='text/x-c')
```

### Running tests

```shell
python -m pytest
```

### Running pylint

```shell
pylint comment_parser
```

### Running formatter

```shell
yapf -rip .
```

### Deploying to PyPi

```shell
python setup.py sdist
twine upload dist/*
```

## Supported Programming Languages

| Language    | Mime String              |
|------------ |------------------------- |
| C           | text/x-c                 |
| C++/C#      | text/x-c++               |
| Go          | text/x-go                |
| HTML        | text/html                |
| Java        | text/x-java-source       |
| Javascript  | application/javascript   |
| Python      | text/x-python            |
| Python      | text/x-script.python     |
| Ruby        | text/x-ruby              |
| Shell       | text/x-shellscript       |
| XML         | text/xml                 |

And more to come!

*Check comment_parser.py for corresponding MIME types.*
