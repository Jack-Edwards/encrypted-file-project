from Crypto.Cipher import AES


class AES_EAX():
    def __init__(self, key: bytes, nonce: bytes = None):
        self.cipher = AES.new(key, AES.MODE_EAX, nonce)
        self.nonce = self.cipher.nonce

    def encrypt_and_digest(self, plaintext: bytes) -> (bytes, bytes):
        ciphertext, tag = self.cipher.encrypt_and_digest(plaintext)
        return ciphertext, tag

    def decrypt_and_verify(self, ciphertext: bytes, tag: bytes) -> bytes:
        """Return bytes if successful, 'None' if failure"""
        try:
            return self.cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            return None


class AES_CFB():
    def __init__(self, key: bytes, iv: bytes = None):
        self.cipher = AES.new(key, AES.MODE_CFB, iv)
        self.iv = self.cipher.iv

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.cipher.decrypt(ciphertext)
