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

## 5/24/24 

AES Research:
Studied the AES algorithm and how it works, think we plan on doing the 256 key version.
Got the general idea of how the algorithm works, but since we are not using any built-in libraries, we will be creating our own map functions for the S-boxes and Rijndael MixColumns. We are also deciding whether we will need to be creating our own SHA key generators, or if we can use a library for that.


## Eric Lin

### 5/20/24

Brainstormed topic ideas

### 5/21/24

Brainstormed topic ideas (dot down by K again ._.)

### 5/22/24

Brainstormed topic ideas + looked into wifi cracking 

### 5/23/24

Decided on AES: 

https://www.youtube.com/watch?v=3MPkc-PFSRI
https://www.youtube.com/watch?v=4KiwoeDJFiA

### 5/24/24

AES Research:
Studied the AES algorithm and how it works, think we plan on doing the 256 key version. 
AES is a symmetric key algorithm, meaning the same key is used for both encryption and decryption. The steps are as follows:
1. Key Expansion
2. Initial Round 
3. Rounds (14 for 256 key)
4. Final Round
5. Decryption

Will have to pad the message to be a multiple of 128 bits, or split if it is too long.
Need to write our mapping functions for the S-boxes and Rijndael MixColumns. :\(


