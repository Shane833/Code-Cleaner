from lexer import *

# I want to create a token table next which will contain
# entries in the form (TOKEN_TYPE, line_no, start_index)

class Parser(object):
	def __init__(self,lines): # Will take a file obj to parse through
		# We will store the file obj
		self.lines = lines
		# we can modify this token map to work with other languages
		self.token_map = {TOKEN.SINGLE_COMM : '//',
						  TOKEN.MULTI_LINE_COMM_START : '/*',
						  TOEKN.MULTI_LINE_COMM_END : '*/'}
		self.token_table = [] # list containing info about the comment type, line no, index
							  # This is the token table that gets returned to the cleaner

	def tokenize(self):
	'''Go through each of the line and then tokenize only the comments
	   and the redundant new lines'''
		for i in range(0, len(self.lines)):
			# If its en empty line then move ahead
			if is_empty_line(self.lines[i]):
				self.token_table.append((TOKEN.EMPTY_LINE, i, 0))
			else:
				# Now to look for comments
				index = -1
				# Not going to make an if-elif-else ladder because there can be multiple
				# comment types on a single line and I don't want to miss them
				if (index = has_multi_line_comm_start())

