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
        #column arrays
        state_matrix = [[], [], [], []]
        for i in range(0, 16):
            state_matrix[i % 4].append(state[i])
        # Row 0: No shift
        # Row 1: Shift left by 1
        state_matrix[1] = state_matrix[1][1:] + state_matrix[1][:1]
        # Row 2: Shift left by 2
        state_matrix[2] = state_matrix[2][2:] + state_matrix[2][:2]
        # Row 3: Shift left by 3
        state_matrix[3] = state_matrix[3][3:] + state_matrix[3][:3]
        shifted_state = state_matrix[0] + state_matrix[1] + state_matrix[2] + state_matrix[3]
        shifted_state = to_byte_array(''.join(shifted_state)) 
        return shifted_state

    def mix_columns(self, state: str) -> list:
        #row arrays
        state_matrix = [state[i:i + 4] for i in range(0, len(state), 4)]
        for i in range(4):
            a = int(state_matrix[0][i], 16)
            b = int(state_matrix[1][i], 16)
            c = int(state_matrix[2][i], 16)
            d = int(state_matrix[3][i], 16)

            state_matrix[0][i] = format(gmul(a, 0x02) ^ gmul(b, 0x03) ^ gmul(c, 0x01) ^ gmul(d, 0x01), "02x")
            state_matrix[1][i] = format(gmul(a, 0x01) ^ gmul(b, 0x02) ^ gmul(c, 0x03) ^ gmul(d, 0x01), "02x")
            state_matrix[2][i] = format(gmul(a, 0x01) ^ gmul(b, 0x01) ^ gmul(c, 0x02) ^ gmul(d, 0x03), "02x")
            state_matrix[3][i] = format(gmul(a, 0x03) ^ gmul(b, 0x01) ^ gmul(c, 0x01) ^ gmul(d, 0x02), "02x")
        return [state_matrix[j][i] for i in range(4) for j in range(4)]

    def add_round_key(self, state: str, round_key: str) -> str:
        bytes_list = to_byte_array(state)
        round_key_list = to_byte_array(round_key)

        for i in range(0, 16):
            bytes_list[i] = format(int(bytes_list[i], 16) ^ int(round_key_list[i], 16), "02x")
        return bytes_list
        
    def key_expansion(self):
        key = to_byte_array(self.key)
        expanded_key = [key[i:i + 4] for i in range(0, len(key), 4)]
        rcon_counter = 0
        for i in range(4, 44):
            temp = expanded_key[i - 1]
            if i % 4 == 0:
                temp = rot_word(temp)
                temp = self.sub_bytes(temp)
                temp = rcon_xor(temp, rcon[rcon_counter])
                rcon_counter += 1
            word = [format(int(expanded_key[i - 4][j], 16) ^ int(temp[j], 16), "02x") for j in range(4)]
            expanded_key.append(word)
        
        round_keys = [''.join(expanded_key[i] + expanded_key[i+1] + expanded_key[i+2] + expanded_key[i+3]) for i in range(0, len(expanded_key), 4)]
        return round_keys
    
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
    print("Text:", text)
    print("Key:", aes.key)
    blocks = aes.encrypt()
    print("Encrypting...")
    with open("encrypted.txt", "w") as file:
        for block in blocks:
            file.write("".join(block))
    print("Encryption successful, written to encrypted.txt")

if __name__ == '__main__':
    globals()[sys.argv[1]](* sys.argv[2:])