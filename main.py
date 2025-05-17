import argparse
from auth import login, register_member, session
from librarian import add_book, delete_book, issue_book, return_book, overdue_list,send_email_reminders
from member import search_catalogue, borrow_book, my_loans

parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', default='./data')
args = parser.parse_args()

data_dir = args.data_dir
book_path = f"{data_dir}/books.csv"
member_path = f"{data_dir}/members.csv"
loan_path = f"{data_dir}/loans.csv"

def librarian_menu():
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book\n2. Delete Book\n3. Register Member\n4. Issue Book\n5. Return Book\n6. Overdue List\n7. Send Email Reminders for Overdue Books\n8. Logout")
        choice = input("> ")
        if choice == '1':
            add_book(book_path)
        elif choice == '2':
            delete_book(book_path, loan_path)
        elif choice == '3':
            register_member(member_path)
        elif choice == '4':
            issue_book(book_path, loan_path, member_path)
        elif choice == '5':
            return_book(book_path, loan_path)
        elif choice == '6':
            overdue_list(loan_path, member_path)
        elif choice == '7':
            send_email_reminders(loan_path, member_path)
        elif choice == '8':
            break
        else:
            print("❌ Invalid choice.")

def member_menu():
    while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Catalogue\n2. Borrow Book\n3. My Loans\n4. Logout")
        choice = input("> ")
        if choice == '1':
            search_catalogue(book_path)
        elif choice == '2':
            borrow_book(session['user'], book_path, loan_path)
        elif choice == '3':
            my_loans(loan_path, session['user'].MemberID)
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")

def main():
    print("Welcome to the Library System")

    while True:
        print("\n1. Register as Member")
        print("2. Register as Librarian")
        print("3. Login")
        print("4. Exit")
        top_choice = input("> ")
        if top_choice == '1':
            register_member(member_path, role='member')
        elif top_choice == '2':
            register_member(member_path, role='librarian')
        elif top_choice == '3':
            role = input("Login as (librarian/member): ").strip().lower()
            if login(member_path, role):
                if role == 'librarian':
                    librarian_menu()
                elif role == 'member':
                    member_menu()
            else:
                print("❌ Login failed. Try again.")
        elif top_choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
