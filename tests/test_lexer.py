import pytest
from CodeCleaner.lexer import *

# creating an object of lex
lex = Lexer()

def test_empty_line():
    lines = ["\t\n","int a","      ", "         {"]
    assert lex.is_empty_line(lines[0]) == True   
    assert lex.is_empty_line(lines[1]) == False
    assert lex.is_empty_line(lines[2]) == True
    assert lex.is_empty_line(lines[3]) == False

def test_single_comm():
    lines = ["//","int a; // This is a variable","\t\t\n","// * Hey // there\t\t",
             "/* // */","#include <stdio.h>\n"]
    assert lex.has_single_comm(lines[0],'//') != -1
    assert lex.has_single_comm(lines[1],'//') != -1
    assert lex.has_single_comm(lines[2],'//') == -1
    assert lex.has_single_comm(lines[3],'//') != -1
    assert lex.has_single_comm(lines[4],'//') != -1
    assert lex.has_single_comm(lines[5],'//') == -1

def test_multi_line_comm_start():
    lines = ["/**/","float b; /* multi line comm","// /* // */",
             "int main{/* This is the main function */","/* */ //",
             "\t\t\n","int a"]
    assert lex.has_multi_line_comm_start(lines[0],"/*") != -1
    assert lex.has_multi_line_comm_start(lines[1],"/*") != -1
    assert lex.has_multi_line_comm_start(lines[2],"/*") != -1
    assert lex.has_multi_line_comm_start(lines[3],"/*") != -1
    assert lex.has_multi_line_comm_start(lines[4],"/*") != -1
    assert lex.has_multi_line_comm_start(lines[5],"/*") == -1
    assert lex.has_multi_line_comm_start(lines[6],"/*") == -1

def test_multi_line_comm_end():
    lines = ["/**/","float b; /* multi line comm","// /* // */",
             "int main{/* This is the main function */","/* */ //",
             "\t\t\n","int a"]
    assert lex.has_multi_line_comm_end(lines[0],"*/") != -1
    assert lex.has_multi_line_comm_end(lines[1],"*/") == -1
    assert lex.has_multi_line_comm_end(lines[2],"*/") != -1
    assert lex.has_multi_line_comm_end(lines[3],"*/") != -1
    assert lex.has_multi_line_comm_end(lines[4],"*/") != -1
    assert lex.has_multi_line_comm_end(lines[5],"*/") == -1
    assert lex.has_multi_line_comm_end(lines[6],"*/") == -1

def test_scanline():
    line = "\t \n"
    result = lex.scanline(line)
    assert result == [(0, Token.EMPTY_LINE)]

    line = "/**/"
    result = lex.scanline(line)
    assert result == [(0, Token.MULTI_LINE_COMM_START), (2, Token.MULTI_LINE_COMM_END)]

    line = "// /* */"
    result = lex.scanline(line)
    assert result == [(0, Token.SINGLE_COMM),
                      (3,Token.MULTI_LINE_COMM_START),
                      (6, Token.MULTI_LINE_COMM_END)]
