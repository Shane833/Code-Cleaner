# **CodeCleaner**
A simple CLI tool for removing comments from source code

## **Usage**
> **python ccleaner.py [options] [filepath(s)]**

### options
| Option |               Output                  |
|--------|---------------------------------------|
|    -   | Default : Generates a new file by appending '_cleaned' to the file|
|   -i   | flags to make changes in the same file|


### Supported Languages
- C
- C++
- Java
- JavaScript
- HTML
- CSS
- Python

## **List of features**:
- [x] Handle variable character single line comment
- [x] Handle variable character multi line comment
- [x] Provide way to generate a new file or make changes in the same file
- [ ] Provide options for inidividual files
- [x] Add multi-language support
- [ ] To take input along with file, the line no. start/range you would like to clean up
- [ ] Add regular expression for multiple files and recursion for a directory
- [ ] Add multithreading to simultaneously handle multiple files
- [ ] Add support for dumping the commments into a separate file
