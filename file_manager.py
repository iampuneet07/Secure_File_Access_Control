import sqlite3
import os
import log_manager
import encryption
import malware_scan

def initialize_file_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT UNIQUE NOT NULL,
                        owner TEXT NOT NULL,
                        shared_with TEXT DEFAULT NULL)''')
    conn.commit()
    conn.close()

def add_file_record(username, filename):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO files (filename, owner) VALUES (?, ?)", (filename, username))
    conn.commit()
    conn.close()

def upload_file(username, filename):
    if not os.path.exists(filename):
        log_manager.log_error(f"Upload failed: {filename} not found by {username}.")
        print(f"Error: File '{filename}' not found.")
        return

    if not malware_scan.is_safe_file(filename):
        log_manager.log_warning(f"Malware detected in {filename}. Upload blocked.")
        print("File upload denied due to security risk.")
        return

    encryption.encrypt_file(filename)
    add_file_record(username, filename + ".enc")

    log_manager.log_event(f"User {username} uploaded and encrypted {filename}.")
    print(f"File '{filename}' encrypted and uploaded successfully.")

initialize_file_db()
