# Simple script to clean up the code by removing comments

# Open the file traverse throught it
# if encounter '//' then remove everything until you encounter a new line or EOF

import sys

# TODO 1 : format it a bit better ✅
# Alright so I want such that if it has only a new line char and no data
# followed by the same things then the second line should be removed
# So I would have to identify if the given line contains only a new line
# or does it really contain any actual data
# PROBLEM : The last line is not getting formatted right missing bracket (FIXED)


# TODO 2 : To handle multi-line strings 👈
# TODO 3 : To be able to be able to perform the changes in the same file or just generate a new single file
# TODO 4 : To be able to identify the language of the file from its extension
# TODO 5 : To take input along with file, the line no. start/range you would like to clean up

def is_empty_line(line) -> bool:
	# go through the line and determines if its just for formatting
	characters = ['\n',' ','\t']
	for l in line:
		if l not in characters:
			return False
		else:
			pass
	return True


def format_code(file):
	with open(file, mode="r+") as new_file,  open("temp2.c", mode="w+") as temp_file:
		# storing the list of lines
		lines = new_file.readlines()
		
		i = 0
		while i < len(lines):
			if is_empty_line(lines[i]):
				#print(lines[i],end="")
				temp_file.write(lines[i])
				temp_file.flush()

				offset = 0
				while is_empty_line(lines[i+offset]):
					offset += 1

				i = i + offset
			else:
				#print(lines[i],end="")
				temp_file.write(lines[i])
				temp_file.flush()
				i += 1

			#if line != '\n':
			#print(line,end="")
			#print("empty? : ", is_empty_line(line))

		new_file.close()
		temp_file.close()
		
	


def remove_comments(file):
	with open("temp.c",mode="w+") as new_file:
		line_no = 0 # to help jump over lines in case of multi-line comments
		for line in file.readlines():
			# Now to parse through the line
			new_line = line
			
			# Handling single line comments
			i = line.find('//')
			if i != -1:
				new_line = line[:i]
				new_line = f"{new_line}\n"# explicitely append a new line characterat the end
			else:
				# Handling multi line comments
				# There will be two cases: 1. ends on the same line 2. ends on a different line
				# 1. If ends on the same line then I can just slice from its beginning to the end
				# 2. If ends on a different line then would need to keep track of all the lines
				# removes all the lines until they are removed
				i = line.find('/*')
				if i != -1:
					print(f"FOUND A MULTILINE COMMENT",)
					print(line,end="")
			
			new_file.write(new_line)
			new_file.flush()

		new_file.close()
		format_code("temp.c")	

		
if __name__ == "__main__":
	if len(sys.argv) > 1:
		with open(sys.argv[1],mode='r+') as file:
			remove_comments(file)
			file.close()

	else:
		print("ERROR : Usage python cleaner.py [File(s) path]")
