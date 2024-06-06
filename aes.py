


from util import *
import os

class AES:
    text: str
    blocks: list    
    def __init__(self, text: str):
        self.key = "2b28ab097eaef7cf15d2154f16a6883c"
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
        subbed_bytes_list = [hex(s_box[int(byte, 16)]).lstrip("0x") for byte in bytes_list]
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
    
    def mix_columns(self, state: str) -> str:
        bytes_list = to_byte_array(state)

        for i in range(0, 4):
            # get the 4 bytes in the column
            a = int(bytes_list[i], 16) 
            b = int(bytes_list[i+4], 16)
            c = int(bytes_list[i+8], 16)
            d = int(bytes_list[i+12], 16)
        
            #apply the fixed_col matrix to the column
            bytes_list[i]   = format(gmul(a, 0x02) ^ gmul(b, 0x03) ^ gmul(c, 0x01) ^ gmul(d, 0x01), "02x")
            bytes_list[i+4] = format(gmul(a, 0x01) ^ gmul(b, 0x02) ^ gmul(c, 0x03) ^ gmul(d, 0x01), "02x")
            bytes_list[i+8] = format(gmul(a, 0x01) ^ gmul(b, 0x01) ^ gmul(c, 0x02) ^ gmul(d, 0x03), "02x")
            bytes_list[i+12]= format(gmul(a, 0x03) ^ gmul(b, 0x01) ^ gmul(c, 0x01) ^ gmul(d, 0x02), "02x")

        return bytes_list
    
    def add_round_key(self, state: str, round_key: str) -> str:
        bytes_list = to_byte_array(state)
        round_key_list = to_byte_array(round_key)

        for i in range(0, 16):
            bytes_list[i] = format(int(bytes_list[i], 16) ^ int(round_key_list[i], 16), "02x")
        return bytes_list
    
    def rot_word(self, state: str) -> str:
        state = to_byte_array(state)
        return state[1] + state[2] + state[3] + state[0]
    
    def rcon_xor(self, state: str, first_col: str, rcon: int) -> str:
        state = to_byte_array(state)
        first_col = to_byte_array(first_col)
        #xor temp with first column and rcon
        state = [format(int(first_col[j], 16) ^ int(state[j], 16), "02x") for j in range(4)]
        state = [format(int(state[j], 16) ^ rcon, "02x") for j in range(4)]
        return state
    
    def xor(self, state: str, col: str) -> str:
        state = to_byte_array(state)
        col = to_byte_array(col)
        return [format(int(state[i], 16) ^ int(col[i], 16), "02x") for i in range(4)]
    
    def key_expansion(self) -> list:
        key = to_byte_array(self.key)
        expanded_key = key[:]
        print(expanded_key)
        for i in range(8, 60):
            temp = expanded_key[i - 5] + expanded_key[i - 1] + expanded_key[i + 3] + expanded_key[i + 7]
            print("last_col", temp)
            if i % 8 == 0:
                temp = self.rot_word(temp)
                print("post rot word:", temp)
                temp = self.sub_bytes(temp)
                print("post sub byte", temp)
                first_col = expanded_key[i - 8] + expanded_key[i - 4] + expanded_key[i] + expanded_key[i + 4]
                print(first_col)
                #xor temp with first column and rcon
                temp = to_byte_array(self.rcon_xor(temp, first_col, rcon[i // 10]))
                print("post rcon xor", temp)
                expanded_key += temp
                print(expanded_key)
            elif i % 8 == 4:
                temp = self.sub_word(temp)
            # expanded_key += [format(int(expanded_key[-32 + j], 16) ^ int(temp[j], 16), "02x") for j in range(4)]

        return expanded_key 
    

# wordlist = []

# def initWords(key):
#     for i in range(0, 32, 8):
#         wordlist.append([key[i], key[i+1], key[i+2], key[i+3]])
#     return wordlist

# # everything here is to generate the key:
# def rotWord(word):
#     return [word[1], word[2], word[3], word[0]]
# # subsitute bytes (richie got it )
# def sub_bytes(word):
#     return [s_box(b) for b in word]
# #rcon
# def xor_first_byte(word, counter):
#     return [word[0] ^ rcon[counter], word[1], word[2], word[3]]

# def keyExpansion(key):
#     initWords(key)
    
#     counter = 8
#     # 14 rounds + 1 inital = 15 set, each with 4 bytes
#     while(len(wordlist) < 60):
#         word = wordlist[counter -1]

#         if(counter % 8 == 0):
#             # make sure rcon uses the correct counter
#             word = xor_first_byte(sub_bytes(rotWord(word)), (counter // 8) - 1)
#         elif(counter % 4 == 0):
#             word = sub_bytes(word)
        
#         # xor with 8 words ago
#         newwords = [wordlist[counter - 8][i] for i in range(4)]
#         wordlist.append(newwords)

#         counter += 1
#     return wordlist
    
# keyExpansion("2b28ab097eaef7cf15d2154f16a6883c")
# print(wordlist)
    
example = "Lorem Ipsum is s"
aes = AES(example)
print(aes.key_expansion())








    

example = "Lorem Ipsum is s"
aes = AES(example)
print(to_byte_array(aes.key))
print(aes.key_expansion())




