from util import *
import os

class AES:
    text: str
    blocks: list    
    def __init__(self, text: str):
        self.key = "2B28AB097EAEF7CF15D2154F1646883C"
        self.text  = text 

    def gen_256_key(self) -> str:
        return os.urandom(32).hex()

    def split_text(self) -> list:
        blocks: list = []
        for i in range(0, len(self.text), 4):
            if len(self.text[i: i+4]) < 4:
                blocks.append(self.text[i: i+4].ljust(4, " "))
            else:
                blocks.append(self.text[i: i+4])        
        return blocks
    
    def sub_bytes(self, state: str) -> str:
        bytes_list = to_byte_array(state)
        subbed_bytes_list = [hex_format(s_box[int(byte, 16)]).lstrip("0x") for byte in bytes_list]
        return subbed_bytes_list
    
    def shift_rows(self, state: str) -> str:
        bytes_list = to_byte_array(state)
        # do nothing to first 4 bytes
        # shift 2nd row by 1
        if bytes_list[4] != "00":
            bytes_list[4], bytes_list[5] = bytes_list[5], bytes_list[4]
            bytes_list[5], bytes_list[6] = bytes_list[6], bytes_list[5]
            bytes_list[6], bytes_list[7] = bytes_list[7], bytes_list[6]
        # shift 3rd row by 2
        if bytes_list[8] != "00":
            bytes_list[8], bytes_list[10] = bytes_list[10], bytes_list[8]
            bytes_list[9], bytes_list[11] = bytes_list[11], bytes_list[9]
        # shift 4th row by 3
        if bytes_list[12] != "00":
            bytes_list[12], bytes_list[13] = bytes_list[13], bytes_list[12]
            bytes_list[12], bytes_list[14] = bytes_list[14], bytes_list[12]
            bytes_list[12], bytes_list[15] = bytes_list[15], bytes_list[12]
        return bytes_list
    
    def gmul(self, a: int, b: int) -> int:
        result = 0
        for _ in range(8):
            if b & 1:  # If the least significant bit of b is set
                result ^= a  # Add a to the result
            high_bit_set = a & 0x80  # Check if the highest bit of a is set
            a <<= 1  
            if high_bit_set:  # If the highest bit of a was set
                a ^= 0x1B  # Apply the XOR with 0x1B (the irreducible polynomial for AES)
            b >>= 1  
        return result & 0xFF  

    def mix_columns(self, state: str) -> str:
        bytes_list = to_byte_array(state)
        for i in range(0, 4):
            a = int(bytes_list[i], 16)
            b = int(bytes_list[i+4], 16)
            c = int(bytes_list[i+8], 16)
            d = int(bytes_list[i+12], 16)
            bytes_list[i]   = hex_format(self.gmul(a, 0x02) ^ self.gmul(b, 0x03) ^ self.gmul(c, 0x01) ^ self.gmul(d, 0x01))
            bytes_list[i+4] = hex_format(self.gmul(a, 0x01) ^ self.gmul(b, 0x02) ^ self.gmul(c, 0x03) ^ self.gmul(d, 0x01))
            bytes_list[i+8] = hex_format(self.gmul(a, 0x01) ^ self.gmul(b, 0x01) ^ self.gmul(c, 0x02) ^ self.gmul(d, 0x03))
            bytes_list[i+12]= hex_format(self.gmul(a, 0x03) ^ self.gmul(b, 0x01) ^ self.gmul(c, 0x01) ^ self.gmul(d, 0x02))
        return bytes_list
    
    def add_round_key(self, state: str, round_key: str) -> str:
        bytes_list = to_byte_array(state)
        round_key_list = to_byte_array(round_key)

        for i in range(0, 16):
            bytes_list[i] = format(int(bytes_list[i], 16) ^ int(round_key_list[i], 16), "02x")
        return bytes_list
    

    def keyExpansion(self):
        wordlist = []
        initWords(self.key, wordlist)
        print(f"Initial Words: {wordlist}")
        counter = 8
        while(len(wordlist) < 60):
            word = wordlist[counter - 1]
            print(f"Counter: {counter}, Word: {word}")

            if(counter % 8 == 0):
                rotated = rotWord(word)
                subbed = self.sub_bytes(rotated)
                word = xor_first_byte(subbed, (counter // 8) - 1)
                print(f"RotWord: {rotated}, SubBytes: {subbed}, Rcon XOR: {word}")
            elif(counter % 4 == 0):
                word = self.sub_bytes(word)
                print(f"SubBytes: {word}")
            
            newword = [hex_format(int(wordlist[counter - 8][i], 16) ^ int(word[i], 16)) for i in range(8)]
            wordlist.append(newword)
            counter += 1
            print(f"New Wordlist: {wordlist[-4:]}")
        return wordlist


# append the initial key to the word list (8 bytes long):
def initWords(key, wordlist):
    print(f"key: {key}")
    for i in range(0, 8):
        wordlist.append(key[i * 4: (i + 1) * 4])

# # everything here is to generate the key:
def rotWord(word):
    return [word[1], word[2], word[3], word[0]]
# # subsitute bytes (richie got it )
# def sub_bytes(word):
#     return [s_box[b] for b in word]
# #rcon
def xor_first_byte(word, counter):
    # print(f"len word: {len(word)}")
    # print(f"first word: {int(word[0], 16)}")
    # print(f"rcon counter: {rcon[counter]}")
    print(word)
    return [int(word[0], 16) ^ rcon[counter], int(word[1], 16), int(word[2], 16), int(word[3], 16)]
    # return [hex(word[0]) ^ rcon[counter], hex(word[1]), hex(word[2]), hex(word[3])]


key = [0x2B, 0x28, 0xAB, 0x09, 0x7E, 0xAE, 0xF7, 0xCF, 0x15, 0xD2, 0x15, 0x4F, 0x16, 0x46, 0x88, 0x3C, 0x2B, 0x28, 0xAB, 0x09, 0x7E, 0xAE, 0xF7, 0xCF, 0x15, 0xD2, 0x15, 0x4F, 0x16, 0x46, 0x88, 0x3C]

test = AES("")
# print(test.gen_256_key())
print(test.keyExpansion())

# print(wordlist)
# keyExpansion(key)
# print(wordlist)







