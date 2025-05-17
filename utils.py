from datetime import datetime, timedelta

def today():
    return datetime.today().date()

def due_date(issue_date):
    return issue_date + timedelta(days=14)

# === librarian.py ===
from models import Book, Loan
from storage import read_csv, write_csv
from utils import today, due_date

import uuid

def add_book(book_path):
    books = read_csv(book_path)
    isbn = input("ISBN: ")
    if any(b['ISBN'] == isbn for b in books):
        print("❌ Book already exists.")
        return
    title = input("Title: ")
    author = input("Author: ")
    total = int(input("Total Copies: "))
    books.append({"ISBN": isbn, "Title": title, "Author": author, "CopiesTotal": total, "CopiesAvailable": total})
    write_csv(book_path, books, ["ISBN", "Title", "Author", "CopiesTotal", "CopiesAvailable"])
    print("✔ Book added.")

def issue_book(book_path, loan_path):
    books = read_csv(book_path)
    loans = read_csv(loan_path)
    isbn = input("ISBN to issue: ")
    member_id = input("Member ID: ")
    book = next((b for b in books if b['ISBN'] == isbn), None)
    if book and int(book['CopiesAvailable']) > 0:
        book['CopiesAvailable'] = str(int(book['CopiesAvailable']) - 1)
        loan = {
            "LoanID": str(uuid.uuid4()),
            "MemberID": member_id,
            "ISBN": isbn,
            "IssueDate": today().isoformat(),
            "DueDate": due_date(today()).isoformat(),
            "ReturnDate": ""
        }
        loans.append(loan)
        write_csv(book_path, books, ["ISBN", "Title", "Author", "CopiesTotal", "CopiesAvailable"])
        write_csv(loan_path, loans, ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"])
        print(f"✔ Book issued. Due on {loan['DueDate']}.")
    else:
        print("❌ Book unavailable.")

def return_book(book_path, loan_path):
    books = read_csv(book_path)
    loans = read_csv(loan_path)
    isbn = input("ISBN to return: ")
    member_id = input("Member ID: ")
    for loan in loans:
        if loan['ISBN'] == isbn and loan['MemberID'] == member_id and loan['ReturnDate'] == '':
            loan['ReturnDate'] = today().isoformat()
            for book in books:
                if book['ISBN'] == isbn:
                    book['CopiesAvailable'] = str(int(book['CopiesAvailable']) + 1)
            write_csv(book_path, books, ["ISBN", "Title", "Author", "CopiesTotal", "CopiesAvailable"])
            write_csv(loan_path, loans, ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"])
            print("✔ Book returned.")
            return
    print("❌ Loan not found.")

def overdue_list(loan_path):
    loans = read_csv(loan_path)
    print("\nOverdue Loans:")
    for loan in loans:
        if loan['ReturnDate'] == '' and loan['DueDate'] < today().isoformat():
            print(f" - Member {loan['MemberID']} | Book {loan['ISBN']} | Due {loan['DueDate']}")