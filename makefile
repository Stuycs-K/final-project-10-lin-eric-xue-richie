usage: 
	@echo "Usage: make all"
	@echo "       make clean"
	@echo "       make test"
encrypt: # the cmd to encrypt the file
	# delete the old file
	@rm -f encrypted.txt
	@python3 aes.py encrypt $(ARGS)
