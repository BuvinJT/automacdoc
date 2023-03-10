# pyMkDocs Utility

## What is pyMkDocs?
pyMkDocs is a terminal-based program used to generate documentation for Python projects.
It extends the features of [MkDocs](https://mkdocs.org).

The parent project is found here: https://github.com/AlexandreKempf/automacdoc

## What does pyMkDocs do?
pyMkDocs analyzes Python source code, produces Markdown files for [MkDocs](https://mkdocs.org), and leans on that to generate a website.  While you may use MkDocs against whatever markdown files you have independently produced, until now there has been no means available for *auto generating* a MkDocs project directly from Python source!

## How do I install pyMkDocs?

`pip install pymkdocs`

## How do I use pyMkDocs?

pyMkDocs analyzes your Python source and generates markdown files from them. It then employs MkDocs to produce html based documentation from the markdown! This process creates:

  - a 'mkdocs.yml' file, which is a config file for [MkDocs](https://mkdocs.org)
  - a 'docs' folder, containing the markdown 
  - a 'site' folder, which is the final web site produced 

### Command line specs

```
| pyMkDocs |
This utility generates MkDocs websites from Python source code.
Help:  pymkdocs -h/--help
Usage: pymkdocs source destination [-m/-r] [-c] [-s]
-m: magic mode (default) / -r: raw mode
-c: include source code
-s: serve test site
```

### Basic Program Scenario

> Note: This is the ideal way to get your feet wet with this tool!

- Change to the directory of a Python project of your choice. 

Example:
~~~ 
cd pymkdocs/example
~~~

- Run pyMkDocs against the source in "raw mode".  (See below for more details.)

Example:
~~~ 
pymkdocs src . -r -c -s
~~~

### Third Party Library Scenario

- Pip install "some_library".  Ideally, pick one which has little to no documentation available.
- Run pyMkDocs against that library, to create some docs for yourself on the fly! 

Example: 
~~~ 
pip install pymkdocs
pymkdocs pymkdocs ./pymkdocs_docs -s
~~~

### Library Development Scenario

- Create your own library.  
- Start using pymkdocs throughout the development process.
- Whenever you test your code changes, run a script such as the following to reinstall the library, and simultaneously regenerate the documentation  (within the project's directory):

~~~
cd my_library
pip3 install .
pymkdocs ./my_library .
~~~

> Note: you must add a `-s` switch after the `pymkdocs` command above, if you wish to view the regenerated website locally.

- If your code changes have modified the library's public interface, those changes will be auto documented for you! 
  
- Commit your code changes in parallel with doc changes.  This way, your git history will always align with the docs! 
  
  > This is an easy way to facilitate "historic docs".  Consumers of your library could always revert the repo back to a given "tag", to acquire the documentation for the exact version they are implementing.

## Content Produced 

Here is a visual aide to help depict what you will be creating by using the utility. 

BEFORE running pyMkDocs: Your project "core" may be comprised of a single source sub directory.

>      - src/
>          ...         # Your python source files and folders

AFTER running pyMkDocs: You would have the following in that project root path:

>      - src/
>          ...         # Your (unmodified) python source files and folders
>
>      - mkdocs.yml    # The site configuration file.
>
>      - docs/
>          - index.md  # The documentation homepage.
>          ...              # Other markdown pages, images and other files.
>
>      - site/                 # The static website - ready to be uploaded or locally served
>          - index.html
>          ...

## Content Merging 

pyMkDocs is not limited to only generating a site from scratch. Instead, it can be dynamically *integrated* with your custom content.  Once you know how, it's easy to add your own pages, to add more MkDocs [extensions](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions), to add [plugins](https://www.mkdocs.org/user-guide/configuration/#plugins), modify the site [theme](https://www.mkdocs.org/user-guide/configuration/#theme) and more!  

### Update Mode

The easiest way to *start* an pyMkDocs project is to first allow the tool to create a basic site for you, as shown previously in these docs.  After that, you may edit the `mkdocs.yml` file which was generated.  When the tool is run again subsequently, it will detect the presence of that prior configuration, and automatically operate in "update mode".

In "Update Mode", the only part of the `mkdocs.yml` which pyMkDocs will modify is that found within a section named `Reference`.  Anything else in that file which you manually customized will be fully preserved and respected while MkDocs regenerates the site.      

> To learn more about how you may modify the `mkdocs.yml` file, see the [MkDocs Configuration Guide](https://www.mkdocs.org/user-guide/configuration/).

### Hybrid  Update Mode

An alternative "Hybrid Mode" has also been provided. This a middle ground between starting from scratch or operating as a pure "update".

To use this method:

- Remove an existing `mkdocs.yml` file (if applicable)
- Create a `docs` folder (if one does not exist)
- Add **your own** Markdown files to the `docs` folder
- Run pyMkDocs!

The result of this will be similiar to creating a whole new site, accept your pre-existing Markdown files will be used to generate site pages and they will be automatically added to the top level of your table of contents! 

### Home Page

When a vistor first browses to the site, its "Home" page will be displayed. This page is created from a Markdown file named `index.md` (named like a default website page: `index.html`).

If this file does not exist in your `docs` folder, pyMkDocs will generate a simple placeholder for you. To revise the content of this page, simply edit, or replace, the `index.md` source.   

## Site Publishing

Once you have the source generated for a static website to display your amazing documentation, how do you make that available to your users / target audience?

Well you may, of course, setup website hosting in any number of manners (which are all well beyond the scope of this document!). With that done, you could simply upload the files there. That said, we highly recommend a solution which is often ideal for this specific purpose - one which is free, fast, and easy... [GitHub Pages](https://pages.github.com/).

With GitHub Pages, you may either create a *new* GitHub repository dedicated just to the site, or you may *add* a GitHub Pages site to an *existing* repository (e.g. your project source). Arguably, the latter makes more sense if the code you are documenting is already on GitHub, or you intend to post it there. For more on this see: [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site)

Note that GitHub Pages allows you to serve your site from either the *root* of the repository, or a sub directory named `docs`. There is (currently) **no option** to define this path yourself, or to use a directory named `site` instead.  

### GitHub Pages Paths

GitHub Pages support Markdown based sites, and can therefore use a `docs` directory with simple Markdown itself. The site service will then convert that to html via a completely **separate mechanism** from what you've already produced with MkDocs though! 

The event you are adding a GitHub Pages site to an *existing* project, it is highly doubtful you would want the docs on the *root* of that.  As such, to post your site exactly as it appears locally, you will need to place what is normally the "site" content in the a directory on the repo root which is instead named `docs`, while placing your "docs" in a directory named `docs_src`. 

To configure the site for this, simply rename your folders and add the following lines to your `mkdocs.yalm` file:

```
docs_dir: docs_src
site_dir: docs
```

Having done this, pyMkDocs will auto generate Markdown into the `docs_src` folder, and MkDocs will generate the website content to `docs`. 

## Parsing Modes

### Raw Mode

The easiest way to learn to use pyMkDocs may be to first run the example provided in "Raw Mode". Pass the `-r` switch on the command line to enable this option. Using this method, the entire directory tree for a source path specified is recursively scanned and all elements of the code indexed. The **files** produced have a direct **one-to-one** alignment of Python package / module to a sub directory / document (i.e. site page).

This is the most straightforward style for indexing the exact source found within that Python code base in a literal manner.    

### Magic Mode

Now that you've seen how easy it is to use "Raw Mode", let's dive into "Magic Mode"!   

"Magic Mode" is used to generate documentation sites in a more dynamic, customizable manner. The key difference between this mode vs. "Raw Mode", is that the method by which objects are indexed is "by import" rather than by "file path". This mode also provides the means to define the structure of the content produced to a notable degree.

The way objects are found in this mode aligns with how the content of a package naturally resolves via import within a Python runtime context. The source elements which are explicitly included within a given Python package's `__init__` module will be indexed by the doc generator's parser / inspector. 

The command line argument passed for the `source` argument may simply be the **name of an import**. That argument does NOT have to be the **path **to its directory, when using this mode. Therefore, after "pip installing" any library including
from remote or *local* sources), you could follow that up by running `pyMkDocs` against it *by import name*!     

As a bonus, when using this mode, "magic comments" (using syntax defined for this specific tool) will be processed if placed within such an `__init__` module being scanned. This is used to dictate how the markdown files / site pages will be named and ordered, along with what content is generated.

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
""" docs : virtual_code
from configparser import ConfigParser
""" 
```

This `__init__` file naturally controls what is accessible via the Python import system when a client executes `import src` (assuming that package can be found). The items defined in this file are imported by a Python interpreter.  They are also auto documented when scanned by this tool, along with processing the "magic comments" the interpreter ignored.

### Magic Comments

The following magic comments commands may be included in your `__init__` module.  

#### Target Doc

~~~
# docs > [Page Name].md
~~~

Comment lines which start with this, indicate a starting point for what is to be written to a given markdown file. That file/page will be named by what follows that `docs >` prefix. Note that the source content indexed and included in the resulting file may come from *any* importable module / package on your system - not just your source!  

#### Prose

```py3
""" docs : prose
This markdown appears where ever you want in the current document.
"""
````

Following this comment pattern, "write" this markdown to the current document.

#### Package Docstring

~~~
# docs : __doc__
~~~

Inject the the package docstring into the current document. 

#### Discard 

```
# docs > null
```

Discards the documentation for whatever source code follows. 

#### Virtual Code

```py3
""" docs : virtual_code
is_virtual_code_cool = True
"""
````

Use this to inject "virtual code", without actually modifying your functional source, for the purpose of having the documentation generator treat it as though it were truly there. This provides a means to create documentation in a completely open ended manner, which is is not tightly bound to literal source.   

#### Virtual Value

```py3
my_global_number=5
""" This number may differ between run contexts.
docs : virtual_value=500
"""
````

Use this in an attribute/variable docstring to override the default value which would otherwise appear in the documentation. 

#### Conditional Value

```py3
MY_CONSTANT="brilliance"
""" Here is a docstring for my constant.
docs : conditional_value
"""
````

Use this in an attribute/variable docstring to modify the style of the default value in the documentation, so as to indicate it is "conditional". 

## Recommended Function Docstring

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

## Attribute Docstrings

The formal standards for Python docstrings are defined in [PEP-257](https://www.python.org/dev/peps/pep-0257/). They do NOT include "attribute docstrings". There is, therefore, no *official* means to document how to use class and module attributes. The primary reason for this
is because a consensus could not be arrived upon as to what the cleanest means would be for developers to employ such a standard in practice. Following the rules for how this is done with modules, classes, and functions (adding triple double comments after the object signatures), seemed excessive or confusing to some. Further, there is a belief that attributes should be "self documenting", by simply using good names for them.     

That said, it has been suggested that *unofficial* documentation generators (such as this) may still wish to adhere to the standards proposed in the *rejected* [PEP-224](https://www.python.org/dev/peps/pep-0224/) or [PEP-258](https://www.python.org/dev/peps/pep-0258/#attribute-docstrings) regarding attributes. So, pyMkDocs recognizes those conventions and processes such comments when generating documentation.

## Additional Features
Check out the example source. There, you will find tons of fancy elements you can now instantly add to your documentation, leveraging the power of many [MkDocs](https://mkdocs.org) extensions!

## What other options exist for auto documentation?

The typical starting point when comparing Python documentation generators, is the standard library's [pydoc](https://docs.python.org/3/library/pydoc.html) module. 
While that tool is easy to use, it's not flexible, and the end result leaves something to be desired. 

In contrast, many would consider the "gold standard" for auto generating Python documentation to be [Sphinx](https://www.sphinx-doc.org/). But that tool is complicated, and uses [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText). Unfortunately, reStructuredText is quite unpleasant to work with and has very limited applications. 

[Markdown](https://en.wikipedia.org/wiki/Markdown) is fast and easy to type freehand, there are many tools which auto generate it, and its use is widespread. Regardless of the doc generator employed, the most laborious task involved in documenting your code is likely to be writing [Doc Strings](https://www.python.org/dev/peps/pep-0257/).  In those contexts, having Markdown available to you can be immensely desirable!
