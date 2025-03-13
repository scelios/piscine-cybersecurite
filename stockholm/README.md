# Stockholm

Stockholm is a Python script that encrypts all files in the `/home/infection` directory using a key and adds the `.ft` extension to the encrypted files. It can also decrypt the files when needed.

## Usage

### Command Line Arguments

- `-v` or `-version`: Show the version of the script.
- `-r` or `-reverse`: Reverse the input (decrypt the files).
- `-s` or `-silent`: Silent mode (suppress output).

### How to Run

1. **Encrypt Files**:
    ```sh
    python stockholm.py
    ```

2. **Decrypt Files**:
    ```sh
    python stockholm.py -r
    ```
### How It Works

## Key Generation:
The script generates a key using base64 and saves it to key.txt if it doesn't already exist.
If key.txt exists, it reads the key from the file.

## File Encryption / Decryption:
The script encrypts all files in the /home/infection directory using the generated key and adds the .ft extension to the encrypted files.
It uses openssl for encryption / decryption with the aes-256-cbc algorithm.


## File Filtering:
The script reads a list of file extensions from wannacry_file_extensions.txt and removes files with extensions not in the list before encryption.
