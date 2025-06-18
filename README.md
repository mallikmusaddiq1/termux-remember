#  Termux Remember

**Secure CLI Note Keeper for Termux with Tagging & Password Protection**

---

## Description

`termux-remember` is a secure, offline-first, and interactive command-line note-taking assistant built especially for Termux users. It supports:

* Multi-line and single-line note input
* Password protection for sensitive notes
* Tagging system with tag editing and deletion
* Keyword search
* Interactive input mode
* Structured output using [rich](https://github.com/Textualize/rich)
* Local-only data storage for complete privacy

---

## Installation

### Option 1: Clone and Install

```bash
git clone https://github.com/mallikmusaddiq1/termux-remember.git
cd termux-remember
pip install .
```

### Option 2: Install via pip

```bash
pip install termux-remember
```

> After installation, run the CLI using the `remember` command.

---

## CLI Overview

A structured POSIX-style terminal application to securely store your thoughts, tasks, and ideas.

| Feature                   | Description                              |
| ------------------------- | ---------------------------------------- |
| --signup                  | Register a new account                   |
| --login                   | Log into your account                    |
| --logout                  | Log out from the current session         |
| --add \[TEXT]             | Add a note (inline or interactive)       |
| --edit-note ID            | Edit note by ID                          |
| --tag TAG                 | Tag a note                               |
| --password                | Protect a note                           |
| --list                    | List all notes                           |
| --find KEYWORD            | Search notes                             |
| --view-note ID            | View a note                              |
| --retag ID TAG            | Change tag of a note                     |
| --show-tag TAG            | Show all notes under a tag               |
| --list-tag                | List all unique tags                     |
| --delete-all-tags         | Delete all tags                          |
| --delete-specific-tag TAG | Remove specific tag from all notes       |
| --rm-note-tag ID          | Remove tag from specific note            |
| --forget ID               | Delete a note                            |
| --forget-all              | Delete all notes (requires confirmation) |
| --version                 | Show version info                        |

---

## Data Directory

```bash
~/.termux_remember/
├── user.json       # Stores user credentials
└── memory.json     # Stores notes and metadata
```

---

## Authentication

```bash
remember --signup
remember --login
remember --logout
```

---

## Notes Management

```bash
remember --add "Note content"
remember --add                       # Interactive input mode
remember --edit-note 3
remember --tag "personal"
remember --password
```

---

## Tagging System

```bash
remember --retag 2 work
remember --list-tag
remember --delete-all-tags
remember --delete-specific-tag "diary"
remember --rm-note-tag 4
```

---

## Listing and Search

```bash
remember --list
remember --find "budget"
remember --view-note 3
remember --show-tag "shopping"
```

---

## Deleting Notes

```bash
remember --forget 5
remember --forget-all
```

---

## Usage Examples

```bash
remember --add "Buy groceries" --tag "personal"
remember --add --tag "journal" --password
remember --edit-note 2
remember --view-note 2
remember --find "groceries"
```

---

## Forgot Password?

Create a new account using `--signup`.

---

## Metadata

```bash
remember --version
```

**Version**: 1.1.2
**Author**: Mallik Mohammad Musaddiq
**Email**: [mallikmusaddiq1@gmail.com](mailto:mallikmusaddiq1@gmail.com)
**GitHub**: [mallikmusaddiq1](https://github.com/mallikmusaddiq1)

---

## License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
