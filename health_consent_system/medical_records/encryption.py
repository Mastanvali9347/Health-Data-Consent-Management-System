from cryptography.fernet import Fernet
from django.conf import settings
import os

KEY_PATH = os.path.join(settings.BASE_DIR, 'secret.key')

def get_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_PATH, 'rb') as f:
            key = f.read()
    return key

fernet = Fernet(get_key())

def encrypt_file(file_data):
    return fernet.encrypt(file_data)

def decrypt_file(file_data):
    return fernet.decrypt(file_data)
