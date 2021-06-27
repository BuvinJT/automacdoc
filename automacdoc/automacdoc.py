# ----------------
import ast
import inspect
import importlib
import os
import sys
import platform
import glob
import traceback
# ----------------
 
DIR_SCAN_MODE, IMPORT_SCAN_MODE = range(2)

MAGIC_DOCNAME_COMMENT='# DOCS >>'

# TODO: define this function correctly
def __markdown_safe(obj): 
    return str(obj).replace('<','').replace('>','')

def rm_docstring_from_source(source):
    """
    Remote the docstring from the source code of a function or a class

    **Parameters**
    > **source:** `str` -- Source code of a function or a class

    **Returns**
    > `str` -- Source code of a class without docstring
    """
    source = source.split('"""')
    if len(source) > 1:
        del source[1]  # remove docstring
    source = "".join(source)
    # to handle intendation inside functions and classes
    source = source.split("\n")
    nb_indent = len(source[0]) - len(source[0].lstrip())
    for i in range(len(source)):
        source[i] = "\t" + source[i][nb_indent:]
    source = "\n".join(source)
    return source

def create_var(name: str, obj, ignore_prefix_function: str):
    return create_att(name, obj, ignore_prefix_function)

def create_att(name: str, obj, ignore_prefix_function: str):
    """
    Generate a dictionary that contains the information about an attribute

    **Parameters**
    > **name:** `str` -- name of the attribute as returned by `inspect.getmembers`
    > **obj:** `object` -- object of the attribute as returned by `inspect.getmembers`
    > **ignore_prefix_function:** `str` -- *None* -- precise the prefix of attribute names to ignore

    **Returns**
    > `dict` -- with keys:
    >  - *name*, *obj* -- the attribute name and object as returned by `inspect.getmembers`
    >  - *module* -- name of the module
    >  - *path* -- path of the module file
    >  - *doc* -- docstring of the attribute
    >  - *source* -- source code of the attribute    
    >  - *type* -- type of the attribute
    >  - *value* -- value of the attribute
    """

    if (
        ignore_prefix_function is not None
        and name[:len(ignore_prefix_function)] == ignore_prefix_function
    ):
        return None

    att = {}
    att["name"]  = name if name else 'undefined'
    att["obj"]   = obj
    att["type"]  = __markdown_safe(type(obj))
    att["value"] = 0    
    """
    try:    att["module"] = inspect.getmodule(obj).__name__
    except: att["module"] = None
    try:    att["path"] = inspect.getmodule(obj).__file__
    except: att["path"] = None
    try:    att["doc"] = inspect.getdoc(obj) or ""
    except: att["doc"] = None
    try:    att["source"] = inspect.getsource(obj)
    except: att["source"] = None
    """    
    att["module"] = None
    att["path"] = None
    att["doc"] = None
    att["source"] = None
    return att


def create_fun(name: str, obj, ignore_prefix_function: str):
    """
    Generate a dictionnary that contains the information about a function

    **Parameters**
    > **name:** `str` -- name of the function as returned by `inspect.getmembers`
    > **obj:** `object` -- object of the function as returned by `inspect.getmembers`
    > **ignore_prefix_function:** `str` -- *None* -- precise the prefix of function names to ignore

    **Returns**
    > `dict` -- with keys:
    >  - *name*, *obj* -- the function name and object as returned by `inspect.getmembers`
    >  - *module* -- name of the module
    >  - *path* -- path of the module file
    >  - *doc* -- docstring of the function
    >  - *source* -- source code of the function
    >  - *args* -- arguments of the function as a `inspect.signature` object
    """

    if (
        ignore_prefix_function is not None
        and name[:len(ignore_prefix_function)] == ignore_prefix_function
    ):
        return None

    fun = {}
    fun["name"] = name if name else 'undefined'
    fun["obj"] = obj
    fun["module"] = inspect.getmodule(obj).__name__
    fun["path"] = inspect.getmodule(obj).__file__
    fun["doc"] = inspect.getdoc(obj) or ""
    fun["source"] = rm_docstring_from_source(inspect.getsource(obj))
    fun["args"] = inspect.signature(obj)
    return fun


def create_class(name: str, obj, ignore_prefix_function: str):
    """
    Generate a dictionnary that contains the information about a class

    **Parameters**
    > **name:** `str` -- name of the class as returned by `inspect.getmembers`
    > **obj:** `object` -- object of the class as returned by `inspect.getmembers`
    > **ignore_prefix_function:** `str` -- *None* -- precise the prefix of function or method names to ignore

    **Returns**
    > `dict` -- with keys:
    >  - *name*, *obj* -- the class name and object as returned by `inspect.getmembers`
    >  - *module* -- name of the module
    >  - *path* -- path of the module file
    >  - *doc* -- docstring of the class
    >  - *source* -- source code of the class
    >  - *args* -- arguments of the class as a `inspect.signature` object
    >  - *functions* -- list of functions that are in the class (formatted as dict)
    >  - *methods* -- list of methods that are in the class (formatted as dict)
    >  - *attributes* -- list of attributes that are in the class (formatted as dict)
    """
    clas = {}
    clas["name"] = name
    clas["obj"] = obj
    clas["module"] = inspect.getmodule(obj).__name__
    clas["path"] = inspect.getmodule(obj).__file__
    clas["doc"] = inspect.getdoc(obj) or ""
    clas["source"] = rm_docstring_from_source(inspect.getsource(obj))
    clas["args"] = inspect.signature(obj)
    clas["functions"] = []
    clas["class_attributes"] = []
    clas["methods"] = []    
    clas["object_attributes"] = []        
    method_names = []
    # avoid the collection of create_fun failures, i.e. None returns 
    for n, o in inspect.getmembers(obj, inspect.isfunction):
        method_names.append(n)
        f = create_fun(n, o, ignore_prefix_function)
        if f: clas["functions"].append(f)
    for n, o in inspect.getmembers(obj, inspect.ismethod):
        method_names.append(n)
        f = create_fun(n, o, ignore_prefix_function)
        if f: clas["methods"].append(f)
    builtin_names = __builtin_object_member_names()    
    for n, o in inspect.getmembers(obj):        
        if n not in builtin_names and n not in method_names:
            a = create_att(n, o, ignore_prefix_function)
            if a: clas["class_attributes"].append(a)
    return clas


class_name_md = (
    "## **{0}**`#!py3 class` {{ #{0} data-toc-label={0} }}\n\n".format
)  # name
method_name_md = (
    "### *{0}*.**{1}**`#!py3 {2}` {{ #{1} data-toc-label={1} }}\n\n".format
)  # class, name, args
attribute_name_md = ( 
    "### **{0}** *{1}* {{ #{0} data-toc-label={0} }}\n\n".format
)  # name, type
all_vars_md= (
    "## **Constants and Globals** {{ #Constants-and-Globals data-toc-label=\"Constants and Globals\" }}\n\n".format
)  
all_funcs_md = (
    "## **Functions** {{ #Functions data-toc-label=Functions }}\n\n".format
)  # name
function_name_md = (
    "### **{0}**`#!py3 {1}` {{ #{0} data-toc-label={0} }}\n\n".format
)  # name, args
doc_md = "{}\n".format  # doc
source_md = (
    '\n\n??? info "Source Code" \n\t```py3 linenums="1 1 2" \n{}\n\t```\n'.
    format
)  # source

def write_attribute(md_file, att, clas=None):
    """
    Add the documentation of a function to a markdown file

    **Parameters**
    > **md_file:** `file` -- file object of the markdown file
    > **att:** `dict` -- attribute information organized as a dict (see `create_att`)

    """
    if att is None:
        return

    md_file.writelines(attribute_name_md(att["name"],att["type"])) 
    #md_file.writelines(doc_md(att["doc"]))
    #md_file.writelines(source_md(att["source"]))    

def write_vars_header(md_file): md_file.writelines(all_vars_md())

def write_functions_header(md_file): md_file.writelines(all_funcs_md())

def write_function(md_file, fun):
    """
    Add the documentation of a function to a markdown file

    **Parameters**
    > **md_file:** `file` -- file object of the markdown file
    > **fun:** `dict` -- function information organized as a dict (see `create_fun`)

    """
    if fun is None:
        return

    md_file.writelines(function_name_md(fun["name"], fun["args"]))
    md_file.writelines(doc_md(fun["doc"]))
    md_file.writelines(source_md(fun["source"]))

def write_method(md_file, method, clas):
    """
    Add the documentation of a method to a markdown file

    **Parameters**
    > **md_file:** `file` -- file object of the markdown file
    > **method:** `dict` -- method information organized as a dict (see `create_fun`)
    > **class:** `dict` -- class information organized as a dict (see `create_fun`)

    """
    if method is None:
        return

    md_file.writelines(
        method_name_md(clas["name"], method["name"], method["args"])
    )
    md_file.writelines(doc_md(method["doc"]))
    md_file.writelines(source_md(method["source"]))


def write_class(md_file, clas):
    """
    Add the documentation of a class to a markdown file

    **Parameters**
    > **md_file:** `file` -- file object of the markdown file
    > **clas:** `dict` -- class information organized as a dict (see `create_clas`)

    """
    md_file.writelines(class_name_md(clas["name"]))
    md_file.writelines(doc_md(clas["doc"]))

    if len(clas["class_attributes"]):
        md_file.writelines("\n**class/static attributes:** \n\n")
        for m in clas["class_attributes"]:
            md_file.writelines(" - [`{0}`](#{0})\n".format(m["name"]))

    if len(clas["functions"]) > 0:
        md_file.writelines("\n**class/static methods:** \n\n")
        for f in clas["functions"]:
            md_file.writelines(" - [`{0}`](#{0})\n".format(f["name"]))

    if len(clas["methods"]):
        md_file.writelines("\n**object methods:** \n\n")
        for m in clas["methods"]:
            md_file.writelines(" - [`{0}`](#{0})\n".format(m["name"]))

    if len(clas["object_attributes"]):
        md_file.writelines("\n**object attributes:** \n\n")
        for m in clas["object_attributes"]:
            md_file.writelines(" - [`{0}`](#{0})\n".format(m["name"]))

    md_file.writelines("\n")

    for m in clas["class_attributes"]:
        write_attribute(md_file, m, clas)    

    for f in clas["functions"]:
        write_method(
            md_file, f, clas
        )  # use write_method to get the clas prefix

    for m in clas["methods"]:
        write_method(md_file, m, clas)    

    for m in clas["object_attributes"]:
        write_attribute(md_file, m, clas)    

def write_module(
    path_to_home: str,
    module_import: str,
    path_to_md: str,
    ignore_prefix_function: str = None,
):
    """
    Generate a Markdown file based on the content of a Python module

    **Parameters**
    > **path_to_home:** `str` -- path to the root of the project (2 steps before the `__init__.py`)
    > **module_import:** `str` -- module name (ex: `my_package.my_module`)
    > **path_to_md:** `str` -- path to the output markdown file
    > **ignore_prefix_function:** `str` -- *None* -- precise the prefix of function or method names to ignore

    """
    package_path = os.path.abspath(path_to_home)
    sys.path.insert(0, package_path)

    try:
        module = importlib.import_module(
            module_import, package=module_import.split(".")[0]
        )
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(str(error) + " in " + module_import)

    clas = [
        create_class(n, o, ignore_prefix_function)
        for n, o in inspect.getmembers(module, inspect.isclass)
    ]
    funs = [
        create_fun(n, o, ignore_prefix_function)
        for n, o in inspect.getmembers(module, inspect.isfunction)
    ]

    if not os.path.isdir(os.path.dirname(path_to_md)):
        os.makedirs(os.path.dirname(path_to_md))
    md_file = open(path_to_md, "w")

    for c in clas:
        write_class(md_file, c)
        md_file.writelines("""\n______\n\n""")

    for f in funs:
        write_function(md_file, f)
        md_file.writelines("""\n______\n\n""")

    md_file.close()


def get_toc_lines_from_file_path(mdfile_name):
    lines = ""
    for i, layer in enumerate(mdfile_name.split("/")):
        if i + 1 != len(mdfile_name.split("/")):
            lines += "        " * (i + 1) + "- " + layer + ":\n"
        else:
            lines += "        " * (i + 1) + "- " + mdfile_name + "\n"
    return lines


def write_mkdocs_yaml(path_to_yaml: str, project_name: str, toc: str):
    """
    Generate the YAML file that contains the website configs

    **Parameters**
    > **path_to_yaml:** `str` -- path to the output YAML file
    > **project_name:** `str` -- name of the project
    > **toc:** `str` -- the toc and the all hierarchy of the website
    """
    yaml_file = open(path_to_yaml, "w")
    content = """site_name: {}
theme:
  name: 'material'
nav:
    - Home: index.md
    - Reference:
{}
markdown_extensions:
    - toc:
        toc_depth: 3
        permalink: True
    - extra
    - smarty
    - codehilite
    - admonition
    - pymdownx.details
    - pymdownx.superfences
    - pymdownx.emoji
    - pymdownx.inlinehilite
    - pymdownx.magiclink
    """.format(project_name, toc)
    yaml_file.writelines(content)
    yaml_file.close()


def write_indexmd(path_to_indexmd: str, project_name: str):
    """
    Generate the YAML file that contains the website configs

    **Parameters**
    > **path_to_indexmd:** `str` -- path to the output YAML file
    > **project_name:** `str` -- name of the project
    """
    indexmd_file = open(path_to_indexmd, "w")
    content = """# Welcome to {0}
This website contains the documentation for the wonderful project {0}
""".format(project_name)
    indexmd_file.writelines(content)
    indexmd_file.close()

def __get_module_path( module_name: str ):
    """
    Attempt to import the module/package simply by name.
    If that import fails, check if this package is found on a path 
    relative to the working directory, otherwise raise an exception.
    """
    try:  
        exec( "import %s" % (module_name,) )
        return eval( "inspect.getfile( %s )" % (module_name,) )
    except Exception as error:
        path = os.path.join(os.path.abspath(module_name),'__init__.py')
        if os.path.isfile(path): return path
        print("ERROR: cannot resolve path for module %s" % (module_name,) )
        raise error    
     
def __get_import_module( module_name: str ):
    """
    Returns importlib module
    Attempt to import the module/package simply by name.
    If that import fails, try to import the package by relative path, 
    otherwise raise an exception.
    """
    try:    return __get_import_by_name( module_name, is_silent=True )
    except: return __get_import_by_path( __get_module_path( module_name ) )
   
def __get_import_by_name( name: str, is_silent=False ):        
    try: return importlib.import_module( name )
    except Exception as error:
        if not is_silent:
            print("ERROR: cannot acquire module: %s" % (name,) )
        raise error

def __get_import_by_path( path: str, is_silent=False ):
    package_name = os.path.splitext(os.path.basename(path))[0]
    if package_name=='__init__':
        path = os.path.dirname(path)
        package_name = os.path.basename(path)
        path = os.path.dirname(path)        
    sys.path.insert(0, path)
    try: return importlib.import_module( package_name )
    except Exception as error:
        if not is_silent:
            print("ERROR: cannot acquire module: %s from %s" % 
                  (package_name,path) )
        raise error
    finally: sys.path.remove(path)
    
def __get_source_path( module, member_name ):
    for n, o in inspect.getmembers( module ):
        if n==member_name: 
            try: return inspect.getmodule(o).__file__
            except: 
                default = module.__file__                
                print("Warning: cannot get source path for: %s fall back: %s" % 
                      (member_name,default))
                return default

def __get_import_class_names( module ): 
    return [n for n,_ in inspect.getmembers(module, inspect.isclass)]

def __get_import_func_names( module ): 
    return [n for n,_ in inspect.getmembers(module, inspect.isfunction)]

def __get_import_class( module, classname: str, ignore_prefix_function: str ): 
    for n, o in inspect.getmembers(module, inspect.isclass):
        if n==classname: return create_class(n, o, ignore_prefix_function)

def __get_import_func( module, funcname: str, ignore_prefix_function: str ): 
    for n, o in inspect.getmembers(module, inspect.isfunction):
        if n==funcname: return create_fun(n, o, ignore_prefix_function)

def __get_import_var( module, varname: str, ignore_prefix_function: str ):
    for n, o in __get_import_vars( module ):
        if n==varname: return create_var(n, o, ignore_prefix_function)

def __is_magic_name( name: str ): return name.startswith('__') and name.endswith('__')

def __is_private_name( name: str ): return name.startswith('__')

def __is_protected_name( name: str ): return name.startswith('_')

def __builtin_object_member_names(): return dir(type('dummy', (object,), {}))
        
def __get_import_vars( module ): 
    import_vars=[]
    builtin_names=__builtin_object_member_names()
    for n,o in inspect.getmembers(module):
        if __is_protected_name(n): continue
        if __is_private_name(n): continue
        if __is_magic_name(n): continue        
        if n in builtin_names: continue        
        if inspect.isabstract(o): continue
        if inspect.isasyncgen(o): continue
        if inspect.isasyncgenfunction(o): continue
        if inspect.isawaitable(o): continue
        if inspect.isbuiltin(o): continue
        if inspect.isclass(o): continue
        if inspect.iscode(o): continue
        if inspect.iscoroutine(o): continue
        if inspect.iscoroutinefunction(o): continue
        if inspect.isdatadescriptor(o): continue
        if inspect.isframe(o): continue
        if inspect.isfunction(o): continue
        if inspect.isgenerator(o): continue
        if inspect.isgeneratorfunction(o): continue
        if inspect.isgetsetdescriptor(o): continue
        if inspect.ismemberdescriptor(o): continue
        if inspect.ismethod(o): continue
        if inspect.ismethoddescriptor(o): continue
        if inspect.ismodule(o): continue
        if inspect.isroutine(o): continue
        if inspect.istraceback(o): continue
        import_vars.append((n,o))
    return import_vars
       
def __write_class( md_file, module_path: str, class_name: str ):
    try:
        module = __get_import_by_path( module_path )
        clas = __get_import_class( module, class_name, ignore_prefix_function='_' )        
        if clas:
            write_class(md_file, clas)
            md_file.writelines("""\n______\n\n""")
    except: 
        print("Warning: failed to write definition of class %s from %s" % 
              (class_name, module_path))
        traceback.print_exc()
       
def __write_func( md_file, module_path: str, func_name: str ):
    try:
        module = __get_import_by_path( module_path )
        func = __get_import_func( module, func_name, ignore_prefix_function='_' )        
        if func:
            write_function(md_file, func)
            md_file.writelines("""\n______\n\n""")
    except: 
        print("Warning: failed to write definition of function %s from %s" % 
              (func_name, module_path))
        traceback.print_exc()

def __write_var( md_file, module_path: str, var_name: str ):
    try:
        module = __get_import_by_path( module_path )
        var = __get_import_var( module, var_name, ignore_prefix_function='_' )        
        if var:
            write_attribute(md_file, var)
            md_file.writelines("""\n______\n\n""")
    except: 
        print("Warning: failed to write definition of variable %s from %s" % 
              (var_name, module_path))
        traceback.print_exc()
        
def __parseSnippetIdentifiers( module_name, magic_init_path, source_lines ):   

    def __get_all_names( module ):     
        class_names=[ n for n,_ in inspect.getmembers(module, inspect.isclass) ] 
        func_names=[ n for n,_ in inspect.getmembers(module, inspect.isfunction) ]
        var_names=[ n for n,_ in __get_import_vars( module ) ]
        return class_names, func_names, var_names
    
    def __get_identifier_names( ast_root_node ):        
        parsed_imports=[]    
        for node in ast.walk( ast_root_node ):
            if isinstance( node, (ast.Import, ast.ImportFrom) ):               
                #module =( node.module if isinstance( node, ast.ImportFrom )
                #          else None )                             
                names = [n.asname if n.asname else n.name  
                         for n in node.names]
                parsed_imports.extend( names )
            # CONSTANTS assigned directly in that module perhaps...    
            #if isinstance( node, ast.Assign ):
            #    for target in node.targets:
            #        parsed_imports.append( target.name )
                                        
        return parsed_imports               

    # get all the identifiers, categorized, but not filtered
    module = __get_import_module( module_name )      
    class_names, func_names, var_names = __get_all_names( module )    
    #print( "all_names", class_names, func_names, var_names )
    
    # get the identifiers which are only found in the code snippet 
    package_path = os.path.dirname( magic_init_path )
    sys.path.insert(0, package_path)
    try: ast_root_node = ast.parse( '\n'.join(source_lines) )    
    except Exception as error:
        print("[-]Warning: failed to parse source snippet from %s" % 
               (magic_init_path,), error)
        return None
    #finally: sys.path.remove(package_path)
    snippet_identifier_names = __get_identifier_names( ast_root_node )    
    #print( "snippet_identifier_names", snippet_identifier_names )
    
    # filter the complete lists against the subset of names from the snippet 
    class_names = [n for n in class_names if n in snippet_identifier_names]
    func_names  = [n for n in func_names  if n in snippet_identifier_names]
    var_names   = [n for n in var_names   if n in snippet_identifier_names]

    # get the source paths for the filtered down items being returned
    class_info={}
    for n in class_names: class_info[n] = __get_source_path( module, n )
    func_info={}
    for n in func_names:  func_info[n]  = __get_source_path( module, n )
    var_info={}
    for n in var_names:   var_info[n]   = __get_source_path( module, n )
                            
    return class_info, func_info, var_info

def write_doc(src: str, mainfolder: str, mode=DIR_SCAN_MODE):
    #print( "write_doc", src, mainfolder, mode )
    # variables
    project_icon = "code"  # https://material.io/tools/icons/?style=baseline
    # setting the paths variable
    project_name = mainfolder.split("/")[-1]
    doc_path = os.path.join(os.path.abspath(mainfolder), "docs")
    if not os.path.isdir(doc_path): os.makedirs(doc_path)
    # init table of contents
    toc = ""
 
    if mode==IMPORT_SCAN_MODE: 
        path_head,path_tail=os.path.split( src )
        if len(path_head) > 0:
            orginal_wrkdir = os.path.abspath(os.curdir)
            os.chdir(path_head)              
        else: orginal_wrkdir = None    
        package_name = path_tail
        magic_init_path = __get_module_path( package_name ) 
        #print( "package init_path", magic_init_path )                    
        # Build this raw "markdown map" first via "magic comments"   
        mdMap={} # { markdown_file_path : source_lines }    
        try: 
            with open( magic_init_path, 'r' ) as f: init_content=f.read()
        except Exception as error: 
            print("ERROR: cannot read from path: %s" % (magic_init_path,))
            raise error        
        lines = init_content.split('\n')
        mdfile_name = None        
        if MAGIC_DOCNAME_COMMENT in init_content:
            source_lines=[]
            for line in lines:
                if line.strip().startswith( MAGIC_DOCNAME_COMMENT ):
                    try: 
                        input_name=line.split( MAGIC_DOCNAME_COMMENT )[1].strip()
                    except Exception as error: 
                        input_name=None
                        print("[-]Error processing magic comment: %s" % 
                              (line,), error)
                    if input_name != mdfile_name:                                                                                 
                        if mdfile_name:
                            mdMap[mdfile_name]=[]
                            mdMap[mdfile_name].extend(source_lines)
                        mdfile_name=input_name
                        source_lines=[]                    
                source_lines.append(line)                   
            if mdfile_name:
                mdMap[mdfile_name]=[]
                mdMap[mdfile_name].extend(source_lines)
        else:                
            mdfile_name = "%s.md" % (package_name,) 
            mdMap[mdfile_name]=lines
        
        # Process the "markdown map", generating the requested docs
        #print( "mdMap", mdMap )    
        for mdfile_name in mdMap: 
            source_lines=mdMap[mdfile_name]
            parsed = __parseSnippetIdentifiers( 
                package_name, magic_init_path, source_lines )
            #print( "parsed", parsed )
            if not parsed: continue                           
            mdfile_path = os.path.join(doc_path, mdfile_name)    
            md_file = open( mdfile_path, "w")   
            #print("Writing document: %s" % (mdfile_name,))  
            class_info, func_info, var_info = parsed
            #print( class_info, func_info, var_info )       # (path)
            for name in class_info: __write_class(md_file, class_info[name], name)
            if len(func_info) > 0 and len(class_info) > 0: write_functions_header(md_file)
            for name in func_info: __write_func(md_file, func_info[name], name)     
            if len(var_info) > 0 and (len(func_info) > 0 or len(class_info) > 0): 
                write_vars_header(md_file)
            for name in var_info:  __write_var(md_file, var_info[name], name)                           
            md_file.close()    
            try: toc += get_toc_lines_from_file_path(mdfile_name)
            except Exception as error: print("[-]Warning ", error)   
        # restore working directory if it were changed
        if orginal_wrkdir: os.chdir(orginal_wrkdir)
    else:         
        code_path = os.path.abspath(src)
        package_name = code_path.split("/")[-1]
        root_path = os.path.dirname(code_path)
         
        # load the architecture of the module
        ign_pref_file = "__"
        full_list_glob = glob.glob(code_path + "/**", recursive=True)
        list_glob = [
            p
            for p in full_list_glob
            if "/" + ign_pref_file not in p and os.path.isfile(p) and p[-3:] == ".py" \
                and "__init__" not in p
        ]

        # write every markdown files based on the architecture
        #Since windows and Linux platforms utilizes different slash in their file structure
        system_slash_style = {"Windows": "\\", "Linux": "/"}                
        for mod in list_glob:
            module_name = mod[len(root_path) + 1 : -3]\
                .replace(system_slash_style.get(platform.system(), "/"), ".")
            mdfile_path = os.path.join(
                doc_path, mod[len(code_path) + 1:-3] + ".md"
            )
            mdfile_name = mdfile_path[len(doc_path) + 1:]
            try:
                write_module(root_path, module_name, mdfile_path)
                toc += get_toc_lines_from_file_path(mdfile_name)
            except Exception as error:
                print("[-]Warning ", error)

    #print( "toc", toc )
    if len(toc) == 0:
        raise ValueError("All the files seem invalid")
    
    #removed the condition because it would'nt update the yml file in case
    #of any update in the source code
    yml_path = os.path.join(mainfolder, 'mkdocs.yml')
    write_mkdocs_yaml(yml_path, project_name, toc)

    index_path = os.path.join(doc_path, 'index.md')
    write_indexmd(index_path, project_name)
    """
    if not os.path.isfile(yml_path):
        write_mkdocs_yaml(yml_path, project_name, toc)

    index_path = os.path.join(doc_path, 'index.md')
    if not os.path.isfile(index_path):
        write_indexmd(index_path, project_name)
    """
