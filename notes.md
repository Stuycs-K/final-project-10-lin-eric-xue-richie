What is AES?

Resouces: 
https://www.youtube.com/watch?v=O4xNJsjtN6E
https://www.youtube.com/watch?v=NHuibtoL_qk

https://legacy.cryptool.org/en/cto/aes-animation
https://www.kavaliro.com/wp-content/uploads/2014/03/AES.pdf

Iterative Process: 
1) SubBytes
2) ShiftRows
3) MixColumns
4) AddRoundKey

note: the last iteration skips mixcolumns

1) SubBytes: using the S-Box, each element in the 4x4 array is replaced with its corresponding counterpart. 
2) ShiftRows: For each row, the number of bytes moved to the end of the row is determined by the row number. For example, the first row none of the bytes are moved, the second row the first byte is moved, the third row three bytes are moved, etc. 
3) MixColumns: The columns are multipled by some invertible matrix (?) one column at a time

Galois Field with 2^8 elements (finite field with order 256). 
- finite fields are algebraic structures with a finite number of elements that you can perform addition, subtraction, multiplication, and division in a way that satisfies the field axoims.

It's constructed using a polnomial represtation over the base field GF(2), which consist of two elements: 0 and 1. GF(2^8) use a polynomial of degree 8 over GF(2) (?). The polynomial defines the field GF(256)

The elements of GF(2^8) can be represented as polynomials of degree less than 8 with coefficents in GF(2). For example: a_7x^7 + a_6x^6 + ... + a_x + _0, where a_i is either 0 or 1. Each polynomial correspondes to an 8 bit binary, giving us 256 unique elements. 

Operations: 
1. Addition/subtraction: done with bitwise oeprations (XOR)
  (a + b)(x) = a(x) xor b(x)
2. Multiplication: polynomal multiplication with a reduction modulo P(x) (?)
3. Division: multiplying the dividen by the multiplicative inverse of the divisor in GF(2^8)

Clarifications: 
GF(2) is the simplies finite field, consisting of only two elements:0 and 1. 

Addition and subtraction (XOR operations):
0 + 0 = 0, 0 + 1 = 1, 1 + 0 = 1, 1 + 1 = 0

Multiplication: 
0 * 0 = 0, 0 * 1 = 0,  1 * 0 = 0, 1 * 1 = 1

An irreducible polynomial over GF(2) is a polynomial that cannot be factored into the product of two non-constant polynomials over GF(2). in other words it has no divisors other than itself and the constant polynomial 1. This polynomial serves as the modulus, ensuring every non-zero element has a multiplicative inverse. 
- common polynomial : x^8 + x^4 + x^3 + x + 1

Multiplicative Inverse: a(x) * b(x) = 1 mod P(x)
- use the extended Euclidean Algorithm: 
    1) apply the algorithm to a(x) and the irreducible polynomial P(x) to express 1 as a linear combination of a(x) and P(x)

     1 = a(x) * u(x) + P(x) * v(x)

     u(x) is the multiplicative inverse of a(x)
    EX: a(x) = x^3 + x + 1, P(x) = x^8 + x^4 + x^3 + x + 1

        a(x) * u(x) = 1 mod P(x)


Polynomial multiplication: 
(x^3 + x + 1)(x^2 + x) = x^5 + 2x^4 + x^3 + x^2 + x
since 2x^4 is in GF(2) it simplifies to zero. Since GF(256) uses G(2) for each coefficent, we use GF(2). 
It also ensures that all coefficents are within the set {0, 1}

x^5 + x^3 + x^2 + x
We don't need to reduce in this case. 



4) AddRoundKey: A round key is applied by a bitwise XOR. This round key was created by expanding the key before the encryption/decryption process and has the same length as a block


How to get the round key: 

The first set of round key is the original key

Word generation: 4 bytes (32 words for 256)

1) Take the previous round key
2) apply rotword (rotate all bytes by 1 to the left)
3) xor the first byte with the round constant (figure out what that is)
4) generate the n*the key gives us the first 8 words
we need (14 + 1)* 4  = 60 words
if W[4i] =  W[4 (i-1)] xor modified result
   W[4i + 1] = W[4i] xor W[4(i-1) + 1]
   W[4i + 2] = W[4i] xor W[4(i-1) + 2]
   W[4i + 1] = W[4i] xor W[4(i-1) + 3]
continue until all round keys are generated


For each new word index: 
  if i is a multiple of 8 
    rotate previous word
    apply subbytes
    xor the first byte with the rcon value
  if i is a mutple of 4
    subbytes
  else
    xor with 8 words earlier 