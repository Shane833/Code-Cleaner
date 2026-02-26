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

# Utility function for identifying the various tokens

# Making a class for differnt types of languages
def is_empty_line(line) -> bool:
	'''go through the line and determines if its just for formatting'''
	characters = ['\n',' ','\t']
	for l in line:
		if l not in characters:
			return False
		else:
			pass
	return True

# Providing an additional argument in identifying the comment characters
# so that the same function can be used for different language comments
def has_single_comm(line, single_comm_str) -> int:
	'''if the single line comment is found then simply
	   return the index within the line else returns -1'''

	index = line.find(single_comm_str)
	return index

def has_multi_line_comm_start(line, multi_comm_start_str) -> int:
	''' If contains /* simply return the index else -1 '''
	index = line.find(multi_comm_start_str)
	return index

def has_multi_line_comm_end(line, multi_comm_end_str) -> int:
	''' If contains */ simply return the index else -1'''
	index = line.find(multi_comm_end_str)
	return index




