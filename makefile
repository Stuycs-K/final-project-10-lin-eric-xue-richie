# Makefile
.PHONY: encrypt decrypt install

# Usage information
usage:
	@echo "Usage: make [command] ARGS=[args]"
	@echo "Commands:"
	@echo "  encrypt @ARGS= <file>: Encrypt the file"
# @echo "  decrypt @ARGS= <file> <key>: Decrypt the file with the key"

encrypt: # the cmd to encrypt the file
	@rm -f encrypted.txt
	@python3 aes.py encrypt $(ARGS)

# decrypt: # the cmd to decrypt the file
# 	@rm -f decrypted.txt
# 	@python3 aes.py decrypt $(ARGS)

# # Command to install requirements
# install:
# 	@pip install pycryptodome

# Default target
.DEFAULT_GOAL := usage
