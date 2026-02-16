# Simple script to clean up the code by removing comments

# Open the file traverse throught it
# if encounter '//' then remove everything until you encounter a new line or EOF

import sys

def format_code(file):
	with open(file, mode="r+") as new_file:
		for line in new_file.readlines():
			if line != '\n':
				print(line,end="")
		new_file.close()

def remove_comments(file):
	with open("temp.c",mode="w+") as new_file:
		for line in file.readlines():
			# Now to parse through the line
			new_line = line
			
			i = line.find('//')
			if i != -1:
				new_line = line[:i]
				new_line = f"{new_line}\n"# explicitely append a new line characterat the end
			
			#print("Modified : ",new_line,end="")
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
