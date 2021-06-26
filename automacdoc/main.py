#!/usr/bin/env python
import os
import sys
from subprocess import call, Popen
import webbrowser
import traceback
from automacdoc import write_doc, DIR_SCAN_MODE, IMPORT_SCAN_MODE

DIR_SCAN_SWITCH    = '-d'     
IMPORT_SCAN_SWITCH = '-i'
__MODES={ DIR_SCAN_SWITCH:DIR_SCAN_MODE
        , IMPORT_SCAN_SWITCH:IMPORT_SCAN_MODE }
 
def main(argv=None):
    argv = sys.argv if argv is None else argv
    arg_count = len(argv)-1
    argv1 = argv[1] if arg_count >= 1 else None
    argv2 = argv[2] if arg_count >= 2 else None
    argv3 = argv[3] if arg_count >= 3 else None        
    src        = argv1 if arg_count < 3 else argv2
    mainfolder = argv2 if arg_count < 3 else argv3  
    mode       = __MODES.get(argv1,DIR_SCAN_MODE)
    
    try:         
        write_doc( src, mainfolder, mode )        
    except Exception as error:
        print("[-] Error ", str(error))
        traceback.print_exc()
        return

    os.chdir(mainfolder)
    call(["mkdocs", "build", "--clean"])
    Popen(["mkdocs", "serve"])

    webbrowser.open("http://127.0.0.1:8000/")

if __name__ == "__main__":
    main(sys.argv)
