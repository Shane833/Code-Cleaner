import sys
import pytest
from CodeCleaner.events import *

'''
# creating an object of event
event = Event()

def test_scanline():
    line = "\t \n"
    event = Event()
    result = event.scanline(line)
    assert result == [(0, Token.EMPTY_LINE)]
    
    line = "//"
    event = Event()
    result = event.scanline(line)
    assert result == [(0, Token.SINGLE_COMM)]

    line = '"'
    event = Event()
    result = event.scanline(line)
    assert event.state == Event.State.IN_STRING
    assert result == [(0, Token.STRING_START)]
    
    line = "/*"
    event = Event()
    result = event.scanline(line)
    assert event.state == Event.State.IN_MULTI_LINE_COMM
    assert result == [(0, Token.MULTI_LINE_COMM_START)]

    line = "/**/"
    event = Event()
    result = event.scanline(line)
    assert event.state == Event.State.DEFAULT
    assert result == [(0, Token.MULTI_LINE_COMM_START), (4, Token.MULTI_LINE_COMM_END)]

    line = "// /* */"
    event = Event()
    result = event.scanline(line)
    assert result == [(0, Token.SINGLE_COMM)]

    line = "/* */ //"
    event = Event()
    result = event.scanline(line)
    assert result == [(0, Token.MULTI_LINE_COMM_START),
                      (5, Token.MULTI_LINE_COMM_END),
                      (6, Token.SINGLE_COMM)]

    line = 'char *s = "This is a string";'
    event = Event()
    result = event.scanline(line)
    assert result == [(10, Token.STRING_START), (27, Token.STRING_END)]

    line = '" /**/ // '
    event = Event()
    result = event.scanline(line)
    assert event.state == Event.State.IN_STRING
    assert result == [(0, Token.STRING_START)]
    
def test_scanfile():
    event = Event()
    lines = ['#include <stdio.h> // helps in I/O',
             '#include <stdlib.h> /* provides memory related function */',
             '  ',
             'int main(){',
             '\tint a; // This is a variable',
             '}\n',
             '']

    token_table = event.scanfile(lines)
    assert event.state == Event.State.DEFAULT
    print(token_table)

    lines = ["/* I going to span "," across lines */"]
    token_table = event.scanfile(lines)
    assert event.state == Event.State.DEFAULT
    print(token_table)

    lines = ['char *s = "This string will\'',
             '\t\t\tis going span two lines"'
             ]
    token_table = event.scanfile(lines)
    assert event.state == Event.State.DEFAULT
    print(token_table)
'''

def test_match_marker():
    event = Event('//', '/*', '*/', '"')

    line = "int main() // Main function"
    current_idx = 11
    new_idx = event.match_marker(line, current_idx, '//')
    assert new_idx == 13

    line = 'char *s = "String";'
    current_idx = 10
    new_idx = event.match_marker(line, current_idx, '"')
    assert new_idx == 11

    line = "/* A Multiline Comment */"
    current_idx = 0
    new_idx = event.match_marker(line, current_idx, '/*')
    assert new_idx == 2

    current_idx = 23
    new_idx = event.match_marker(line, current_idx, '*/')
    assert new_idx == 25

def test_scanTokens():
    event = Event('//', '/*', '*/', '"')

    line = "// /* */"
    tokens = event.scanTokens(line)
    #print(tokens)

    line = "int a; // This is a variable /*"
    tokens = event.scanTokens(line)
    #print(tokens)

    line = "/**///"
    tokens = event.scanTokens(line)
    #print(tokens)

    line = 'char *s = "String";'
    tokens = event.scanTokens(line)
    print(tokens)

    line = 'char s[10] = "Shane"; /* String */ // single comment'
    tokens = event.scanTokens(line)
    #print(tokens)
