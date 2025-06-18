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
Termux Remember - Secure Note Keeper for Termux
------------------------------------------------
A command-line assistant for storing personal notes, ideas, and tasks with optional tagging,
password protection, and search functionality.

STORAGE PATHS
-------------
• Credentials : ~/.termux_remember/user.json
• Notes       : ~/.termux_remember/memory.json

AUTHENTICATION
--------------
• --signup               Create a new account
• --login                Login to an existing account
• --logout               Logout from current session

NOTE ADDITION & EDITING
------------------------
• --add TEXT             Add a single-line note
• --add                  Launch interactive note input
• --edit-note ID         Edit a note by ID
• --tag TAG              Tag a note (e.g., --tag "task")
• --password             Protect the note with password

TAG MANAGEMENT
--------------
• --retag ID TAG              Replace tag of a note
• --list-tag                  List all tags
• --delete-all-tags           Remove all tags from all notes
• --delete-specific-tag TAG   Remove specific tag from all notes
• --rm-note-tag ID            Remove tag from a single note

LISTING & SEARCH
----------------
• --list                  Display all notes
• --find KEY              Search notes by keyword
• --view-note ID          View a specific note
• --show-tag TAG          View notes under a specific tag

DELETION
--------
• --forget ID             Delete note by ID
• --forget-all            Delete all notes (confirmation required)

MISC
----
• --version               Show version and author info

EXAMPLES
--------
$ remember --signup
$ remember --add "Buy milk" --tag "groceries"
$ remember --add --tag "journal" --password
$ remember --edit-note 3
$ remember --list
$ remember --find "meeting"
$ remember --view-note 2
$ remember --retag 2 "work"
$ remember --delete-specific-tag "personal"
$ remember --forget 4
$ remember --forget-all

GitHub: {github}
""",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("--signup", action="store_true", help="Create a new user account")
    parser.add_argument("--login", action="store_true", help="Login to your account")
    parser.add_argument("--logout", action="store_true", help="Logout from your session")
    parser.add_argument("--add", nargs='?', default=None, type=str, help="Add a note (single-line with TEXT or interactive if no TEXT)")
    parser.add_argument("--edit-note", metavar='ID', type=str, help="Edit a note by ID")
    parser.add_argument("--tag", metavar='TAG', type=str, help="Add tag to the note")
    parser.add_argument("--password", action="store_true", help="Protect the note using password")
    parser.add_argument("--list", action="store_true", help="List all notes")
    parser.add_argument("--find", metavar='KEY', type=str, help="Search notes by keyword")
    parser.add_argument("--view-note", metavar='ID', type=str, help="View a note by ID")
    parser.add_argument("--show-tag", metavar='TAG', type=str, help="Show notes by tag")
    parser.add_argument("--retag", nargs=2, metavar=('ID', 'TAG'), help="Change tag of a note")
    parser.add_argument("--list-tag", action="store_true", help="List all unique tags")
    parser.add_argument("--delete-all-tags", action="store_true", help="Remove all tags")
    parser.add_argument("--delete-specific-tag", metavar='TAG', type=str, help="Remove specific tag from all notes")
    parser.add_argument("--rm-note-tag", metavar='ID', type=str, help="Remove tag from a specific note")
    parser.add_argument("--forget", metavar='ID', type=str, help="Delete a specific note")
    parser.add_argument("--forget-all", action="store_true", help="Delete all notes with confirmation")
    parser.add_argument("--version", action="store_true", help="Show application version and info")

    args = parser.parse_args()

    if args.version:
        console.print(f"""
termux-remember v{version}
Author : {author}
Email  : {email}
GitHub : {github}
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
            console.print("Error: Note text cannot be empty. For multi-line input, use just --add without quotes.")
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
