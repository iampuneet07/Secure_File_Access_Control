import tkinter as tk
from tkinter import messagebox, filedialog
import auth
import file_manager

# Colors and styling
BG_COLOR = "#282C34"
FG_COLOR = "#ABB2BF"
BTN_COLOR = "#61AFEF"
FONT = ("Arial", 12)

class SecureFileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Access Control")
        self.root.geometry("500x450")
        self.root.config(bg=BG_COLOR)

        tk.Label(root, text="🔒 Secure File Access System", font=("Arial", 16, "bold"), fg="white", bg=BG_COLOR).pack(pady=10)

        # Buttons with styling
        self.create_styled_button("Register", self.register_user)
        self.create_styled_button("Login", self.login_user)
        self.create_styled_button("Upload File (Encrypt)", self.upload_file)
        self.create_styled_button("Download File (Decrypt)", self.download_file)
        self.create_styled_button("Exit", root.quit)

    def create_styled_button(self, text, command):
        btn = tk.Button(self.root, text=text, command=command, font=FONT, fg="white", bg=BTN_COLOR, relief="ridge", padx=20, pady=5)
        btn.pack(pady=8, ipadx=10, fill="x", padx=40)

    def register_user(self):
        self.create_popup_window("Register", self.process_registration)

    def login_user(self):
        self.create_popup_window("Login", self.process_login, show_otp=True)

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Encrypt")
        if file_path:
            username = self.get_username()
            if username:
                file_manager.upload_file(username, file_path)
                messagebox.showinfo("Success", "File encrypted and uploaded successfully")

    def download_file(self):
        file_path = filedialog.askopenfilename(title="Select an Encrypted File to Decrypt")
        if file_path:
            username = self.get_username()
            if username:
                file_manager.download_file(username, file_path)
                messagebox.showinfo("Success", "File decrypted successfully")

    def create_popup_window(self, title, submit_function, show_otp=False):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x300")
        popup.config(bg=BG_COLOR)

        tk.Label(popup, text="Username:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
        username_entry = tk.Entry(popup, font=FONT)
        username_entry.pack(pady=5)

        tk.Label(popup, text="Password:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
        password_entry = tk.Entry(popup, show="*", font=FONT)
        password_entry.pack(pady=5)

        otp_entry = None
        if show_otp:
            tk.Label(popup, text="2FA Code:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
            otp_entry = tk.Entry(popup, font=FONT)
            otp_entry.pack(pady=5)

        def submit():
            username = username_entry.get()
            password = password_entry.get()
            otp = otp_entry.get() if otp_entry else None
            submit_function(username, password, otp, popup)

        tk.Button(popup, text="Submit", command=submit, font=FONT, fg="white", bg=BTN_COLOR, relief="ridge").pack(pady=10)

    def process_registration(self, username, password, otp, popup):
        if auth.register(username, password):
            messagebox.showinfo("Success", "User registered successfully")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Registration failed")

    def process_login(self, username, password, otp, popup):
        if auth.login(username, password, otp):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Login failed")

    def get_username(self):
        popup = tk.Toplevel(self.root)
        popup.title("Enter Username")
        popup.geometry("250x150")
        popup.config(bg=BG_COLOR)

        tk.Label(popup, text="Username:", font=FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
        username_entry = tk.Entry(popup, font=FONT)
        username_entry.pack(pady=5)

        def confirm():
            self.username = username_entry.get()
            popup.destroy()

        tk.Button(popup, text="Confirm", command=confirm, font=FONT, fg="white", bg=BTN_COLOR).pack(pady=5)
        self.root.wait_window(popup)
        return self.username

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureFileApp(root)
    root.mainloop()
