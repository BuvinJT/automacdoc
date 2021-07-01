# AutoMacDoc Utility

## What is AutoMacDoc?
AutoMacDoc is a tool to generate documentation for Python modules or groups
of functions. It extends the features of [MkDocs](https://mkdocs.org).
It is, itself written in [Python](https://python.org).

## Why was this project created?

[MkDocs](https://mkdocs.org) is an amazing tool to generate a website with 
[Markdown](https://en.wikipedia.org/wiki/Markdown). Until now, however, there 
was no tool for *auto generating* a MkDocs project from Python source.

The typical starting point when comparing Python documentation generators, is
the standard library's [pydoc](https://docs.python.org/3/library/pydoc.html) module. 
While that tool is easy to use, it's not flexible, and the end result leaves 
something to be desired. In contrast, many would consider the "gold standard" for
auto generating Python documentation to be [Sphinx](https://www.sphinx-doc.org/).
But that tool is complicated, and uses **reStructuredText**.
Too bad reStructuredText *sucks*, **MarkDown** *rocks*!

As the real work involved in documenting your code will end up revolving
around writing [Doc Strings](https://www.python.org/dev/peps/pep-0257/) one way 
or another, being able to express yourself in that context via Markdown will make
you HAPPY for a long time to come!

## How do I install it?

`pip install automacdoc`

## Recipe to make it work:
  - Ingredients:
    - 1 folder containing Python source files (e.g. the `example` folder in this repo)
    OR
    - 1 fresh `pip install`
    - (OPTIONAL) custom Docstrings and/or "magic comments" included in source (see below)
 
  - Easy steps:
    - Install automacdoc.
    - Open a terminal and change to the project directory. Example: `cd automacdoc`
    - Run automacdoc. Example: `automacdoc example/src example -r -c -s`
    
Command line help:

```
| AutoMacDoc |
This utility generates MkDocs websites from Python source code.
Help:  automacdoc -h/--help
Usage: automacdoc source destination [-m/-r] [-c] [-s]
-m: magic mode (default) / -r: raw mode
-c: include source code
-s: serve test site
```
 
## How does this work?
AutoMacDoc analyzes your Python source and generates markdown files from them.
It then employs MkDocs to produce html based documentation from the markdown!
This process creates:
  - a 'mkdocs.yml' file, which is a config file for [MkDocs](https://mkdocs.org)
  - a 'docs' folder, containing the markdown 
  - a 'site' folder, which is the final web site produced 

### Raw Mode

The easiest way to learn to use AutoMacDoc may be to first run the example 
provided in "Raw Mode". Pass the `-r` switch on the command line to enable 
this option. Using this method for generating the documentation, the entire
directory tree for a source path specified is recursively scanned and all 
elements of the code indexed. The files produced have a direct one-to-one 
alignment of Python package / module to a sub directory / document 
(i.e. site page).

This is the most straightforward style for indexing the exact source 
found within that Python code base in a literal manner.    
 
### Magic Mode
  
Now that you've seen how easy it is to use "Raw Mode", let's dive into "Magic Mode"!   

"Magic Mode" is used to generate documentation sites in a more dynamic,
customizable manner. The key difference between this mode vs. "Raw Mode", is that
the method by which objects are indexed is "by import" rather than by "file path".
This mode also provides the means to define the structure of the content produced
to a notable degree.

The way objects are found in this mode aligns with how the content of a package 
naturally resolves via import within a Python runtime context. The source elements 
which are explicitly included within a given Python package's `__init__` module 
will be indexed by the doc generator's parser / inspector. 

The command line argument passed for the "source" argument may simply be the 
name of an import. That argument does not have to be the path to its directory, 
when using this mode. Therefore, after "pip installing" any library (including
from remote or *local* sources), you could follow that up by running `automacdoc` 
against it *by import name*!     

As a bonus, when using this mode, "magic comments" (using syntax defined for this
specific tool) will be processed if placed within such an `__init__` module being
scanned. This is used to dictate how the markdown files / site pages will be named
and ordered, along with what content is generated.

Let's look at an example "magic init" file...   

**example/src/__init__.py**:

```py3
"""
This library is very impressive... :)
"""
# docs > Introduction.md
# docs : __doc__ 

#------------------------------------------------------------------------------
# docs > Mini.md
""" docs : prose
Here is some preamble text for the page...  
"""
from .functions import mini, MIN_SIZE
""" docs : prose
Closing comments on these functions...  
"""

#------------------------------------------------------------------------------
# docs > Shark.md
""" docs : prose
This page is devoted to the **Shark**.  
"""
from .class_and_function import Shark, maxi

#------------------------------------------------------------------------------
# docs > null
from os import abc 

#------------------------------------------------------------------------------
# docs > Config Parser.md
""" docs : virtual
from configparser import ConfigParser
""" 
```

This `__init__` file naturally controls what is accessible via the Python 
import system when a client executes `import src` (assuming that package can 
be found). The items defined in this file are imported by a Python interpreter. 
They are also auto documented when scanned by this tool, along with processing
the "magic comments" the interpreter ignored.

The following magic comments commands may be included in your `__init__` module.  

**START WRITING**: `# docs > [Page Name].md`

Comment lines which start with this, indicate a starting point 
for what is to be written to a given markdown file. That file/page will be named 
by what follows that `docs >` prefix. Note that the source content indexed and 
included in the resulting file may come from *any* importable module / package 
on your system - not just your source!  

**PROSE**:

```py3
""" docs : prose
This markdown appears where ever you want in the current document.
"""
````

Following this comment pattern, "write" this markdown to the current document.

**PACKAGE DOCSTRING**: `# docs : __doc__` 

Inject the the package doc string into the current document. 


**DISCARD**: `# docs > null`

Discards the documentation for whatever source code follows. 

**VIRTUAL CODE**:

```py3
""" docs > virtual
is_virtual_code_cool = True
"""
````

Following this comment pattern, the parsing / object inspecting performed
by the tool will act as though the virtual code were actually present,
but without it having to truly be included in your project.
This provides a means to create documentation in a completely open ended manner
that is is not tightly bound to any literal source.   

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
