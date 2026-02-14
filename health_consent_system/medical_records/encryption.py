from cryptography.fernet import Fernet
from django.conf import settings
import os

KEY_PATH = os.path.join(settings.BASE_DIR, "secret.key")

def get_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        return key
    with open(KEY_PATH, "rb") as f:
        return f.read()

fernet = Fernet(get_key())

def encrypt_file(data: bytes) -> bytes:
    return fernet.encrypt(data)

def decrypt_file(data: bytes) -> bytes:
    return fernet.decrypt(data)
