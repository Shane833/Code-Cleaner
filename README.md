# **CodeCleaner**
A simple CLI tool for removing comments from source code

## **Usage**
> **python ccleaner.py [options] [filename]:[start/end]**

### options
| Option |               Output                  |
|--------|---------------------------------------|
|   -i   | flags to make changes in the same file|


## **List of features**:
- [ ] Handle variable character single line comment
- [ ] Handle variable character multi line comment
- [ ] Create a finite state machine for handling extra options
- [x] Provide way to generate a new file or make changes in the same file
- [ ] Add multi-language support
- [ ] To take input along with file, the line no. start/range you would like to clean up
- [ ] Add regular expression for multiple files and recursion for a directory
- [ ] Add multithreading to simultaneously handle multiple files
- [ ] Add support for dumping the commments into a separate file
