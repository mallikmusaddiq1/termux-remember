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
        email = input("📧 Enter your email: ").strip()
        password = getpass.getpass("🔐 Create password: ")
        password_hash = hash_password(password)
        self.user_data = {
            "email": email,
            "password_hash": password_hash,
            "session_active": False
        }
        save_json(USER_FILE, self.user_data)
        console.print("✅ [green]Signup complete.[/green] Now login to start using termux-remember.")

    def login(self):
        if not self.user_data:
            console.print("❌ [red]No account found.[/red] Run --signup first.")
            return False
        password = getpass.getpass("🔐 Enter password: ")
        if hash_password(password) == self.user_data.get("password_hash"):
            self.user_data["session_active"] = True
            save_json(USER_FILE, self.user_data)
            console.print("✅ [green]Logged in successfully.[/green]")
            return True
        else:
            console.print("❌ [red]Incorrect password.[/red]")
            return False

    def logout(self):
        self.user_data["session_active"] = False
        save_json(USER_FILE, self.user_data)
        console.print("👋 [cyan]Logged out.[/cyan]")

    def is_logged_in(self):
        return self.user_data.get("session_active", False)

    def verify_password(self):
        password = getpass.getpass("🔐 Confirm password: ")
        return hash_password(password) == self.user_data.get("password_hash")