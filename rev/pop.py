from curses.ascii import isprint
import os
import sys

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(0)
    try:
        with open(args[0], "r", encoding="latin-1") as f:
            file_content = f.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(0)
    except UnicodeDecodeError:
        print("Error decoding file")
        sys.exit(0)
    
    output_content = ''.join(char if isprint(char) or char == '\n' else '' for char in file_content)
    
    with open("output.txt", "w", encoding="latin-1") as f:
        f.write(output_content)
    
    print("Filtered content written to output.txt")

if __name__ == "__main__":
    main()