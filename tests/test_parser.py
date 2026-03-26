from CodeCleaner.parser import Parser

'''
def test_parser():
    parser.clean_file()
    parser.print_lines()
'''

def test_parser():
    lines = ['#include <stdio.h> // helps in I/O\n',
             '#include <stdlib.h> /* provides memory related function */\n',
             '  \n',
             'int main(){\n',
             '\tint a; // This is a variable\n',
             '}\n',
             '']
    cleaned_lines = ['#include <stdio.h> \n',
                     '#include <stdlib.h> \n',
                     '  \n',
                     'int main(){\n',
                     '\tint a; \n',
                     '}\n',
                     '']
    parser = Parser(['//', '/*', '*/', '"'],lines)
    new_lines = parser.clean_file()
    assert new_lines == cleaned_lines
    '''
    file = open('tests/testfiles/test.h')
    lines = file.readlines()
    parser = Parser(['//', '/*', '*/', '"'],lines)
    parser.clean_file()
    #parser.print_lines()
    file.close()
    ''' 
