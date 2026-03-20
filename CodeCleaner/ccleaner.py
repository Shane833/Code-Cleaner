#!/usr/bin/env python3

# TODO : Things to still implement
# 1. Handle strings in python
# 2. Handle escape characters

from pathlib import Path
from parser import Parser
from enum import Enum
import sys

# define some exceptions
class UnSupportedFileTypeError(Exception):
    pass

class Option(Enum):
    DEFAULT = 0
    OVERWRITE = 1

class Language(Enum):
    C_FAMILY = 1
    PYTHON = 2
    HTML = 3

# Mapping of options
options = {"-i": Option.OVERWRITE}

# Mapping of languages
languages = {".h" : Language.C_FAMILY, ".c" : Language.C_FAMILY,
             ".cpp" : Language.C_FAMILY, ".hpp": Language.C_FAMILY,
             ".java" : Language.C_FAMILY, ".js" : Language.C_FAMILY,
             ".py" : Language.PYTHON, ".html" : Language.HTML}

# Mapping of markers for languages
markers = {Language.C_FAMILY : ['//', '/*', '*/', '"'],
          Language.PYTHON: ['#', None, None, None],
          Language.HTML : [None, '<!--', '-->', None]}

# Basic Util function
def correctUsage():
    logInfo("USAGE -> python ccleaner.py [OPTIONS] [FILES]")

def logError(msg):
    print(f"[ERROR] : {msg}")

def logInfo(msg):
    print(f"[INFO] : {msg}")

# Command line Argument Handling
def processArguments(arguments):
    file_paths = []
    selected_option = Option.DEFAULT
    
    if len(arguments) == 1:
        correctUsage()
        exit(1)
    else:
        # Check for gloabal options, if provided
        if arguments[1] in options.keys():
            # Then set the option
            selected_option = options[arguments[1]]
            # then look for the files
            for i in range(2, len(arguments)):
                file_paths.append(arguments[i])
        else:
            # else go with the default and only store files
            for i in range(1, len(arguments)):
                file_paths.append(arguments[i])
        
        if len(file_paths) == 0:
            logError("No files provided!")
            correctUsage()
            exit(1)

    return (selected_option, file_paths)

def processFile(option, file_path):
    # Using the options provided it will make changes in the file
    try:
        file = open(file_path, 'r+')
        path = Path(file_path)
        # details regarding the file
        name = path.stem
        extension = path.suffix
        parent = path.parent
        # Source Code language to identify comment types
        lang_type = None
        lang_markers = None
        # Find the source language using the extension
        if extension in languages.keys():
            lang_type = languages[extension]
            lang_markers = markers[lang_type]

        # Invalid file type 
        if not lang_type:
            raise UnSupportedFileTypeError()

        # Clean it
        parser = Parser(lang_markers, file.readlines())
        cleaned_lines = parser.clean_file()

        if option == Option.DEFAULT:
            # create a new file and write the cleaned data in it
            new_file_path = f"{parent}/{name}_cleaned{extension}"
            try:
                new_file = open(new_file_path, 'w+')
                new_file.writelines(cleaned_lines)
                new_file.flush()
                new_file.close()
                logInfo(f"{new_file_path} GENERATED!")
            except:
                logError("FAILED TO GENERATE FILE!")

        elif option == Option.OVERWRITE:
            # make changes in the same file
            file.seek(0)
            file.truncate()
            file.writelines(cleaned_lines)
            file.flush()
            logInfo(f"{file_path} CLEANED!")
        file.close()

    except FileNotFoundError:
        logError(f"{file_path} FILE NOT FOUND!")
    except UnSupportedFileTypeError:
        logError(f"{file_path} UNSUPPORTED FILE TYPE!")
        logInfo(f"{file_path} SKIPPED!")


def main():
    option, file_paths = processArguments(sys.argv)

    for file_path in file_paths:
        processFile(option, file_path)
    

if __name__ == "__main__":
    main()
