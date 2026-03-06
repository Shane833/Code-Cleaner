from CodeCleaner.parser import Parser

file = open('CodeCleaner/hashmap.c')
parser = Parser(file.readlines())

def test_parser():
    parser.clean_file()
    parser.print_lines()
