import random


class Utils:
    @staticmethod
    def parse_byte_to_4_bits_tuple(number_byte: int):
        if number_byte < 0 or number_byte > 255:
            print("number is not a byte size")

        left_4_bit = (number_byte >> 4) & 0x0F
        right_4_bit = number_byte & 0x0F

        return left_4_bit, right_4_bit

    @staticmethod
    def convert_all_list_to_str(int_list):
        return [str(octet) for octet in int_list]
