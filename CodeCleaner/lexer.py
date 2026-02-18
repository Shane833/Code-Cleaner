# We will be tokenizing the lines depending on what they contain
# We can have single line comment, multiline comment start, 
# multiline comment end, empty line

# Lexer will only work on lines provided in the function parameters

class Token(Enum):
	EMPTY_LINE = 1
	SINGLE_COMM = 2
	MULTI_COMM_START = 3
	MULTI_COMM_END = 4


