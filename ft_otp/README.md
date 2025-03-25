# OTP Generator

This project is a one-time password (OTP) generator based on the TOTP (Time-Based One-Time Password) algorithm. It allows generating secret keys, encrypting them, and producing valid OTP tokens. It also includes QR code generation to facilitate integration with OTP applications.

---

## Usage

### Display Help

To display help and available options, run:

```bash
python ft_otp.py -h
```

---

### Generate an OTP Secret Key

To generate an OTP secret key and encrypt it, use the `-g` or `--generate` option followed by the path to a text file containing the raw secret key:

```bash
python ft_otp.py -g key.txt
```

**Example:**  
If the file `key.txt` contains the raw key `mysecretkey1234567890`, the program will encrypt this key and save it in a file named `key.hex`.

---

### Generate OTP Tokens

To generate OTP tokens from an encrypted secret key, use the `-k` or `--key` option followed by the path to the `.hex` file containing the encrypted key:

```bash
python ft_otp.py -k key.hex
```

**Example:**  
If the file `key.hex` contains a valid key, the program will generate a list of valid OTP tokens for the current period and display a QR code for one of the tokens.

---

### Interrupt the Program

You can interrupt the program at any time by pressing `Ctrl+C`.

---

## Example Output

### Generating a Secret Key

```bash
$ python ft_otp.py -g secret.txt
Encrypting the secret key
Secret key saved to key.hex
```

### Generating OTP Tokens

```bash
$ python ft_otp.py -k key.hex
Generating the OTP tokens
Valid tokens: ['123456', '654321', '789012', '345678', '901234']
QR code generated for token: 789012
```

A QR code will be displayed in a graphical window.

---

## Warnings

- Ensure that the input files meet the expected formats:
  - `.txt` for raw keys.
  - `.hex` for encrypted keys.
- Secret keys must have a **minimum length of 64 characters** and be a **multiple of 4**.

---

## Comparison with `oathtool`

You can compare the generated tokens with the `oathtool` utility:

```bash
oathtool --base32 --totp $(cat key.hex)
```

---

## Running with Docker

```bash
docker compose up --build
docker exec -it otp bash
```

---
