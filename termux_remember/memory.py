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

    def add_memory(self, text=None, tag=None, password_protected=False):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        if text is None:
            console.print("""[bold yellow]Enter your note:[/bold yellow]
[green]Type your note and end with 'EOF' on a new line.[/green]""")
            lines = []
            first_line = input("Note: ").strip()
            if not first_line or first_line == "EOF":
                console.print("[bold red]❌ Note cannot be empty.[/bold red]")
                return
            if "\\n" in first_line:
                text = first_line.replace("\\n", "\n")
            else:
                lines.append(first_line)
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                text = "\n".join(lines).strip()

        if not text:
            console.print("[bold red]❌ Note cannot be empty.[/bold red]")
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
        console.print(f"[bold green]✅ Note saved with ID {note_id}.[/bold green] 📁 Path: {MEMORY_FILE}")

    def edit_note(self, note_id, new_text=None):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("[bold red]❌ Note not found.[/bold red]")
            return

        if note.get("password_protected") and not self.auth.verify_password():
            console.print("[bold red]❌ Incorrect password.[/bold red]")
            return

        if new_text is None:
            note_panel = Panel(
                note["text"],
                title=f"✏️ Current Note {note_id}",
                subtitle=f"Tag: {note.get('tag') or 'None'}",
                border_style="cyan"
            )
            console.print(note_panel)
            console.print(
                "[bold yellow]📝 Enter new content:[/bold yellow]\n"
                "[green]Type your new content and finish by typing 'EOF' on a new line.[/green]"
            )

            lines = []
            first_line = input("New note: ").strip()
            if not first_line or first_line == "EOF":
                console.print("[bold red]❌ Note cannot be empty.[/bold red]")
                return
            if "\\n" in first_line:
                new_text = first_line.replace("\\n", "\n")
            else:
                lines.append(first_line)
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                new_text = "\n".join(lines).strip()

        if not new_text:
            console.print("[bold red]❌ Note cannot be empty.[/bold red]")
            return

        note["text"] = new_text
        note["timestamp"] = str(datetime.datetime.now())
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"[bold green]✅ Note {note_id} updated.[/bold green]")

    def delete_note(self, note_id):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print(f"[bold red]❌ Note {note_id} not found.[/bold red]")
            return

        if note.get("password_protected") and not self.auth.verify_password():
            console.print("[bold red]❌ Incorrect password.[/bold red]")
            return

        del self.memory_data[note_id]
        save_json(MEMORY_FILE, self.memory_data)
        console.print(f"[bold yellow]🗑️ Note {note_id} deleted.[/bold yellow]")

    def delete_all_notes(self):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        confirm = input("⚠️ Are you sure you want to delete all notes? (yes/no): ").strip().lower()
        if confirm != "yes":
            console.print("[yellow]❎ Deletion cancelled.[/yellow]")
            return

        if not self.auth.verify_password():
            console.print("[bold red]❌ Incorrect password.[/bold red]")
            return

        self.memory_data = {}
        save_json(MEMORY_FILE, self.memory_data)
        console.print("[bold red]🔥 All notes permanently deleted.[/bold red]")

    def delete_specific_tag(self, tag_to_delete):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        tag_found = False
        for note in self.memory_data.values():
            if note.get("tag") == tag_to_delete:
                note["tag"] = None
                tag_found = True

        if tag_found:
            save_json(MEMORY_FILE, self.memory_data)
            console.print(f"[bold green]🏷️ All notes with tag '{tag_to_delete}' have been untagged.[/bold green]")
        else:
            console.print(f"[yellow]⚠️ No notes found with tag '{tag_to_delete}'.[/yellow]")

    def delete_all_tags(self):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        for note in self.memory_data.values():
            note["tag"] = None

        save_json(MEMORY_FILE, self.memory_data)
        console.print("[bold green]🏷️ All tags have been removed from all notes.[/bold green]")

    def remove_note_tag(self, note_id):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔐 Please login first.[/bold red]")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print("[bold red]❌ Note not found.[/bold red]")
            return

        if note.get("tag"):
            note["tag"] = None
            save_json(MEMORY_FILE, self.memory_data)
            console.print(f"[yellow]🏷️ Tag removed from note {note_id}.[/yellow]")
        else:
            console.print(f"[blue]Note {note_id} has no tag assigned.[/blue]")

    def retag_note(self, note_id, new_tag):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔐 Please login first.[/bold red]")
            return

        note = self.memory_data.get(note_id)
        if not note:
            console.print(f"[red]❌ Note {note_id} not found.[/red]")
            return

        if new_tag.lower() == "null":
            note["tag"] = None
            console.print(f"[yellow]🏷️ Tag removed from note {note_id}.[/yellow]")
        else:
            note["tag"] = new_tag
            console.print(f"[green]🏷️ Note {note_id} updated with new tag: '{new_tag}'[/green]")

        save_json(MEMORY_FILE, self.memory_data)

    def list_notes(self):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔐 Please login first.[/bold red]")
            return

        if not self.memory_data:
            console.print("[yellow]📝 No notes found.[/yellow]")
            return

        table = Table(title="📋 Your Notes", header_style="bold magenta")
        table.add_column("ID", justify="center")
        table.add_column("Tag", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("🔒", justify="center")

        for note_id, entry in self.memory_data.items():
            tag = entry.get("tag") or "-"
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "🔐" if entry.get("password_protected") else ""
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, tag, display_text, locked)

        console.print(table)

    def list_tags(self):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔐 Please login first.[/bold red]")
            return

        tags = set()
        for entry in self.memory_data.values():
            if entry.get("tag"):
                tags.add(entry["tag"])

        if tags:
            tag_list = "\n".join(f"• {tag}" for tag in sorted(tags))
            console.print(Panel(tag_list, title="🏷️ Unique Tags", border_style="magenta"))
        else:
            console.print("[yellow]📭 No tags found.[/yellow]")

    def find_notes(self, keyword):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return

        found = False
        table = Table(title=f"🔍 Search Results for '{keyword}'", header_style="bold cyan")
        table.add_column("ID", justify="center")
        table.add_column("Tag", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("Count", justify="center")
        table.add_column("🔒", justify="center")

        for note_id, entry in self.memory_data.items():
            count = entry["text"].lower().count(keyword.lower())
            if count == 0:
                continue
            found = True
            tag = entry.get("tag") or "-"
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "🔐" if entry.get("password_protected") else ""
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, tag, display_text, str(count), locked)

        if found:
            console.print(table)
        else:
            console.print(f"[yellow]No matches found for keyword:[/yellow] '{keyword}'")

    def view_note(self, note_id):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔒 Please login first.[/bold red]")
            return
        note = self.memory_data.get(note_id)
        if not note:
            console.print("[bold red]❌ Note not found.[/bold red]")
            return
        if note.get("password_protected") and not self.auth.verify_password():
            console.print("[bold red]❌ Incorrect password.[/bold red]")
            return

        note_panel = Panel(
            note["text"],
            title=f"📄 Note {note_id}",
            subtitle=f"Tag: {note.get('tag') or 'None'}",
            title_align="left",
            subtitle_align="right",
            border_style="green"
        )
        console.print(note_panel)

    def show_notes_by_tag(self, tag):
        if not self.auth.is_logged_in():
            console.print("[bold red]🔐 Please login first.[/bold red]")
            return

        found = False
        table = Table(title=f"🏷️ Notes with Tag: {tag}", header_style="bold yellow")
        table.add_column("ID", justify="center")
        table.add_column("Preview", justify="left")
        table.add_column("🔒", justify="center")

        for note_id, entry in self.memory_data.items():
            if entry.get("tag") != tag:
                continue
            found = True
            preview = entry["text"].split("\n")[0][:50]
            if len(entry["text"].split("\n")[0]) > 50:
                preview += "..."
            locked = "🔐" if entry.get("password_protected") else ""
            display_text = "******" if entry.get("password_protected") else preview
            table.add_row(note_id, display_text, locked)

        if found:
            console.print(table)
        else:
            console.print(f"[yellow]⚠️ No notes found with tag: '{tag}'[/yellow]")