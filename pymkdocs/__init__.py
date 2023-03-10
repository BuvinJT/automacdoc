# docs > null
from ._version import __version__

# docs > Command Line.md
""" docs : prose
```
| pyMkDocs |
This utility generates MkDocs websites from Python source code.
Help:  pymkdocs -h/--help
Usage: pymkdocs source destination [-m/-r] [-c] [-s]
-m: magic mode (default) / -r: raw mode
-c: include source code
-s: serve test site
```
"""

# docs > Python API.md 
from .pymkdocs import write_doc, RAW_MODE, MAGIC_MODE 