import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("Encryption key generated and saved.")

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)

    os.remove(filename)
    print(f"File '{filename}' encrypted successfully.")

def decrypt_file(encrypted_filename):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    original_filename = encrypted_filename.replace(".enc", "")
    with open(original_filename, "wb") as file:
        file.write(decrypted_data)

    os.remove(encrypted_filename)
    print(f"File '{encrypted_filename}' decrypted successfully.")

generate_key()
