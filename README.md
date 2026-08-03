# 🔐 Password Manager CLI

A secure command-line password manager built with Python, featuring industry-standard encryption and authentication practices.

## Overview

This project was built as a hands-on exercise in applied cryptography and secure software design. It allows users to register, log in, and securely store, retrieve, and manage passwords for different websites — all encrypted at rest.

## Features

- 🔑 User registration and login with hashed master passwords
- 🔒 AES-GCM encryption for stored passwords, with a unique salt per entry
- 🧂 Key derivation via PBKDF2-HMAC-SHA256 (900,000 iterations)
- 📊 Password strength analysis using `zxcvbn`
- 🎲 Cryptographically secure random password generation
- 🔍 Search stored entries by website or username
- ✏️ Edit and delete existing entries

## Security Design

| Purpose | Method |
|---|---|
| Master password storage | `bcrypt` hashing |
| Password encryption | AES-GCM (authenticated encryption) |
| Key derivation | PBKDF2-HMAC-SHA256, 900,000 iterations |
| Salt | Unique 16-byte salt per password entry |

Each password is encrypted with a key derived from the user's master password and a per-entry salt — the master password itself is never stored, only its bcrypt hash.

## Project Structure
```
password-manager/
├── main.py          # CLI entry point
├── Auth.py           # Authentication logic (register/login/logout)
├── Database.py        # SQLite database layer
├── Encryption.py       # Encryption/decryption and key derivation
├── Password.py         # Core password manager logic
├── User.py            # Data models (User, PasswordEntry)
├── requirements.txt
└── .gitignore
```
## Installation

```bash
git clone https://github.com/yahya-toualbia/password-manager.git
cd password-manager
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Follow the on-screen menu to register an account, log in, and manage your passwords.

## Tech Stack

- Python 3
- `cryptography` — AES-GCM encryption, PBKDF2 key derivation
- `bcrypt` — master password hashing
- `zxcvbn` — password strength estimation
- SQLite — local storage

## Disclaimer

This project was built for educational purposes as part of a self-directed cybersecurity learning path. While it follows sound cryptographic practices, it has not undergone professional security auditing and should not be used to store real sensitive credentials in production.

## Author

Built by [yahya-toualbia](https://github.com/yahya-toualbia) — part of an ongoing journey into cybersecurity and secure software development.
