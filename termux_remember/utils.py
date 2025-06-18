# termux_remember/utils.py

import os
import json
import hashlib
from rich.console import Console

console = Console()

def hash_password(password):
    """Return SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(path):
    """
    Load JSON data from the specified file path.
    Returns an empty dictionary if the file is missing or unreadable.
    """
    if not os.path.exists(path):
        console.print(f"[yellow]File not found:[/yellow] {path}. Initializing empty store.")
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading JSON from[/red] {path}: {e}")
        return {}

def save_json(path, data):
    """
    Save the provided data dictionary to the specified JSON file path.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        console.print(f"[green]Data saved successfully to:[/green] {path}")
    except Exception as e:
        console.print(f"[red]Error saving JSON to[/red] {path}: {e}")