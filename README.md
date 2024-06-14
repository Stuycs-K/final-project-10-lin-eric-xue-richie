[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/ecp4su41)

[Video](https://drive.google.com/file/d/1VVpfFmSCAl2rlgPphm00e7oEeakGJgnP/view?usp=sharing)

# AES Encryption

This project implements AES (Advanced Encryption Standard) encryption in Python. The AES class provides functionality for encrypting plaintext using a specified 128-bit key. 

## Installation

1. Clone the repository or download the source code.
2. Ensure you have Python 3.x installed on your system.

## Key Files

- `aes.py`: Contains the AES class with encryption methods.
- `util.py`: Contains utility functions used in AES encryption.
- `encrypted.txt`: The output file where encrypted text will be saved.
- `test.py`: Contains test cases for the AES class. (not working after changes)

## Instructions

1. Place your plaintext file in the same directory as the script.
2. Run the script from the command line with the file name as an argument.
3. The encrypted text will be saved to `encrypted.txt`.

## Usage

### make encrypt

To encrypt a file, use the `encrypt` function provided in the script. 

You can run the script from the command line to encrypt a text file. 

```sh
make encrypt ARGS=<file_name>
```

Replace `<file_name>` with the name of the file you want to encrypt.

You can also encrypt with a custom key by passing the key as an argument.

```sh
make encrypt ARGS="<file_name> <key>"
```

### Example

```sh
make encrypt ARGS="plaintext.txt"
```

This command will read the contents of `plaintext.txt`, encrypt it using AES, and save the encrypted text to `encrypted.txt`.
