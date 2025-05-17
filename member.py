from storage import read_csv, write_csv_row, write_csv_all
from datetime import datetime, timedelta

import uuid

def search_catalogue(book_path):
    books = read_csv(book_path)
    keyword = input("Search by title/author: ").lower()
    found = False
    for b in books:
        if keyword in b['Title'].lower() or keyword in b['Author'].lower():
            print(f"ISBN-{b['ISBN']} {b['Title']} by {b['Author']} - Available: {b['CopiesAvailable']}")
            found = True
    if not found:
        print("❌ No matching books found.")

def borrow_book(member, book_path, loan_path):
    books = read_csv(book_path)
    isbn = input("Enter ISBN to borrow: ").strip()
    book = next((b for b in books if b['ISBN'] == isbn), None)

    if not book:
        print("❌ Book not found.")
        return
    if int(book['CopiesAvailable']) <= 0:
        print("❌ No copies available.")
        return

    # Update CopiesAvailable
    book['CopiesAvailable'] = str(int(book['CopiesAvailable']) - 1)
    write_csv_all(book_path, books)

    # Add loan entry
    issue_date = datetime.today().date()
    due_date = issue_date + timedelta(days=14)

    new_loan = {
        'LoanID': str(uuid.uuid4())[:8],
        'MemberID': member.MemberID,
        'ISBN': isbn,
        'IssueDate': str(issue_date),
        'DueDate': str(due_date),
        'ReturnDate': ''
    }

    write_csv_row(loan_path, new_loan)
    print(f"✅ Book borrowed successfully! Due on {due_date.strftime('%d-%b-%Y')}.")

def my_loans(loan_path, member_id):
    loans = read_csv(loan_path)
    has_loans = False
    for l in loans:
        if l['MemberID'] == member_id:
            has_loans = True
            returned = l['ReturnDate'] if l['ReturnDate'] else 'Not returned'
            print(f"📘 ISBN: {l['ISBN']} | Issued: {l['IssueDate']} | Due: {l['DueDate']} | Returned: {returned}")
    if not has_loans:
        print("ℹ️ No loans found.")
