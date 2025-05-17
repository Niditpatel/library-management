# Library Management System

A simple command-line Library Management System built with Python.  
It supports adding, issuing, returning, and deleting books, managing members, and sending email reminders for overdue books using SendGrid.

---

## Features

- Add new books with ISBN, title, author, and copies.
- Issue books to members with due dates.
- Return books and update availability.
- Delete books if not currently on loan.
- List overdue loans.
- Send email reminders automatically to members with overdue books (via SendGrid).


## File Structure

The project structure appears as follows:

Library\_Management\_System/
├── .vscode/
│   └── ... (VS Code configuration files)
├── data/
│   ├── books.csv
│   ├── loans.csv
│   └── members.csv
├── tests/
│   └── ... (Test files)
├── venv/
│   └── ... (Virtual environment)
├── auth.py
├── librarian.py
├── main.py
├── member.py
├── model.py
├── README.md
├── storage.py
└── utils.py

* auth.py: Likely handles user authentication and registration functionalities.
* librarian.py: Might contain functionalities specific to librarians (e.g., adding books, managing loans).
* main.py: The main entry point of the application.
* member.py: Could define the Member class and related functionalities.
* model.py: Might define the data models (e.g., Book, Loan).
* README.md: This file, providing a description of the project.
* storage.py: Likely handles data storage and retrieval (potentially using CSV files as seen in the data directory).
* utils.py: May contain utility functions used throughout the project.
* data/: Contains data files, including books.csv, loans.csv, and members.csv.
* tests/: Contains test files for the project.
* .vscode/: Contains VS Code specific configuration.
* venv/: The virtual environment containing project dependencies.

## Getting Started
1.  *Clone the repository* (if applicable). or Download the Zip Code
2.Create and activate a virtual environment (recommended):
  python -m venv venv
  venv\Scripts\activate -- for windows
  source venv/bin/activate -- for ios/linux
3. install the dependences 
  pip install bcrypt
  pip install pytest
  pip install python-dotenv
  pip install sendgrid
4. start project using 
  python main.py --data-dir ./data
5. test case -- how to run tests
   python -m pytest tests/test_issue_return.py

