#!/usr/bin/env python
import os
import sys
from subprocess import call, Popen
import webbrowser
import traceback
from automacdoc import write_doc, DIR_SCAN_MODE, IMPORT_SCAN_MODE

def main(argv=None):
    args = __parse_args(sys.argv if argv is None else argv)
    if isinstance(args,int): return args
    src, dest, is_serve, options = args
    try: 
        write_doc(src, dest, options)
        os.chdir(dest)
        call(["mkdocs", "build", "--clean"])    
        if is_serve:
            Popen(["mkdocs", "serve"])
            webbrowser.open("http://127.0.0.1:8000/")    
        return 0                
    except Exception as error:
        print("[-] Error ", str(error))
        traceback.print_exc()
        return 1

def __parse_args(argv):
    # Note argparse wasn't employed simply to avoid that dependency...
    HELP_SWITCHES      = ["-h","--help","/?"]
    DIR_SCAN_SWITCH    = "-d"     
    IMPORT_SCAN_SWITCH = "-i"
    SOURCE_SWITCH      = "-c"
    SERVE_SWITCH       = "-s"
    TITLE = "| AutoMacDoc |"
    DESCR = "Generates MkDoc website from Python source code"
    USAGE =("Usage: automacdoc source destination [{0}/{1}] [{2}] [{3}]\n"
            "{0}: directory scan mode (default) / {1}: import scan mode\n"
            "{2}: include source code\n"
            "{3}: serve site option\n").format( 
            DIR_SCAN_SWITCH, IMPORT_SCAN_SWITCH, SOURCE_SWITCH, SERVE_SWITCH)
 
    argv = sys.argv if argv is None else argv
    arg_count = len(argv)-1
    switches = argv[2:]
         
    is_invalid = arg_count < 2    
    is_help = False
    for switch in HELP_SWITCHES:
        is_help=switch in argv
        if is_help: break        
    if is_invalid or is_help:
        print(TITLE)
        print(DESCR)
        print(USAGE)
        return 1 if is_invalid else 0
    
    src      = argv[1] 
    dest     = argv[2]   
    is_serve = SERVE_SWITCH in switches
    mode     = (IMPORT_SCAN_MODE if IMPORT_SCAN_SWITCH in switches 
                else DIR_SCAN_MODE)
    options  = {
          "mode": mode
        , "is_source_shown": SOURCE_SWITCH in switches
        , "ignore_prefix": '_' if mode==IMPORT_SCAN_MODE else None         
        }
    return src, dest, is_serve, options 
     
if __name__ == "__main__": sys.exit(main(sys.argv))
