# termux_remember/auth.py

import getpass
from rich.console import Console

from .utils import hash_password, load_json, save_json
from .constants import USER_FILE

console = Console()

class AuthManager:
    def __init__(self):
        self.user_data = load_json(USER_FILE)

    def signup(self):
        email = input("Enter your email: ").strip()
        password = getpass.getpass("Create password: ").strip()

        if not email or not password:
            console.print("Error: Email and password cannot be empty.")
            return

        password_hash = hash_password(password)
        self.user_data = {
            "email": email,
            "password_hash": password_hash,
            "session_active": False
        }
        save_json(USER_FILE, self.user_data)
        console.print("Signup successful. You can now login using --login.")

    def login(self):
        if not self.user_data:
            console.print("Error: No account found. Use --signup to create an account.")
            return False

        password = getpass.getpass("Enter password: ").strip()
        if hash_password(password) == self.user_data.get("password_hash"):
            self.user_data["session_active"] = True
            save_json(USER_FILE, self.user_data)
            console.print("Login successful.")
            return True
        else:
            console.print("Error: Incorrect password.")
            return False

    def logout(self):
        self.user_data["session_active"] = False
        save_json(USER_FILE, self.user_data)
        console.print("You have been logged out.")

    def is_logged_in(self):
        return self.user_data.get("session_active", False)

    def verify_password(self):
        password = getpass.getpass("Confirm password: ").strip()
        return hash_password(password) == self.user_data.get("password_hash")