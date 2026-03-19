#!/usr/bin/env python3

from pathlib import Path
from parser import Parser
from enum import Enum
import sys

class Options(Enum):
    DEFAULT = 0
    OVERWRITE = 1

class Languages(Enum):
    C_FAMILY = 1

# Map the options
options = {"-i": Options.OVERWRITE}

# Mapping of lanugaes
languages = {".h" : Languages.C_FAMILY, ".c" : Languages.C_FAMILY,
             ".cpp" : Languages.C_FAMILY, ".hpp": Languages.C_FAMILY}

def correctUsage():
    print("USAGE : python ccleaner.py [OPTIONS] [FILES]")

def processArguments(arguments):
    file_paths = []
    selected_option = Options.DEFAULT
    
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
            print("ERROR : No files provided!")
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

        # Find the source language using the extension
        if extension in languages.keys():
            lang_type = languages[extension]
        # TODO: Make use of the extensions

        # Clean it
        parser = Parser(file.readlines())
        cleaned_lines = parser.clean_file()

        if option == Options.DEFAULT:
            # create a new file and write the cleaned data in it
            new_file_path = f"{parent}/{name}_cleaned{extension}"
            try:
                new_file = open(new_file_path, 'w+')
                new_file.writelines(cleaned_lines)
                new_file.flush()
                new_file.close()
            except:
                print("UNKNOWN ERROR!")

        elif option == Options.OVERWRITE:
            # make changes in the same file
            file.seek(0)
            file.truncate()
            file.writelines(cleaned_lines)
            file.flush()

        file.close()

    except FileNotFoundError:
        print(f"ERROR : {file_path} file not found!")

def main():
    option, file_paths = processArguments(sys.argv)

    for file_path in file_paths:
        processFile(option, file_path)
    

if __name__ == "__main__":
    main()
