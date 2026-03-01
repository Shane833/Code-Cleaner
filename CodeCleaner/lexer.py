# We will be tokenizing the lines depending on what they contain
# We can have single line comment, multiline comment start, 
# multiline comment end, empty line

# Lexer will only work on lines provided in the function parameters

from enum import Enum

class Token(Enum):
    EMPTY_LINE = 1
    SINGLE_COMM = 2
    MULTI_LINE_COMM_START = 3
    MULTI_LINE_COMM_END = 4
    STRING_START = 5 # Adding this bcz we don't want to erase comments inside strings
    STRING_END = 6 # can span over multiple lines

class Lexer(object):

    class State(Enum):
        DEFAULT = 1
        IN_STRING = 2
        IN_MULTI_LINE_COMM = 3
        
    def __init__(self):
        self.state = Lexer.State.DEFAULT # used to monitor when inside string we ignore scanning

    def is_empty_line(self,line) -> bool:
        '''go through the line and determines if its just for formatting'''
        return line.strip() == "" # simple way, i.e. after removing all the whitespace if we are left with nothing then its an empty line

    # Providing an additional argument in identifying the comment characters
    # so that the same function can be used for different language comments
    def has_single_comm(self, line, marker) -> int:
        '''if the single line comment is found then simply
           return the index within the line else returns -1'''
        return line.find(marker)

    def has_multi_line_comm_start(self, line, marker) -> int:
        ''' If contains /* simply return the index else -1 '''
        return line.find(marker)

    def has_multi_line_comm_end(self, line, marker) -> int:
        ''' If contains */ simply return the index else -1'''
        return line.find(marker)

    def has_string(self, line,marker):
        ''' If contains "" simply return the index else -1 '''
        return line.find(marker)

    def scanline(self, line) -> list[tuple[int,Token]]:
        ''' Go through the line and indentify all the tokens '''
        index = 0
        result = [] # list of tokens

        # If empty line don't bother
        if self.is_empty_line(line):
            result.append((index, Token.EMPTY_LINE))
        else:
            index = self.has_single_comm(line,'//')
            if index != -1:
                result.append((index, Token.SINGLE_COMM))
            
            index = self.has_multi_line_comm_start(line, '/*')
            if index != -1:
                result.append((index, Token.MULTI_LINE_COMM_START))
            
            index = self.has_multi_line_comm_end(line, '*/')
            if index != -1:
                result.append((index, Token.MULTI_LINE_COMM_END))

        return result

    def scanfile(self, file):
        pass
