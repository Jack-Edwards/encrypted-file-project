from Crypto.Cipher import AES


class SymmetricCrypto():
    def __init__(self, key: bytes, iv: bytes = None):
        self.cipher: AES.AESCipher = AES.new(key, AES.MODE_CFB, iv)
        self.iv = self.cipher.iv

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.cipher.decrypt(ciphertext)
