# Work Log

## Richie Xue

### 5/20/24

Brainstormed topic ideas 

### 5/20/24

Brainstormed topic ideas (shot down by K)

### 5/21/24

Brainstormed topic ideas (shot down by K again ._.)

### 5/22/24

Brainstormed topic ideas + looked into AES

### 5/23/24

AES Research:
https://legacy.cryptool.org/en/cto/aes-animation

### 5/24/24 

AES Research:
Studied the AES algorithm and how it works, think we plan on doing the 256 key version.
Got the general idea of how the algorithm works, but since we are not using any built-in libraries, we will be creating our own map functions for the S-boxes and Rijndael MixColumns. We are also deciding whether we will need to be creating our own SHA key generators, or if we can use a library for that.

AES is a symmetric key algorithm, meaning the same key is used for both encryption and decryption. The steps are as follows:
1. Key Expansion
2. Initial Round 
3. Rounds (14 for 256 key)
4. Final Round
5. Decryption

Will have to pad the message to be a multiple of 128 bits, or split if it is too long.
Need to write our mapping functions for the S-boxes and Rijndael MixColumns. :\(

### 5/28/24
Write gen_256_key function to generate the 256 bit key and split_text and to_hex to prep for cleaning input text for multiple runs of AES encryption.

### 5/29/24
Wrote subbytes today, a substitution function that uses the S-box to replace each byte in the state with a new byte. 

### 5/30/24
Wrote shiftrows today, a function that shifts the rows of the state by a certain offset. Only works for 4x4 matrices, so we will have to have make sure the input is a multiple of 128 bits.

### 6/5/2024
WIP implementation of key_expandsion  in class

### 6/6/2024
Finished key expansion, and started on the add_round_key function.

### 6/7/2024
Finished add_round_key, so began writing the encrypt function itself.

### 6/9/2024
Finished encrypt function, makefile, aes128 is done. 

## Eric Lin

### 5/20/24

Brainstormed topic ideas

### 5/21/24

Brainstormed topic ideas (dot down by K again ._.)

### 5/22/24

Brainstormed topic ideas + looked into wifi cracking 

### 5/23/24

Decided on AES: 

### 5/24/24

Watched a video on AES and looked at the animation richie told me to look at + wikipedia research + started taking notes 
https://www.youtube.com/watch?v=3MPkc-PFSRI
https://www.youtube.com/watch?v=4KiwoeDJFiA

### 5/27/24

Learned and took (a lot) of notes on the iterative steps. Still need to learn how to generate round keys, but besides that I got everything else. 

### 5/28/24

https://www.geeksforgeeks.org/advanced-encryption-standard-aes/#

Took notes on round key generation (still a bit lost, what's a round constant?)

### 5/29/24

worked on keygen