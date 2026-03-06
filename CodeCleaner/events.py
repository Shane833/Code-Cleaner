# We will be tokenizing the lines depending on what they contain
# We can have single line comment, multiline comment start, 
# multiline comment end, empty line

# Event will only work on lines provided in the function parameters

from enum import Enum

class Token(Enum):
    EMPTY_LINE = 1
    SINGLE_COMM = 2
    MULTI_LINE_COMM_START = 3
    MULTI_LINE_COMM_END = 4 
    STRING_START = 5 # Adding this bcz we don't want to erase comments inside strings
    STRING_END = 6 # can span over multiple lines

class Event(object):

    class State(Enum):
        DEFAULT = 1
        IN_STRING = 2
        IN_MULTI_LINE_COMM = 3
        
    def __init__(self):
        self.state = Event.State.DEFAULT # used to monitor when inside string we ignore scanning

    def is_empty_line(self,line) -> bool:
        '''go through the line and determines if its just for formatting'''
        return line.strip() == "" # simple way, i.e. after removing all the whitespace if we are left with nothing then its an empty line

    def peek_and_match(self, index, line, marker) -> bool:
        # since at the end of the file a new line char is always present
        # so it means I don't have to worry about index out of bound error
        # But there was a bug bcz I didn't handle the when we start reaching
        # the end of line and encounter 
        return line[index+1] == marker if index + 1 < len(line) else False 

    def scanline(self, line) -> list[tuple[int, Token]]:
        tokens = []
        # Scan for empty line
        if self.is_empty_line(line):
            tokens.append((0, Token.EMPTY_LINE))
        else:
            for idx,char in enumerate(line):
                if char == '/': # TODO : Scanning based on fixed characters(assuming 2 char strings) which is wrong 
                    # skip if inside a string or multiline comm
                    if self.state == Event.State.DEFAULT:
                        if self.peek_and_match(idx, line, '/'):
                            tokens.append((idx, Token.SINGLE_COMM))
                            break # break out of the loop as anything after that will be ignored anyways
                        elif self.peek_and_match(idx, line, '*'): 
                            tokens.append((idx, Token.MULTI_LINE_COMM_START))
                            self.state = Event.State.IN_MULTI_LINE_COMM

                if char == '*':
                    if self.state == Event.State.IN_MULTI_LINE_COMM:
                        if self.peek_and_match(idx, line, '/'):
                            tokens.append((idx + 2, Token.MULTI_LINE_COMM_END))
                            self.state = Event.State.DEFAULT

                elif char == '"':
                    # first check the current and then modify
                    # if we are already in a multiline comm then no need 
                    # change the state
                    if self.state == Event.State.DEFAULT:
                        self.state = Event.State.IN_STRING
                        tokens.append((idx, Token.STRING_START))
                    elif self.state == Event.State.IN_STRING:
                        self.state = Event.State.DEFAULT
                        tokens.append((idx, Token.STRING_END))
                    else: # ignore inside a multiline comm
                        pass

        return tokens

    def scanfile(self, lines) -> list[tuple[int, list[tuple[int, Token]]]]:
        # Generates a token table for the whole file
        token_table = []
        for idx,line in enumerate(lines):
            token_table.append((idx,self.scanline(line)))

        return token_table
        
