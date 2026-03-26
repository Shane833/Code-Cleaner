from enum import Enum

class Token(Enum):
    EMPTY_LINE = 1
    SINGLE_COMM = 2
    MULTI_LINE_COMM_START = 3
    MULTI_LINE_COMM_END = 4 
    STRING = 5 # making string have a single token 

class Event(object):
    # States the finite machine can have
    class State(Enum):
        DEFAULT = 1
        IN_STRING = 2
        IN_MULTI_LINE_COMM = 3
        
    def __init__(self,single_comm_marker,multi_line_comm_start_marker, 
                 multi_line_comm_end_marker, string_marker):
        self.state = Event.State.DEFAULT # used to monitor when inside string we ignore scanning
        self.comment_markers = {Token.SINGLE_COMM : single_comm_marker,
                                Token.MULTI_LINE_COMM_START : multi_line_comm_start_marker,
                                Token.MULTI_LINE_COMM_END : multi_line_comm_end_marker,
                                Token.STRING : string_marker}

    def is_empty_line(self,line) -> bool:
        '''go through the line and determines if its just for formatting'''
        return line.strip() == "" # simple way, i.e. after removing all the whitespace if we are left with nothing then its an empty line
     
    # Modifying scanfile function to use scanTokens() function
    def scanfile(self, lines:list[str]) -> list[tuple[int, list[tuple[int, Token]]]]:
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
