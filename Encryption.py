# =========================
# encryption.py
# =========================
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:

    def __init__(self):
        """
        Initialize encryption system.
        """
        self.hashes = hashes
        self.secrets = secrets
        

    def generate_key(self, master_password, salt):
        """
        Generate encryption key.
        """
        kdf = PBKDF2HMAC(
            algorithm=self.hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=900000
        )
        aes_key = kdf.derive(master_password.encode())
        return aes_key

    def encrypt_password(self, password, key):
        """
        Encrypt plain password.
        """
        nonce = self.secrets.token_bytes(12)
        aes = AESGCM(key)
        encrypted_password = nonce + aes.encrypt(nonce ,password.encode(), None)
        return encrypted_password

    def decrypt_password(self, encrypted_password, key):
        """
        Decrypt encrypted password.
        """
        aes = AESGCM(key)
        decrypted_password = aes.decrypt(encrypted_password[:12], encrypted_password [12:], None)
        return decrypted_password.decode()
