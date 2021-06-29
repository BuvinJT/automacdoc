# Welcome to AutoMacDoc

## What is AutoMacDoc?
AutoMacDoc is a tool to generate documentation for Python modules or groups
of functions. It extends the features of [MkDocs](https://mkdocs.org).  It is,
itself written in [Python](https://python.org).

## Why was this project created?

The basic starting point for Python documentation generators is via the 
Standard Library module [pydoc](https://docs.python.org/3/library/pydoc.html).
While that tool is easy to use, it is not flexible and the end result leaves something
to be desired. In contrast, the gold standard for auto generating Python documention is
argably [Sphinx](https://www.sphinx-doc.org/). But that tool is complicated, and is 
driven by **reStructuredText**.  Too bad that reStructuredText *sucks*, **MarkDown** *rocks*!
[MkDocs](https://mkdocs.org) is an amazing tool to generate a website with MarkDown...
but until now, there was no tool for *auto generating* a MkDocs project from Python source!

## How do I install it?
With pip pardi : `pip install automacdoc`

## Recipe to make it work!
  - Ingredients:
    - 1 folder containing Python source files (e.g. the `example` folder in this repo)
    - 1 (or more!) custom Docstrings are ideally include in that code, to supplement the auto generated text

  - Easy steps:
    - Install automacdoc.
    - Open a terminal and change to the project directory. Example: `cd automacdoc`
    - Run automacdoc. Example: `automacdoc example/src example -m -c -s`
    
  - Full command line argument details:

```
| AutoMacDoc |
This utility generates MkDocs websites from Python source code.
Usage: automacdoc source destination [-m/-r] [-c] [-s]
-m: magic mode (default) / -r: raw mode
-c: include source code
-s: serve test site
```
 
## How does this work?
AutoMacDoc analyzes your Python source and generates *markdown* files from them.
It then employs MkDocs to produce html based documentation from the markdown!
This process creates:
  - a 'mkdocs.yml' file, which is a config file for [MkDocs](https://mkdocs.org)
  - a 'docs' folder, which contains the markdown source processed by [MkDocs](https://mkdocs.org)
  - a 'site' folder, which contains the static site produced 
 
### Magic Mode
  
By default, "Magic Mode" is used to generate the documents in a dynamic, highly
customizable manner.  Those objects which are available naturally via a package 
import, within a Python runtime context, are the those which are documented.
More specifically, the source elements which are explicitly included within 
a given Python package's `__init__` module will be indexed by the parser
/ inspector. 

As a bonus, when using this mode, "magic comments" (included for this specific
tool) will be processed if placed within an `__init__` module being scanned.
This is used to dictate how the markdown files / site pages will be named, ordered, 
and the content which they index.

This mode may be most easily understood by looking at an example file provided.   

**example/src/__init__.py**:

```py3
# DOCS > Mini.md
from .functions import mini, MIN_SIZE
# DOCS > Shark.md
from .class_and_function import Shark, maxi
# DOCS > NULL
from os import abc 
# DOCS > Config Parser.md
""" DOCS > VIRTUAL
from configparser import ConfigParser
""" 
```

This `__init__` file naturally controls what is accessible via the Python 
import system when a client executes `import src` (assuming that package can 
be found). Rather than importing the entire directory under "src", only the 
items defined in this file are imported by a Python interpreter. Likewise, that
is all which is auto documented when running in this mode.  

**START WRITING**: `# DOCS >`

The comment lines shown which start with this comment indicate a starting point 
for what is to be written to a given markdown file. That file/page will be named 
by what follows that comment prefix. Note that the source content indexed and 
included in the resulting file may come from *any* importable module / package 
on your system.  That does not have to be limited to only the source within a 
fixed directory.

In a similar manner to how the import tracing works when processing the code,
the command line argument passed for the "source" argument may simply be the 
name of an import. That argument does not have to be the path to its directory, 
when using this mode. Therefore, after "pip installing" any library (including
from remote or *local* sources), you could follow that up by running `automacdoc` 
against it *by import name*!     

**DISCARD**: `# DOCS > NULL`

Discards the documentation for whatever source code follows. 

**VIRTUAL CODE**:

```py3
""" DOCS > VIRTUAL
is_virtual_code_cool = True
"""
````

Following this comment pattern, will cause the parsing/inpsecting to occur 
as though the virtual code were actually present,
but without it having to truly be executed and included in your project.
This provides a means to create documentation in a completely open ended manner
that is is not tightly bound to the literal source.   

### Raw Mode

Alternatively, AutoMacDoc may be run in "Raw Mode". Pass the `-r` switch on the 
command line for this. Using this method for generating the documentation, the 
entire directory tree for a source path specified is recursively scanned and all 
elements of the source indexed. The files produced have a direct one-to-one 
alignment of python package / module to a sub directory / document (site page).

This is the most detailed, comprehensive style for indexing the exact source 
found within that Python code base in a literal manner.    

## Minimal project layout

  - before AutoMacDoc:

>      src/
>          ...         # Other python files or folders

  - after AutoMacDoc:

>      mkdocs.yml      # The configuration file.
>
>      src/
>          ...         # Other python files or folders
>
>      docs/
>          index.md    # The documentation homepage.
>          ...         # Other markdown pages, images and other files.
>
>      site/           # The static site ready to be hosted
>          index.html
>          ...


## Recommended Docstring
**Code:**
```py3
def fun(arg1: int, arg2: str = 'Hello World!'):
    """Description of your function

    **Parameters**

    > **arg1:** `int` -- Description of argument `arg1`.

    > **arg2:** `str` -- Description of argument `arg2`.

    **Returns**

    > `str` -- Description of returned object.
    """
    return arg2 + str(arg1)
```

**Screenshot:**

![recommended docstring screenshot](img/recommend_docstring.png)

## Want more?
Check out the example source. There, you will find tons of fancy elements you 
can now instantly add to your documentation, leveraging the power of many
[MkDocs](https://mkdocs.org) extensions!

## Now what?
Once you have the source generated for a static website to display your amazing
documentation, how do you make that available to your users / target audience?

Well you may, of course, setup website hosting in any number of manners, which
are well beyond the scope of this document. With that done, you could
simply upload these files there.  That said, a very notable option for this
specific purpose, which is free, fast, and easy, is to use
[GitHub Pages](https://pages.github.com/).

With GitHub Pages, you may create a *new* GitHub repository dedicated to the 
site, or you may *add* a GitHub Pages site to an *existing* repository (e.g. your
project source). Arguably, the latter makes more sense if the code you are 
documenting is already on GitHub, or you intend to post it there. For more on this see:
[Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site)
