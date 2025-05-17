from storage import read_csv, write_csv
from utils import today, due_date
from models import Loan
from datetime import datetime
from datetime import date

from dotenv import load_dotenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

import uuid

# Load environment variables
load_dotenv()

def add_book(book_path):
    books = read_csv(book_path)
    isbn = input("ISBN: ")
    if any(b['ISBN'] == isbn for b in books):
        print("❌ Book already exists.")
        return
    title = input("Title: ")
    author = input("Author: ")
    copies = int(input("Copies: "))
    book = {
        'ISBN': isbn,
        'Title': title,
        'Author': author,
        'CopiesTotal': copies,
        'CopiesAvailable': copies
    }
    books.append(book)
    write_csv(book_path, books, book.keys())
    print("✔ Book added.")


def delete_book(book_path, loan_path):
    books = read_csv(book_path)
    loans = read_csv(loan_path)

    isbn = input("ISBN to delete: ").strip()
    book = next((b for b in books if b['ISBN'].strip() == isbn), None)

    if not book:
        print("❌ Book not found.")
        return

    # Check for active loans (ReturnDate == '')
    active_loans = [loan for loan in loans if loan['ISBN'].strip() == isbn and loan['ReturnDate'].strip() == '']
    if active_loans:
        print("❌ Cannot delete. Book is currently on loan.")
        return

    books = [b for b in books if b['ISBN'].strip() != isbn]
    write_csv(book_path, books, fieldnames=book.keys())
    print("✔ Book deleted successfully.")

def issue_book(book_path, loan_path, member_path):
    books = read_csv(book_path)
    members = read_csv(member_path)
    loans = read_csv(loan_path)

    isbn = input("ISBN to issue: ")
    member_id = input("Member ID: ")

    book = next((b for b in books if b['ISBN'] == isbn), None)
    if not book or int(book['CopiesAvailable']) <= 0:
        print("❌ Book not available.")
        return

    if not any(m['MemberID'] == member_id for m in members):
        print("❌ Member not found.")
        return

    issue = today()
    due = due_date(issue)

    loan = {
        'LoanID': str(uuid.uuid4())[:8],
        'MemberID': member_id,
        'ISBN': isbn,
        'IssueDate': issue.isoformat(),
        'DueDate': due.isoformat(),
        'ReturnDate': ''
    }
    loans.append(loan)
    write_csv(loan_path, loans, loan.keys())

    book['CopiesAvailable'] = str(int(book['CopiesAvailable']) - 1)
    write_csv(book_path, books, book.keys())
    print(f"✔ Book issued. Due on {due.strftime('%d-%b-%Y')}.")


def return_book(book_path, loan_path):
    loans = read_csv(loan_path)
    books = read_csv(book_path)

    isbn = input("ISBN: ").strip()
    member_id = input("Member ID: ").strip()

    # Find the loan that matches ISBN, MemberID, and has empty ReturnDate
    loan_found = False
    for loan in loans:
        if (loan['ISBN'].strip() == isbn and
            loan['MemberID'].strip() == member_id and
            loan['ReturnDate'].strip() == ''):
            loan_found = True
            loan['ReturnDate'] = date.today().isoformat()
            break

    if not loan_found:
        print("❌ Loan not found or already returned.")
        return

    # Increment CopiesAvailable for the returned book
    for book in books:
        if book['ISBN'].strip() == isbn:
            # Convert to int, increment, then back to str for CSV storage
            book['CopiesAvailable'] = str(int(book['CopiesAvailable']) + 1)
            break

    # Save updated data back
    write_csv(loan_path, loans, fieldnames=loans[0].keys())
    write_csv(book_path, books, fieldnames=books[0].keys())

    print("✔ Book returned successfully.")


def overdue_list(loan_path, member_path):
    from datetime import date
    loans = read_csv(loan_path)
    members = read_csv(member_path)
    today_str = date.today().isoformat()

    overdue = [l for l in loans if l['ReturnDate'] == '' and l['DueDate'] < today_str]
    if not overdue:
        print("✔ No overdue loans.")
        return

    print("=== Overdue Loans ===")
    for loan in overdue:
        member = next((m for m in members if m['MemberID'] == loan['MemberID']), {})
        print(f"Loan ID: {loan['LoanID']}, Member: {member.get('Name', '?')}, Due: {loan['DueDate']}")


def send_email_reminders(loan_path, member_path):
    loans = read_csv(loan_path)
    members = read_csv(member_path)
    today_str = date.today().isoformat()

    overdue_loans = [l for l in loans if l['ReturnDate'] == '' and l['DueDate'] < today_str]
    if not overdue_loans:
        print("✔ No overdue loans.")
        return

    print("📧 Sending reminders to members with overdue books...")

    member_loans = {}
    for loan in overdue_loans:
        member_id = loan['MemberID']
        if member_id not in member_loans:
            member_loans[member_id] = []
        member_loans[member_id].append(loan)

    for member_id, loans in member_loans.items():
        member = next((m for m in members if m['MemberID'] == member_id), None)
        if not member or 'Email' not in member:
            continue

        email = member['Email']
        name = member.get('Name', 'Member')

        body = f"Dear {name},\n\nYou have the following overdue book(s):\n"
        for loan in loans:
            body += f"- ISBN: {loan['ISBN']}, Due Date: {loan['DueDate']}\n"
        body += "\nPlease return them as soon as possible.\n\nThanks,\nLibrary"

        send_email(email, "Overdue Book Reminder", body)

    print("✔ Email reminders sent.")




def send_email(to_email, subject, body):
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        print("❌ SENDGRID_API_KEY not set in environment variables.")
        return

    message = Mail(
        from_email='yourlibrary@example.com',
        to_emails=to_email,
        subject=subject,
        plain_text_content=body)

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print(f"📤 Sent email to {to_email}")
        else:
            print(f"❌ Failed to send email to {to_email}, status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception when sending email to {to_email}: {e}")
