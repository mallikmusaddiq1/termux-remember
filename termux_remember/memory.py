# termux_remember/memory.py

import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .utils import load_json, save_json
from .constants import MEMORY_FILE
from .auth import AuthManager

console = Console()

class MemoryManager:
    def __init__(self):
        self.memory_data = load_json(MEMORY_FILE)
        self.auth = AuthManager()

    def _input_multiline(self, prompt):
        console.print(prompt)
        lines = []
        first_line = input("> ").strip()
        if not first_line or first_line == "EOF":
            return None
        if "\\n" in first_line:
            return first_line.replace("\\n", "\n")
        lines.append(first_line)
        while True:
            line = input()
            if line.strip() == "EOF":
                break
            lines.append(line)
        return "\n".join(lines).strip()

    def add_memory(self, text=None, tag=None, password_protected=False):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        if text is None:
            text = self._input_multiline(
                "[Enter your note. End with 'EOF' on a new line.]"
            )

        if not text:
            console.print("Note cannot be empty.")
            return

        note_id = str(len(self.memory_data) + 1)
        entry = {
            "id": note_id,
            "text": text,
            "tag": tag,
            "timestamp": str(datetime.datetime.now()),
            "password_protected": password_protected
        }
        self.memory_data[note_id] = entry
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"Note saved with ID {note_id}.")

    def edit_note(self, note_id, new_text=None):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("Note not found.")
            return

        if note.get("password_protected") and not self.auth.verify_password():
            console.print("Incorrect password.")
            return

        if new_text is None:
            console.print(Panel(note["text"], title=f"Current Note {note_id}", subtitle=f"Tag: {note.get('tag') or 'None'}", border_style="cyan"))
            new_text = self._input_multiline("[Enter new content. End with 'EOF']")

        if not new_text:
            console.print("Note cannot be empty.")
            return

        note["text"] = new_text
        note["timestamp"] = str(datetime.datetime.now())
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"Note {note_id} updated.")

    def delete_note(self, note_id):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("Note not found.")
            return

        if note.get("password_protected") and not self.auth.verify_password():
            console.print("Incorrect password.")
            return

        del self.memory_data[note_id]
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"Note {note_id} deleted.")

    def delete_all_notes(self):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        confirm = input("Are you sure you want to delete all notes? (yes/no): ").strip().lower()
        if confirm != "yes":
            console.print("Operation cancelled.")
            return

        if not self.auth.verify_password():
            console.print("Incorrect password.")
            return

        self.memory_data = {}
        save_json(MEMORY_FILE, self.memory_data)
        console.print("All notes deleted.")

    def delete_specific_tag(self, tag_to_delete):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        found = False
        for note in self.memory_data.values():
            if note.get("tag") == tag_to_delete:
                note["tag"] = None
                found = True

        if found:
            save_json(MEMORY_FILE, self.memory_data)
            console.print(f"All notes with tag '{tag_to_delete}' untagged.")
        else:
            console.print(f"No notes found with tag '{tag_to_delete}'.")

    def delete_all_tags(self):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        for note in self.memory_data.values():
            note["tag"] = None

        save_json(MEMORY_FILE, self.memory_data)
        console.print("All tags removed.")

    def remove_note_tag(self, note_id):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("Note not found.")
            return

        if note.get("tag"):
            note["tag"] = None
            save_json(MEMORY_FILE, self.memory_data)
            console.print(f"Tag removed from note {note_id}.")
        else:
            console.print(f"Note {note_id} has no tag.")

    def retag_note(self, note_id, new_tag):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("Note not found.")
            return

        note["tag"] = None if new_tag.lower() == "null" else new_tag
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"Note {note_id} tag updated.")

    def list_notes(self):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        if not self.memory_data:
            console.print("No notes found.")
            return

        table = Table(title="Notes", header_style="bold")
        table.add_column("ID", justify="center")
        table.add_column("Tag", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("Locked", justify="center")

        for note_id, entry in self.memory_data.items():
            tag = entry.get("tag") or "-"
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "Yes" if entry.get("password_protected") else "No"
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, tag, display_text, locked)

        console.print(table)

    def list_tags(self):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        tags = {entry["tag"] for entry in self.memory_data.values() if entry.get("tag")}
        if tags:
            tag_list = "\n".join(sorted(tags))
            console.print(Panel(tag_list, title="Tags", border_style="dim"))
        else:
            console.print("No tags found.")

    def find_notes(self, keyword):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        table = Table(title=f"Search: '{keyword}'", header_style="bold")
        table.add_column("ID", justify="center")
        table.add_column("Tag", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("Matches", justify="center")
        table.add_column("Locked", justify="center")

        found = False
        for note_id, entry in self.memory_data.items():
            count = entry["text"].lower().count(keyword.lower())
            if count == 0:
                continue
            found = True
            tag = entry.get("tag") or "-"
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "Yes" if entry.get("password_protected") else "No"
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, tag, display_text, str(count), locked)

        if found:
            console.print(table)
        else:
            console.print(f"No matches found for '{keyword}'.")

    def view_note(self, note_id):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("Note not found.")
            return

        if note.get("password_protected") and not self.auth.verify_password():
            console.print("Incorrect password.")
            return

        note_panel = Panel(
            note["text"],
            title=f"Note {note_id}",
            subtitle=f"Tag: {note.get('tag') or 'None'}",
            title_align="left",
            subtitle_align="right",
            border_style="green"
        )
        console.print(note_panel)

    def show_notes_by_tag(self, tag):
        if not self.auth.is_logged_in():
            console.print("Please login first.")
            return

        table = Table(title=f"Notes with Tag: {tag}", header_style="bold")
        table.add_column("ID", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("Locked", justify="center")

        found = False
        for note_id, entry in self.memory_data.items():
            if entry.get("tag") != tag:
                continue
            found = True
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "Yes" if entry.get("password_protected") else "No"
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, display_text, locked)

        if found:
            console.print(table)
        else:
            console.print(f"No notes found with tag: '{tag}'")