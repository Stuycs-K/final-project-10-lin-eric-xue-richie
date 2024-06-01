import unittest
from aes import *

class TestAES(unittest.TestCase):
    def setUp(self):
        self.example = "Lorem Ipsum is s"
        self.aes = AES(self.example)
        self.input_state = "63EB9FA02F9392C0AFC7AB30A220CB2B"
        self.expected_output = "BA84E81B75A48D40F48D067D7A320E5D"

    def test_split_text_to_hex_init(self):
        expected_hex = "4c 6f 72 65 6d 20 49 70 73 75 6d 20 69 73 20 73"
        actual_hex = to_hex(self.aes.split_text())
        self.assertEqual(actual_hex, expected_hex)

    def test_sub_bytes(self):
        pre_shift = "4c 6f 72 65 6d 20 49 70 73 75 6d 20 69 73 20 73"
        expected_subbed = ['29', '6f', '76', '40', '6f', '6b', '3c', '77', '63', '3b', 'c5', '63', '8f', 'c5', '6b', '3c', '77', '63', 'f9', 'c5', '7b', 'b7', 'c5', '7b']
        actual_subbed = self.aes.sub_bytes(pre_shift)
        self.assertEqual(actual_subbed, expected_subbed)

    def test_shift_rows(self):
        pre_shift = ['29', '6f', '76', '40', '6f', '6b', '3c', '77', '63', '3b', 'c5', '63', '8f', 'c5', '6b', '3c', '77', '63', 'f9', 'c5', '7b', 'b7', 'c5', '7b']
        expected_post_shift = ['29', '6f', '76', '40', '6b', '3c', '77', '6f', 'c5', '63', '63', '3b', '3c', '8f', 'c5', '6b', '77', '63', 'f9', 'c5', '7b', 'b7', 'c5', '7b']
        actual_post_shift = self.aes.shift_rows(pre_shift)
        self.assertEqual(actual_post_shift, expected_post_shift)

    def test_gmul(self):
        self.assertEqual(self.aes.gmul(0x57, 0x13), 0xfe)

    def test_mix_columns(self):
        actual_output = "".join(self.aes.mix_columns(self.input_state)).upper()
        self.assertEqual(actual_output, self.expected_output)

    def test_add_round_key(self):
        round_key = "E291B1D632125979FC91E4A2F188E693"
        actual_output = "".join(self.aes.add_round_key(self.expected_output, round_key)).upper()
        self.assertEqual(actual_output, "581559CD47B6D439081CE2DF8BBAE8CE")

if __name__ == '__main__':
    unittest.main()