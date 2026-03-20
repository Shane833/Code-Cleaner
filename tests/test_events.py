import sys
import pytest
from CodeCleaner.events import *

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

    # Trying 
    event = Event('#', None, None, None)

    line = "a = 2 # This is a variable"
    current_idx = 6
    new_idx = event.match_marker(line, current_idx, '#')
    assert new_idx == 7

def test_scanTokens():
    # C Family - C, C++, Java, JavaScript
    event = Event('//', '/*', '*/', '"')

    line = "// /* */"
    tokens = event.scanTokens(line)
    assert tokens == [(0, Token.SINGLE_COMM)]

    line = "int a; // This is a variable /*"
    tokens = event.scanTokens(line)
    assert tokens == [(7, Token.SINGLE_COMM)]

    line = "/**///"
    tokens = event.scanTokens(line)
    assert tokens == [(0, Token.MULTI_LINE_COMM_START),
                      (2, Token.MULTI_LINE_COMM_END),
                      (4, Token.SINGLE_COMM)]
    
    line = 'char *s = "String";'
    tokens = event.scanTokens(line)
    assert tokens == [(10, Token.STRING),
                      (17, Token.STRING)]
    
    line = 'char s[10] = "Shane"; /* String */ // single comment'
    tokens = event.scanTokens(line)
    assert tokens == [(13, Token.STRING),
                      (19, Token.STRING),
                      (22, Token.MULTI_LINE_COMM_START),
                      (32, Token.MULTI_LINE_COMM_END),
                      (35, Token.SINGLE_COMM)]

    # Python
    event = Event('#', None, None, None)
    line = "if a == 2: # check condition"
    tokens = event.scanTokens(line)
    assert tokens == [(11, Token.SINGLE_COMM)]

    # HTML
    event = Event(None, '<!--', '-->', None)
    line = "<p>This is a text</p> <!-- This a comment -->"
    tokens = event.scanTokens(line)
    assert tokens == [(22, Token.MULTI_LINE_COMM_START),
                      (42, Token.MULTI_LINE_COMM_END)]

