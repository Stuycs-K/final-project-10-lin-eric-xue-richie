from util import *
import os

class AES:
    def __init__(self, text: str):
        self.key = self.gen_256_key()  
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
            # get the 4 bytes in the column
            a = int(bytes_list[i], 16) 
            b = int(bytes_list[i+4], 16)
            c = int(bytes_list[i+8], 16)
            d = int(bytes_list[i+12], 16)
        
            #apply the fixed_col matrix to the column
            bytes_list[i]   = format(self.gmul(a, 0x02) ^ self.gmul(b, 0x03) ^ self.gmul(c, 0x01) ^ self.gmul(d, 0x01), "02x")
            bytes_list[i+4] = format(self.gmul(a, 0x01) ^ self.gmul(b, 0x02) ^ self.gmul(c, 0x03) ^ self.gmul(d, 0x01), "02x")
            bytes_list[i+8] = format(self.gmul(a, 0x01) ^ self.gmul(b, 0x01) ^ self.gmul(c, 0x02) ^ self.gmul(d, 0x03), "02x")
            bytes_list[i+12]= format(self.gmul(a, 0x03) ^ self.gmul(b, 0x01) ^ self.gmul(c, 0x01) ^ self.gmul(d, 0x02), "02x")

        return bytes_list
    
    def add_round_key(self, state: str, round_key: str) -> str:
        bytes_list = to_byte_array(state)
        round_key_list = to_byte_array(round_key)

        for i in range(0, 16):
            bytes_list[i] = format(int(bytes_list[i], 16) ^ int(round_key_list[i], 16), "02x")
        return bytes_list

