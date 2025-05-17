from dataclasses import dataclass

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    copies_total: int
    copies_available: int

@dataclass
class Member:
    MemberID: str
    Name: str
    PasswordHash: str
    Email: str
    JoinDate: str
    Role:str

@dataclass
class Loan:
    loan_id: str
    member_id: str
    isbn: str
    issue_date: str
    due_date: str
    return_date: str = ''
