"""
Implementation of the Java PBEWithMD5AndDES in Python
"""

# Imports
from Crypto.Hash import MD5
from Crypto.Cipher import DES


def salt_convert(salt_string):
    """
    Converts the salt string from TNL to the correct format for Python
    """
    output = ''
    parts = salt_string.split(',')

    for part in parts:
        part_num = int(part)
        if part_num < 0:
            part_num = 256 - abs(part_num)
        output += chr(part_num)

    return output


class PBEWithMD5AndDES:
    """
    Mimic Java's PBEWithMD5AndDES algorithm to produce a DES key
    """
    def __init__(self, enc_password, enc_salt, enc_iterations):
        self.enc_password = enc_password
        self.enc_salt = enc_salt
        self.enc_iterations = enc_iterations

    def encrypt(self, plaintext):
        padding = 8 - len(plaintext) % 8
        plaintext += chr(padding) * padding
        hasher = MD5.new()
        hasher.update(self.enc_password)
        hasher.update(self.enc_salt)
        result = hasher.digest()

        for i in range(1, self.enc_iterations):
            hasher = MD5.new()
            hasher.update(result)
            result = hasher.digest()

        encoder = DES.new(result[:8], DES.MODE_CBC, result[8:16])
        encrypted = encoder.encrypt(plaintext)

        return encrypted.encode('base64')
