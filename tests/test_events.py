import sys
import pytest
from CodeCleaner.events import *

# creating an object of event
event = Event()

'''
def test_empty_line():
    lines = ["\t\n","int a","      ", "         {"]
    assert event.is_empty_line(lines[0]) == True   
    assert event.is_empty_line(lines[1]) == False
    assert event.is_empty_line(lines[2]) == True
    assert event.is_empty_line(lines[3]) == False

def test_single_comm():
    lines = ["//","int a; // This is a variable","\t\t\n","// * Hey // there\t\t",
             "/* // */","#include <stdio.h>\n"]
    assert event.has_single_comm(lines[0],'//') != -1
    assert event.has_single_comm(lines[1],'//') != -1
    assert event.has_single_comm(lines[2],'//') == -1
    assert event.has_single_comm(lines[3],'//') != -1
    assert event.has_single_comm(lines[4],'//') != -1
    assert event.has_single_comm(lines[5],'//') == -1

def test_multi_line_comm_start():
    lines = ["/**/","float b; /* multi line comm","// /* // */",
             "int main{/* This is the main function */","/* */ //",
             "\t\t\n","int a"]
    assert event.has_multi_line_comm_start(lines[0],"/*") != -1
    assert event.has_multi_line_comm_start(lines[1],"/*") != -1
    assert event.has_multi_line_comm_start(lines[2],"/*") != -1
    assert event.has_multi_line_comm_start(lines[3],"/*") != -1
    assert event.has_multi_line_comm_start(lines[4],"/*") != -1
    assert event.has_multi_line_comm_start(lines[5],"/*") == -1
    assert event.has_multi_line_comm_start(lines[6],"/*") == -1

def test_multi_line_comm_end():
    lines = ["/**/","float b; /* multi line comm","// /* // */",
             "int main{/* This is the main function */","/* */ //",
             "\t\t\n","int a"]
    assert event.has_multi_line_comm_end(lines[0],"*/") != -1
    assert event.has_multi_line_comm_end(lines[1],"*/") == -1
    assert event.has_multi_line_comm_end(lines[2],"*/") != -1
    assert event.has_multi_line_comm_end(lines[3],"*/") != -1
    assert event.has_multi_line_comm_end(lines[4],"*/") != -1
    assert event.has_multi_line_comm_end(lines[5],"*/") == -1
    assert event.has_multi_line_comm_end(lines[6],"*/") == -1
'''

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


