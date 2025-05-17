import csv
from models import Book, Member, Loan
from typing import List

def read_csv(file_path):
    with open(file_path, newline='') as f:
        return list(csv.DictReader(f))

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def load_books(path) -> List[Book]:
    return [Book(**row) for row in read_csv(path)]

def load_members(path) -> List[Member]:
    return [Member(**row) for row in read_csv(path)]

def load_loans(path) -> List[Loan]:
    return [Loan(**row) for row in read_csv(path)]


def write_csv_row(path, row):
    """Append a single row to a CSV file."""
    try:
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writerow(row)
    except FileNotFoundError:
        # Create new file with header
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            writer.writerow(row)

def write_csv_all(path, rows):
    """Overwrite entire CSV with given rows."""
    if not rows:
        return
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)