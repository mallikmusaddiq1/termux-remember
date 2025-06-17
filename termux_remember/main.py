# termux_remember/main.py

import argparse
import sys
from argparse import RawTextHelpFormatter
from rich.console import Console

from termux_remember.constants import version, author, email, github
from termux_remember.auth import AuthManager
from termux_remember.memory import MemoryManager

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description=f"""
🧠 Termux Remember – A Secure CLI Note Keeper for Termux
────────────────────────────────────────────────────────────
An interactive terminal-based assistant to securely store your 
personal notes, ideas, and tasks. Supports tagging, password 
protection, multi-line entries, and keyword-based search.

📁 STORAGE DIRECTORY
────────────────────
• User credentials : ~/.termux_remember/user.json
• Saved notes      : ~/.termux_remember/memory.json

🔐 USER AUTHENTICATION
──────────────────────
• --signup               Register using email and password
• --login                Login to your account
• --logout               Logout from the current session

📝 NOTE ADDITION & EDITING
────────────────────────────
• --add TEXT             Add a note (only single-line input if TEXT is provided)
• --add                  Launch interactive input mode (single & multi-line input)
• --edit-note ID         Edit a specific note by ID (interactive)
• --tag TAG              Assign a tag to your note (e.g., --tag "personal")
• --password             Protect note using your account password

📥 INTERACTIVE INPUT MODES
────────────────────────────
• Use --add "your note"        → For single-line notes
• Use just --add               → For interactive multi-line input
  ↳ Type lines and finish with: EOF

🔁 Examples:
$ remember --add
> Today was great
> I am very happy
> EOF

🏷️ TAGGING & MANAGEMENT
────────────────────────
• --retag ID TAG              Change tag of a specific note
• --list-tag                  List all unique tags
• --delete-all-tags           Remove all tags from all notes
• --delete-specific-tag TAG   Remove a specific tag from all notes
• --rm-note-tag ID            Remove tag from a specific note

📋 LIST & SEARCH
────────────────
• --list                      List all notes (****** 🔒 indicated protected notes)
• --find KEY                  Search notes by keyword
• --view-note ID              View full content of a note
• --show-tag TAG              Show all notes under a specific tag

🗑️ NOTE DELETION
─────────────────
• --forget ID                 Delete a specific note
• --forget-all                Delete ALL notes (confirmation + password)

🔐 SECURITY DETAILS
────────────────────
• Passwords hashed with SHA-256
• Deletion/viewing of protected notes requires confirmation

🧪 USAGE EXAMPLES
──────────────────
remember --signup
remember --login
remember --add "Call mom" --tag "family"
remember --add --tag "diary" --password
remember --edit-note 2
remember --find "milk"
remember --view-note 2
remember --retag 2 "tasks"
remember --list-tag
remember --delete-all-tags
remember --delete-specific-tag "family"
remember --rm-note-tag 2
remember --forget 2
remember --forget-all

🔑 FORGOT PASSWORD?
────────────────────
Create a new account using --signup

📦 VERSION & META
──────────────────
• --version    Display current version and author info

👨‍💻 AUTHOR
─────────────
• Author  : {author}
• Email   : {email}
• GitHub  : {github}

🌐 GITHUB REPO
───────────────
{github}

Made with ❤️ for Termux users who don’t want to forget little things.
""",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("--signup", action="store_true", help="Create a new user account")
    parser.add_argument("--login", action="store_true", help="Login to your account")
    parser.add_argument("--logout", action="store_true", help="Logout from your session")
    parser.add_argument("--add", nargs='?', default=None, type=str, help="Add a new note (single-line with TEXT, or interactive if no TEXT)")
    parser.add_argument("--edit-note", metavar='ID', type=str, help="Edit a specific note by its ID (interactive)")
    parser.add_argument("--tag", metavar='TAG', type=str, help="Organize notes with unique tag ")
    parser.add_argument("--password", action="store_true", help="Protect the note with your login password")
    parser.add_argument("--list", action="store_true", help="List all saved notes")
    parser.add_argument("--find", metavar='KEY', type=str, help="Search notes by keyword")
    parser.add_argument("--view-note", metavar='ID', type=str, help="View a specific note by its ID")
    parser.add_argument("--show-tag", metavar='TAG', type=str, help="Show notes with a specific tag")
    parser.add_argument("--retag", nargs=2, metavar=('ID', 'TAG'), help="Change the tag of a specific note")
    parser.add_argument("--list-tag", action="store_true", help="List all unique tags")
    parser.add_argument("--delete-all-tags", action="store_true", help="Remove all tags from all notes")
    parser.add_argument("--delete-specific-tag", metavar='TAG', type=str, help="Remove a specific tag from all notes")
    parser.add_argument("--rm-note-tag", metavar='ID', type=str, help="Remove tag from a specific note")
    parser.add_argument("--forget", metavar='ID', type=str, help="Delete a specific note by its ID")
    parser.add_argument("--forget-all", action="store_true", help="Delete all notes (require confirmation & password)")
    parser.add_argument("--version", action="store_true", help="Show current version of the app ")

    args = parser.parse_args()

    if args.version:
        console.print(f"""
[bold green]📦 termux-remember v{version}[/bold green]
[bold cyan]🧑‍💻 Author:[/bold cyan] {author}
[bold blue]🔗 GitHub:[/bold blue] {github}
[bold yellow]✉️ Email:[/bold yellow] {email}

[bold magenta]Made with ❤️ for Termux users who don’t want to forget little things.[/bold magenta]
""")
        return

    auth = AuthManager()
    memory = MemoryManager()

    if args.signup:
        auth.signup()
    elif args.login:
        auth.login()
    elif args.logout:
        auth.logout()
    elif '--add' in sys.argv or args.tag or args.password:
        note_text = args.add
        if note_text is None:
            memory.add_memory(text=None, tag=args.tag, password_protected=args.password)
        elif note_text.strip() == "":
            console.print("[bold red]❌ Empty note text. For multi-line or interactive input, use just --add without quotes.[/bold red]")
        else:
            memory.add_memory(text=note_text, tag=args.tag, password_protected=args.password)
    elif args.edit_note:
        memory.edit_note(args.edit_note)
    elif args.list:
        memory.list_notes()
    elif args.find:
        memory.find_notes(args.find)
    elif args.view_note:
        memory.view_note(args.view_note)
    elif args.show_tag:
        memory.show_notes_by_tag(args.show_tag)
    elif args.retag:
        memory.retag_note(args.retag[0], args.retag[1])
    elif args.list_tag:
        memory.list_tags()
    elif args.delete_all_tags:
        memory.delete_all_tags()
    elif args.delete_specific_tag:
        memory.delete_specific_tag(args.delete_specific_tag)
    elif args.rm_note_tag:
        memory.remove_note_tag(args.rm_note_tag)
    elif args.forget:
        memory.delete_note(args.forget)
    elif args.forget_all:
        memory.delete_all_notes()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()