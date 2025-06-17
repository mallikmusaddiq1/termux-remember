# termux_remember/utils.py
import os
import json
import hashlib
from rich.console import Console

console = Console()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"❌ [red]Failed to load JSON from:[/red] {path} — {e}")
        return {}

def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        console.print(f"💾 [green]Saved:[/green] {path}")
    except Exception as e:
        console.print(f"❌ [red]Failed to save JSON to:[/red] {path} — {e}")