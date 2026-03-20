# We will be tokenizing the lines depending on what they contain
# We can have single line comment, multiline comment start, 
# multiline comment end, empty line

# Event will only work on lines provided in the function parameters

from enum import Enum

''' Modifying the Tokens to make it work with scanTokens()
class Token(Enum):
    EMPTY_LINE = 1
    SINGLE_COMM = 2
    MULTI_LINE_COMM_START = 3
    MULTI_LINE_COMM_END = 4 
    STRING_START = 5 # Adding this bcz we don't want to erase comments inside strings
    STRING_END = 6 # can span over multiple lines
'''
class Token(Enum):
    EMPTY_LINE = 1
    SINGLE_COMM = 2
    MULTI_LINE_COMM_START = 3
    MULTI_LINE_COMM_END = 4 
    STRING = 5 # making string have a single token 

class Event(object):

    class State(Enum):
        DEFAULT = 1
        IN_STRING = 2
        IN_MULTI_LINE_COMM = 3
        
    def __init__(self,single_comm_marker,multi_line_comm_start_marker, 
                 multi_line_comm_end_marker, string_marker):
        self.state = Event.State.DEFAULT # used to monitor when inside string we ignore scanning
        # TODO : Allowing different types of comments to be processed
        self.comment_markers = {Token.SINGLE_COMM : single_comm_marker,
                                Token.MULTI_LINE_COMM_START : multi_line_comm_start_marker,
                                Token.MULTI_LINE_COMM_END : multi_line_comm_end_marker,
                                Token.STRING : string_marker}
    '''
    def __init__(self):
        self.state = Event.State.DEFAULT # used to monitor when inside multiline comm or string
    '''

    def is_empty_line(self,line) -> bool:
        '''go through the line and determines if its just for formatting'''
        return line.strip() == "" # simple way, i.e. after removing all the whitespace if we are left with nothing then its an empty line
    '''
    #TODO: The function name doesn't suggest what it really does
    def peek_and_match(self, index, line, marker) -> bool:
        # since at the end of the file a new line char is always present
        # so it means I don't have to worry about index out of bound error
        # But there was a bug bcz I didn't handle the when we start reaching
        # the end of line and encounter 
        return line[index + 1] == marker if index + 1 < len(line) else False 
    ''' 
    '''
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
    '''
    '''
    def scanfile(self, lines) -> list[tuple[int, list[tuple[int, Token]]]]:
        # Generates a token table for the whole file
        token_table = []
        for idx,line in enumerate(lines):
            token_table.append((idx,self.scanline(line)))

        return token_table
    '''
    # Modifying scanfile function to use scanTokens() function
    def scanfile(self, lines) -> list[tuple[int, list[tuple[int, Token]]]]:
        # Generates a token table for the whole file
        token_table = []
        for idx,line in enumerate(lines):
            token_table.append((idx,self.scanTokens(line)))

        return token_table

    # Function to match characters
    def match_marker(self, line, idx, marker) -> int:
        ''' Returns a new index by skipping over the matched marker
            else returns the same index '''
        if marker is None:
            return idx

        line_length = len(line)
        marker_length = len(marker)
        
        # Index out of bounds check
        if idx + (marker_length - 1) >= line_length: # subtract 1 to convert size to index
            return idx
        else: # If marker didn't match
            for i in range(0, marker_length):
                if line[idx + i] != marker[i]:
                    return idx
        
        return idx + marker_length

    # Function 
    def scanTokens(self, line):
        idx = 0
        tokens = []
        single_comm_found = False # Flag for breaking out of the loop

        # Scan for an empty line
        if self.is_empty_line(line):
            tokens.append((0, Token.EMPTY_LINE))
        # Else look for other characters
        else:
            while idx < len(line):
                token_found = False
                for token, marker in self.comment_markers.items():

                    new_idx = self.match_marker(line, idx, marker) # generates a new index after skipping chars
                    if idx != new_idx:
                        if self.state == Event.State.DEFAULT:
                            if token == Token.MULTI_LINE_COMM_START:
                                self.state = Event.State.IN_MULTI_LINE_COMM
                                tokens.append((idx, token))
                            elif token == Token.SINGLE_COMM:
                                tokens.append((idx, token))
                                single_comm_found = True
                            elif token == Token.STRING:
                                tokens.append((idx, token))
                                self.state = Event.State.IN_STRING

                        elif self.state == Event.State.IN_MULTI_LINE_COMM:
                            if token == Token.MULTI_LINE_COMM_END:
                                tokens.append((idx, token))
                                self.state = Event.State.DEFAULT

                        elif self.state == Event.State.IN_STRING:
                            if token == Token.STRING:
                                tokens.append((idx, token))
                                self.state = Event.State.DEFAULT

                        idx = new_idx # update to new index when tokens are matched 
                        token_found = True
                        break
                
                # We break out of the loop the moment we find a single line comment
                if single_comm_found:                
                    break
                if not token_found:
                    idx += 1 # increment loop if no token matched

        return tokens
