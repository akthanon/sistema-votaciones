Corregido, manteniendo los enlaces sin cambios y dejando tu username/placeholder original:

# 🗳️ Voting System

> **⚠️ WARNING:** This system contains security vulnerabilities that were created **accidentally** during its development. Do not use in production environments.

## 📋 Description

Web voting system built with Flask that, due to accidental errors during its development, presents multiple security flaws. Ideal for identifying and fixing common vulnerabilities.

## 🎯 The Researcher's Challenge

This system has been designed with **unintended** vulnerabilities that emerged during its development. The cybersecurity researcher's task is precisely to discover them, identify them, and propose solutions. Vulnerabilities may be hidden in different layers of the system: from the user interface to the server logic and the database. The challenge consists of applying pentesting techniques to find these flaws, understand their origin, and learn how to prevent them in real systems.

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/akthanon/sistema-votaciones-vulnerable.git
cd sistema-votaciones-vulnerable

# Install dependencies
pip install flask

# Run
python app.py
```

The system will be available at: `http://localhost:5000`

## 🎯 Features

- Voting for 2 candidates (Emilia 👩, Oscar 👨)
- Scoring system (0-100)
- Vote control by IP and cookie
- Real-time statistics
- Responsive interface

## ⚠️ Accidental Vulnerabilities

The system presents security errors that emerged **unintentionally** during development:

- Input validation failures
- Possible injection issues
- Session handling errors
- Insufficient data validation
- Possible race conditions

## 🔧 Requirements

- Python 3.6+
- Flask
- SQLite3

## 📄 License

MIT - Project for educational and learning purposes
