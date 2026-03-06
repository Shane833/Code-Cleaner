from CodeCleaner.events import Event, Token
from enum import Enum

class Parser(object):

    class State(Enum):
        DEFAULT = 1
        IN_STRING = 2
        IN_MULTI_LINE_COMM = 3
 
    def __init__(self,lines): # Will take a file obj to parse through
        self.lines = lines
        self.event_table = None
        self.event = Event()
        self.state = Parser.State.DEFAULT
        self.multi_line_comm_start = None
        self.multi_line_comm_end = None

    def __generate_events(self):
        self.event_table = self.event.scanfile(self.lines)

    def clean_file(self) -> []:
        self.remove_comments()
        self.format()

        return self.lines

    def remove_comments(self):
        # First pass to remove comments
        self.__generate_events()
        for line_no, event in self.event_table:
            if len(event) != 0: # Only enter if it contains any real comment data
                for idx, token in event:
                    if token == Token.SINGLE_COMM:
                        new_line = self.lines[line_no][:idx]
                        new_line = f"{new_line}\n"
                        self.lines[line_no] = new_line
                        #TODO: I'm not really making use of states, so do that
                    elif token == Token.MULTI_LINE_COMM_START:
                        self.state = Parser.State.IN_MULTI_LINE_COMM
                        self.multi_line_comm_start = (line_no, idx)
                    elif token == Token.MULTI_LINE_COMM_END:
                        self.multi_line_comm_end = (line_no, idx)
                        self.__service_multi_line_comm()
                        self.state = Parser.State.DEFAULT

    def format(self):
        # Second pass to remove unnecessary empty lines
        # TODO: Currently popping from the list will render the pre saved indexes useless
        self.__generate_events()
        previous_event = None
        no_of_deleted_lines = 0 # acts like an offset for correcting the index
        for line_no, event in self.event_table:
            if event == previous_event and len(event) != 0:
               self.lines.pop(line_no - no_of_deleted_lines) 
               no_of_deleted_lines += 1
            else:
                previous_event = event
 
             
    def __service_multi_line_comm(self):
        # iterate through the ranges from start to end
        start_line = self.multi_line_comm_start[0]
        end_line = self.multi_line_comm_end[0]
        start_idx = self.multi_line_comm_start[1]
        end_idx = self.multi_line_comm_end[1]
        
        #TODO: Get rid of as many constants/fixed no.s like the ' - 2' at the end
        # On the same line
        if start_line == end_line:
            self.__fill_line(start_line, start_idx, end_idx)
        else:
            self.__fill_line(start_line, start_idx, len(self.lines[start_line]) - 2) # 2 bcz don't want to get rid of the \n character at the end of the file
            self.__fill_line(end_line, 0, end_idx)
            for line_no in range(start_line + 1, end_line):
                self.__fill_line(line_no, 0, len(self.lines[line_no]) - 2)

        self.multi_line_comm_start = None
        self.multi_line_comm_end = None


    def __fill_line(self, line_no, start, end):
        line = list(self.lines[line_no])
        for i in range(start, end+1):
            line[i] = " "

        self.lines[line_no] = "".join(line)

        
    def print_lines(self):
        for line in self.lines:
            print(line, end="")
                        

                

        



