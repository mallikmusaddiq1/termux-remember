# 🧠 Termux Remember

**Secure CLI Note Keeper for Termux with Tagging & Password Protection**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)]()
[![Platform](https://img.shields.io/badge/platform-Termux%2FLinux-lightgrey)]()
[![PyPI](https://img.shields.io/pypi/v/termux-remember)](https://pypi.org/project/termux-remember/)
[![Downloads](https://static.pepy.tech/badge/termux-remember)](https://pepy.tech/project/termux-remember)

---

## 📦 Description

`termux-remember` is a secure, offline-first, and interactive command-line note-taking assistant built especially for Termux users. It supports:

- 📝 Multi-line and single-line notes
- 🔐 Password protection (per-note)
- 🏷️ Tagging system with powerful tag operations
- 🔍 Keyword search
- 🧩 Full interactive input modes
- 🖥️ Beautiful output with [rich](https://github.com/Textualize/rich)
- 📂 Local-only storage for privacy

---

## ⚙️ Installation

### Option 1: Clone and Install
```bash
git clone https://github.com/mallikmusaddiq1/termux-remember.git
cd termux-remember
pip install .
```

### Option 2: Install directly via pip
```bash
pip install termux-remember
```

> After installation, use the `remember` command from anywhere in Termux.

---

## 🧠 Termux Remember - CLI Reference

An interactive terminal-based assistant to securely store your personal notes, ideas, and tasks. Supports tagging, password-protection, multi-line entries, and keyword-based search.

---

## 📁 STORAGE DIRECTORY

- `~/.termux_remember/user.json` → User credentials
- `~/.termux_remember/memory.json` → Saved notes

---

## 🔐 USER AUTHENTICATION
```bash
--signup           Register with your email and password
--login            Login to your account
--logout           Logout from the current session
```

---

## 📝 NOTE ADDITION & EDITING
```bash
--add TEXT         Add a note (single-line)
--add              Launch interactive input mode (multi-line)
--edit-note ID     Edit a specific note by its ID (interactive)
--tag TAG          Add a tag to your note
--password         Protect your note with your login password
```

---

## 📥 INTERACTIVE INPUT MODES

### 1. Single-line input
```bash
remember --add "Today I learned Python!"
```

### 2. Multi-line interactive input
```bash
remember --add
```
Then type:
```
Note: This app is helpful.
It supports password protection.
EOF
```
✅ Finish with `EOF` on a new line  
✅ Use `\n` inside single-line input to simulate newlines
```bash
remember --add "Line1\nLine2"
```

---

## 🏷️ TAGGING & MANAGEMENT
```bash
--retag ID TAG             Change tag of a note
--list-tag                 List all unique tags
--delete-all-tags          Remove all tags
--delete-specific-tag TAG  Remove a specific tag
--rm-note-tag ID           Remove tag from a specific note
```

---

## 📋 LIST & SEARCH
```bash
--list             List all saved notes (🔐 = password-protected)
--find KEY         Search notes by keyword
--view-note ID     View full note by ID
--show-tag TAG     Show notes under a specific tag
```

---

## 🗑️ NOTE DELETION
```bash
--forget ID        Delete a specific note
--forget-all       Delete all notes (confirmation + password required)
```

---

## 🔐 SECURITY DETAILS
- Passwords stored securely using SHA-256 hashing
- Protected notes are hidden unless verified
- View/delete of protected notes requires confirmation

---

## 🧪 USAGE EXAMPLES
```bash
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
```

---

## 🔑 FORGOT PASSWORD?
Just create a new account using `--signup`

---

## 📦 VERSION & META
```bash
--version          Show version and author details
```

---

## 👨‍💻 AUTHOR
**Mallik Mohammad Musaddiq**  
📧 Email: mallikmusaddiq1@gmail.com  
🌐 GitHub: [mallikmusaddiq1](https://github.com/mallikmusaddiq1)

---

## 🌐 GITHUB REPOSITORY
[https://github.com/mallikmusaddiq1/termux-remember](https://github.com/mallikmusaddiq1/termux-remember)

---

## 📄 LICENSE
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for Termux users who don’t want to forget little things.s licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for Termux users who don't want to forget little things.
