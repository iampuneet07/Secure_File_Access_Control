import sqlite3
import bcrypt
import pyotp

# Initialize user database
def initialize_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        secret TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Register a new user
def register(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Error: Username already exists.")
        conn.close()
        return False

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    secret = pyotp.random_base32()

    cursor.execute("INSERT INTO users (username, password, secret) VALUES (?, ?, ?)", 
                   (username, hashed_password, secret))
    conn.commit()
    conn.close()
    
    print(f"User '{username}' registered successfully.")
    print(f"Your 2FA Secret Key (store safely): {secret}")  
    return True

# User login with password and 2FA
def login(username, password, otp):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password, secret FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        stored_password, secret = user
        if bcrypt.checkpw(password.encode(), stored_password):
            totp = pyotp.TOTP(secret)
            if totp.verify(otp):  
                print("Login successful.")
                return True
            else:
                print("Error: Invalid OTP.")
        else:
            print("Error: Incorrect password.")
    else:
        print("Error: User not found.")
    
    conn.close()
    return False

initialize_db()
