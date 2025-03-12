import sys
import base64 # To convert the secret into the 20 random bytes
import hmac # Provides the HMAC algorithm
import hashlib # Provides the SHA1 algorithm
import time
from math import floor
import qrcode
from PIL import Image, ImageTk
from tkinter import Tk, Label
import os


TOKEN_LENGTH = 6 
VALIDITY_DURATION = 30
VALID_START = -2 # Allow 2 time steps in the past to be considered valid
VALID_END = 2 # Allow 2 time steps in the future to be considered valid

def save_and_encrypt_secret_key(secret: str):
    """Encrypts and saves the secret key to a file."""
    key = base64.b32encode(secret.encode())
    if (len(key) < 64 or len(key) % 4 != 0):
        print("Please provide a secret key of at least 64 characters and a multiple of 4")
        sys.exit(1)
    # save the key to a file
    with open(f"key.hex", "wb") as file:
        file.write(key)

def generate_counter_value ():
    """Generates the counter value for the TOTP algorithm's hash generator."""
    timestamp = time.time() # Gets current time as a float (= with microseconds)
    timestamp = floor(timestamp) # Turn it into an integer (= only seconds)
    # Doing the following ensures that the value increments by one every 30
    # seconds
    counter_value = floor(timestamp / VALIDITY_DURATION)
    return counter_value

def generate_hash (K: str, C: int):
    """Generates a TOTP compatible HMAC hash based on the shared secret (K) and
    the current time window/counter value C."""
    key_bytes = base64.b32decode(K)
    counter_bytes = C.to_bytes(8, byteorder = 'big')
    hash = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)
    return hash


def truncate_dynamically (hash: bytes):
    """Truncates a generated HMAC hash and returns it as an integer"""
    offset = hash[-1] & 0x0F
    truncated = hash[offset:offset + 4]
    code_number = int.from_bytes(truncated, byteorder = 'big')
    return code_number & 0x7FFFFFFF


def truncated_hash_to_token (code: int, digits: int = TOKEN_LENGTH):
    """Takes a truncated HMAC code number and returns the modulo of that to
    return the requested number of digits"""
    code = code % 10 ** digits
    code = str(code)
    if len(code) < digits:
        code = code.rjust(digits, "0")
    return code

def generate_totp_tokens (key: str, 
                          timestep_start = VALID_START,
                          timestep_end = VALID_END):
    """Generates a list of valid tokens within the valid window provided."""
    tokens: list[str] = []
    counter_value = generate_counter_value()

    for timestep in range(timestep_start, timestep_end + 1):
        hm = generate_hash(key, counter_value + timestep)
        code = truncate_dynamically(hm)
        valid_token = truncated_hash_to_token(code)
        tokens.append(valid_token)

    return tokens

def generate_qr_code(data: str):
    """Generates a QR code from the provided data and saves it to a file."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    return img
    

def display_qr_code(img):
    """Displays the QR code image in a Tkinter window."""
    root = Tk()
    root.title("QR Code")
    img = ImageTk.PhotoImage(img)
    label = Label(root, image=img)
    label.pack()
    root.mainloop()

def check_file(file, types):
    """Check if the file exists and is of the specified type and length"""
    if not file.endswith(types):
        print(f"Error: File {file} not supported")
        return False
    if not os.path.exists(file):
        print(f"Error: File {file} not found")
        return False
    if len(open(file).read()) < 64 and types == ".hex":
        print(f"Error: File {file} is not a valid key")
        return False
    return True

def generate_counter_value():
    """Generates the counter value for the HMAC algorithm."""
    return floor(time.time() / VALIDITY_DURATION)

def generate_hash(key: str, counter: int):
    """Generates the HMAC hash for the provided key and counter."""
    key = base64.b32decode(key)
    counter = counter.to_bytes(8, byteorder="big")
    hash = hmac.new(key, counter, hashlib.sha1).digest()
    return hash

def truncate_dynamically(hash: bytes):
    """Truncates the hash to the desired length."""
    offset = hash[-1] & 0xf
    truncated_hash = hash[offset:offset+4]
    return truncated_hash

def truncated_hash_to_token(truncated_hash: bytes):
    """Converts the truncated hash to a token."""
    code = int.from_bytes(truncated_hash, byteorder="big") & 0x7fffffff
    return str(code % 10 ** TOKEN_LENGTH).rjust(TOKEN_LENGTH, "0")

def generate_totp_tokens (key: str, 
                          timestep_start = VALID_START,
                          timestep_end = VALID_END):
    """Generates a list of valid tokens within the valid window provided."""
    tokens : list[str] = []
    counter_value = generate_counter_value()
    for timestep in range(timestep_start, timestep_end + 1):
        hash = generate_hash(key, counter_value + timestep)
        code = truncate_dynamically(hash)
        valid_token = truncated_hash_to_token(code)
        tokens.append(valid_token)

    return tokens

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = ["-h"]
    if args[0] == "-h":
        print("Usage: python scorpion.py [-h] [-g] [-k] ")
        print("Options:")
        print("-h, --help: Show this help message and exit")
        print("-g, --generate: Generate a new OTP secret key")
        print("-k, --key: Provide a secret key to generate OTP tokens")
        sys.exit(0)
    if len(args) != 2:
        print("Error: Invalid number of arguments")
        sys.exit(1)

    
    if args[0] == "-g" or args[0] == "--generate":
        if check_file(args[1], ".txt") is False:
            sys.exit(1)
        print("Encrypting the secret key")
        secret = open(args[1]).read()
        save_and_encrypt_secret_key(secret)
        print(f"Secret key saved to key.hex")

    elif args[0] == "-k" or args[0] == "--key":
        if check_file(args[1], ".hex") is False:
            sys.exit(1)
        print("Generating the OTP tokens")
        hex = open(args[1]).read()
        valid_tokens = generate_totp_tokens(hex)
        print(f"Valid tokens: {valid_tokens}")
        if valid_tokens:
            token = valid_tokens[2]
            print(f"QR code generated for token: {token}")
            img = generate_qr_code(token)
            display_qr_code(img)
        # secret = base64.b64decode(hex)
        # print(f"Secret key: {secret}")
        # valid_tokens = generate_totp_tokens(secret)
        