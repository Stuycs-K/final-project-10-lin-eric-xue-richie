from util import *
import os
import sys 
class AES:
    text: str

    def __init__(self, text: str):
        self.key = "5468617473206D79204B756E67204675"
        #self.key = self.gen_128_key()
        self.text  = to_hex(text)

    def gen_128_key(self) -> str:
        return os.urandom(16).hex()

    def split_text(self) -> list:
        blocks = []
        formatted_text = self.text.replace(" ", "")
        for i in range(0, len(formatted_text), 32):
            blocks.append(to_byte_array(formatted_text[i:i+32]))
        return blocks
    
    def sub_bytes(self, state: str) -> str:
        bytes_list = to_byte_array(state)       
        subbed_bytes_list = [format(s_box[int(byte, 16)], "02x") for byte in bytes_list]
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
        
    def key_expansion(self) -> list:
        expanded_key = []
        key = to_byte_array(self.key)        
        for i in range(0, 4):
            expanded_key.append([key[i], key[i+4], key[i+8], key[i+12]])
        rcon_counter = 0
        for i in range(4, 44):
            temp = expanded_key[i - 1]
            if i % 4 == 0:
                temp = rot_word(temp)
                temp = self.sub_bytes(temp)
                temp = rcon_xor(temp, rcon[rcon_counter])
                rcon_counter += 1
            temp = [format(int(expanded_key[i - 4][j], 16) ^ int(temp[j], 16), "02x") for j in range(4)]
            expanded_key.append([temp[j] for j in range(4)])
        
        # format the expanded key into their round keys
        keys = []
        for i in range(0, 44, 4):
            temp_key = expanded_key[i] + expanded_key[i+1] + expanded_key[i+2] + expanded_key[i+3]
            for j in range(4):
                temp_key[j] = expanded_key[i][j] + expanded_key[i+1][j] + expanded_key[i+2][j] + expanded_key[i+3][j]
            temp_key = "".join(temp_key[:4])
            keys.append(temp_key)
        return keys

    def encrypt(self) -> str:
        blocks = self.split_text()
        returnBlocks = []
        round_keys = self.key_expansion()
        for block in blocks:
            block = self.add_round_key(block, round_keys[0])
            for i in range(1, 10):
                block = self.sub_bytes(block)
                block = self.shift_rows(block)
                block = self.mix_columns(block)
                block = self.add_round_key(block, round_keys[i])
                
            block = self.sub_bytes(block)
            block = self.shift_rows(block)
            block = self.add_round_key(block, round_keys[10])
            returnBlocks.append(block)
        return returnBlocks  
    
def encrypt(file_name: str) -> None:
    with open(file_name, "r") as file:
        text = file.read()
    aes = AES(text)
    print("Key: ", aes.key)
    blocks = aes.encrypt()
    print("Encrypted blocks: ", blocks)
    with open("encrypted.txt", "w") as file:
        for block in blocks:
            file.write("".join(block))
    print("Encryption successful, written to encrypted.txt")

if __name__ == '__main__':
    globals()[sys.argv[1]](* sys.argv[2:])