# Reverse Engineering Project

The purpose of this project is to reverse engineer the `level[1-3]` binaries and extract the associated passwords.

## Tools Used

To achieve this, **IDA** (Interactive Disassembler) was used to analyze the binaries and understand their behavior.

## Project Structure

The project is organized as follows:

```
rev/
├── README.md          # This file
├── level1/            # Files related to level 1
│   ├── level1         # Binary to reverse engineer
│   ├── password       # Extracted password for level 1
│   ├── patch          # Patched binary (if applicable)
│   ├── patch.c        # Source code for the patch
│   └── source.c       # Decompiled or reverse-engineered source code
├── level2/            # Files related to level 2
│   ├── level2         # Binary to reverse engineer
│   ├── password       # Extracted password for level 2
│   ├── patch          # Patched binary (if applicable)
│   ├── patch.c        # Source code for the patch
│   └── source.c       # Decompiled or reverse-engineered source code
├── level3/            # Files related to level 3
│   ├── level3         # Binary to reverse engineer
│   ├── password       # Extracted password for level 3
│   ├── patch          # Patched binary (if applicable)
│   ├── patch.c        # Source code for the patch
│   └── source.c       # Decompiled or reverse-engineered source code
```

## How to Use

1. **Analyze the binaries**: Use IDA or any other reverse engineering tool to disassemble and analyze the binaries located in the `level1/`, `level2/`, and `level3/` directories.
2. **Extract passwords**: The extracted passwords are stored in the `password` files within each level's directory.
3. **Review reverse-engineered code**: The reverse-engineered or decompiled source code is available in the `source.c` files for each level.
4. **Apply patches (if needed)**: If a patch was applied to bypass certain protections, the patched binary and its source code are available in the `patch` and `patch.c` files, respectively.

## Notes

- The passwords for each level are stored in plain text in the `password` files.
- The `source.c` files contain the reverse-engineered logic of the binaries for better understanding.

## License

This project is for educational purposes only. Use responsibly.