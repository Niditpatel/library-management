import builtins
import pytest
from librarian import issue_book, return_book
from storage import write_csv, read_csv

@pytest.fixture
def temp_data_files(tmp_path):
    # Setup temporary CSV files with initial data
    book_path = tmp_path / "books.csv"
    loan_path = tmp_path / "loans.csv"
    member_path = tmp_path / "members.csv"

    # Sample books data (ISBN, Title, Author, CopiesTotal, CopiesAvailable)
    books = [
        {"ISBN": "1234567890", "Title": "Test Book", "Author": "Author A", "CopiesTotal": "1", "CopiesAvailable": "1"},
    ]
    write_csv(book_path, books, ["ISBN", "Title", "Author", "CopiesTotal", "CopiesAvailable"])

    # Empty loans data
    loans = []
    write_csv(loan_path, loans, ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"])

    # Sample members data
    members = [
        {"MemberID": "1001", "Name": "Test Member", "PasswordHash": "", "Email": "test@mail.com", "JoinDate": "2025-01-01", "Role": "member"},
    ]
    write_csv(member_path, members, ["MemberID", "Name", "PasswordHash", "Email", "JoinDate", "Role"])

    return str(book_path), str(loan_path), str(member_path)

def test_issue_and_return(temp_data_files):
    book_path, loan_path, member_path = temp_data_files

    # Mock input for issue_book
    def mock_input_issue(prompt):
        if "ISBN" in prompt:
            return "1234567890"
        if "Member ID" in prompt:
            return "1001"
        return ""

    original_input = builtins.input
    builtins.input = mock_input_issue
    try:
        issue_book(book_path, loan_path, member_path)
    finally:
        builtins.input = original_input

    # Verify CopiesAvailable is decremented
    books = read_csv(book_path)
    assert books[0]['CopiesAvailable'] == '0'

    loans = read_csv(loan_path)
    assert any(
        l['MemberID'] == '1001' and l['ISBN'] == '1234567890' and l['ReturnDate'] == ''
        for l in loans
    ), "Loan was not created properly or missing ReturnDate"

    print("Loans before return:", loans)

    # Mock input for return_book
    def mock_input_return(prompt):
        if "ISBN" in prompt:
            return "1234567890"
        if "Member ID" in prompt:
            return "1001"
        return ""

    original_input = builtins.input
    builtins.input = mock_input_return
    try:
        return_book(book_path, loan_path)
    finally:
        builtins.input = original_input

    # Verify CopiesAvailable is incremented back
    books = read_csv(book_path)
    assert books[0]['CopiesAvailable'] == '1'
