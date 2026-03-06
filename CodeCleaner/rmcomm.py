from CodeCleaner.parser import Parser
import sys

def main():
    file_path = sys.argv[1]
    with open(file_path, "r+") as file:
        parser = Parser(file.readlines())
        new_lines = parser.clean_file()
        file.seek(0)
        file.truncate()
        file.writelines(new_lines)
        file.flush()
        file.close()

    print(sys.argv)

if __name__ == "__main__":
    main()
