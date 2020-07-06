import string
import random


class RandomComponent:

    @staticmethod
    def random_string(string_length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))