# Welcome to AutoMacDoc

## What is AutoMacDoc?
AutoMacDoc is a tool to generate documentation for Python modules or groups
of functions. It is based on [MkDocs](https://mkdocs.org) and written in [Python](https://python.org).

## Why was this project created?

The gold standard for auto generating Python documention is argably  
[Sphinx](https://www.sphinx-doc.org/). But that tools is complicated, and it 
uses **reStructuredText**.  In our opinion, reStructuredText *sucks*, **MarkDown** *rocks*!
[MkDocs](https://mkdocs.org) is an amazing tool to generate a website with MarkDown...
but until now, there was no tool for auto generating a MkDocs project from Python source code!

## How to install?
With pip pardi : `pip install automacdoc`

## Recipe to make it work!
  - Ingredients:
    - a folder containing Python source files (e.g. the `example` folder in this repo)
    - ideally, include custom Docstrings in that code (to supplement the auto generated text)

  - Easy steps:
    - install automacdoc
    - open a terminal
    - change to the project source directory
    - execute `automacdoc [source] [destination]`
    - example: `automacdoc example/src example`
    
  - Or try the alternate "import scan mode"!
    - execute `automacdoc [-i/-d] [source] [destination]`
    - example: `automacdoc -i example/src example`

## Now what?
Once you have the source generated for a static website to display your amazing
documentation, how do you make that available to your users / target audience?

Well you may, of course, setup website hosting in any number of manners, which 
are well beyond the scope of this documentation. With that done, you could 
simply upload these files there.  That said, a very notable option for this 
specific purpose, which is free, fast, and easy, is to use 
[GitHub Pages](https://pages.github.com/).

With GitHub Pages, you may create a *new* GitHub repository dedicated to the 
site, or you may *add* a GitHub Pages site to an existing repository (e.g. your
project source). Arguably, the latter makes more sense for most use case.  
For more on this see: [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site)

## How does this work?
AutoMacDoc analyzes your Python source and generates both markdown, and markup, documentation from it!
It creates:
  - a 'mkdocs.yml' file, which is a config file for [MkDocs](https://mkdocs.org)
  - a 'docs' folder which contains the markdown source for [MkDocs](https://mkdocs.org)
  - a 'site' folder which contains the static site produced by [MkDocs](https://mkdocs.org)

### Directory Scan Mode

By default, AutoMacDoc runs in "Directory Scan Mode". Using this method for generating
the documentation, the entire directory tree for the source path specified is 
recursively scanned and all elements of the source are indexed.  The files produced have 
a direct one-to-one alignment of module to document page.   
 
### Import Scan Mode
  
Alternatively, "Import Scan Mode" may be used to generate the documents in a more
dynamic, filtered, and custom manner.  Rather than documenting an entire code base, 
only the the elements explicitly included in within a package's __init__ module will be 
indexed.  This aligns with how package / library imports work within a Python 
runtime context.  Further, the __init__ module for a package may contain 
"magic comments" which dictate how the markdown files / site pages will be named 
and divided.

This mode can be most easily explained, and understood, by looking at an example 
source file provided.   

**example/src/__init__.py**:

```py3
# DOCS >> Mini.md
from .functions import mini
# DOCS >> Shark.md
from .class_and_function import Shark, maxi
```

This __init__ file naturally controls what is accessible via the Python import system 
when a client executes `import src` (assuming that package can be found).  Rather than 
importing the entire directory tree recursively under "src", only the items defined
here are imported, and as such that is all which is auto documented by this mode.  

The comment lines which start with `# DOCS >>` indicate a starting point for what 
is to be written to a given markdown file.  That file/page will be named whatever 
follows that comment prefix. Note that the source content indexed and included in 
the resulting file may come from *any* importable module / package on your system 
- not just the source within this directory.

Finally, when using this mode, note that the command line argument passed for the 
"source" may simply be the name of an import, not the path to it's source directory.
Therefore, after "pip installing" any library, you could follow that up by 
running automacdoc against an import from it.     

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
Check out the example source. There, you will found tons of fancy elements you 
can now add to your documentation!
