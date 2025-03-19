
import csv
import os
import time
import statistics
from collections import deque

class TextSecurity:
    def __init__(self, shift):
        self.shifter = shift
        self.s = self.shifter % 26

    def _convert(self, text, s):
        result = ""
        for ch in text:
            if ch.isupper():
                result += chr((ord(ch) + s - 65) % 26 + 65)
            elif ch.islower():
                result += chr((ord(ch) + s - 97) % 26 + 97)
            else:
                result += ch
        return result

    def encrypt(self, text):
        return self._convert(text, self.shifter)

    def decrypt(self, text):
        return self._convert(text, 26 - self.s)

text_security = TextSecurity(4)
