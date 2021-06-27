#!/usr/bin/env python
import os
import sys
from subprocess import call, Popen
import webbrowser
import traceback
from automacdoc import write_doc, DIR_SCAN_MODE, IMPORT_SCAN_MODE

HELP_SWITCHES      = ["-h","--help","/?"]
SERVE_SWITCH       = "-s"
DIR_SCAN_SWITCH    = "-d"     
IMPORT_SCAN_SWITCH = "-i"
TITLE = "---| AutoMacDoc |---"
USAGE =("Usage: automacdoc [{0}/{1}] source destination [{2}]\n"
        "{0}: directory scan mode (default) / {1}: import scan mode\n"
        "{2}: serve site option\n"
        ).format( DIR_SCAN_SWITCH, IMPORT_SCAN_SWITCH, SERVE_SWITCH )

__MODES={ DIR_SCAN_SWITCH:DIR_SCAN_MODE
        , IMPORT_SCAN_SWITCH:IMPORT_SCAN_MODE }
 
def main(argv=None):
    argv = sys.argv if argv is None else argv
    is_help = False
    for switch in HELP_SWITCHES:
        is_help=switch in argv
        if is_help: break
    if is_help:
        print(TITLE)
        print(USAGE)
        return 0
    arg_count = len(argv)-1
    argv1 = argv[1] if arg_count >= 1 else None
    argv2 = argv[2] if arg_count >= 2 else None
    argv3 = argv[3] if arg_count >= 3 else None        
    src        = argv1 if arg_count < 3 else argv2
    mainfolder = argv2 if arg_count < 3 else argv3  
    mode       = __MODES.get(argv1,DIR_SCAN_MODE)    
    is_serve   = SERVE_SWITCH in argv
    
    try: write_doc( src, mainfolder, mode )        
    except Exception as error:
        print("[-] Error ", str(error))
        traceback.print_exc()
        return 1

    os.chdir(mainfolder)
    call(["mkdocs", "build", "--clean"])
    
    if is_serve:
        Popen(["mkdocs", "serve"])
        webbrowser.open("http://127.0.0.1:8000/")
    
    return 0

if __name__ == "__main__": sys.exit(main(sys.argv))
