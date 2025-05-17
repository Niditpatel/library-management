import bcrypt
from datetime import date
from models import Member
from storage import read_csv, write_csv
import getpass

session = {}

def register_member(member_path, role='member'):
    members = read_csv(member_path)
    member_id = input("Member ID: ").strip()

    if any(m['MemberID'] == member_id for m in members):
        print("❌ Member ID already exists.")
        return

    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ").strip()
    confirm = getpass.getpass("Confirm Password: ").strip()

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    join_date = date.today().isoformat()

    members.append({
        "MemberID": member_id,
        "Name": name,
        "PasswordHash": hashed,
        "Email": email,
        "JoinDate": join_date,
        "Role": role
    })

    write_csv(member_path, members, ["MemberID", "Name", "PasswordHash", "Email", "JoinDate", "Role"])
    print(f"✔ {role.capitalize()} registered successfully.")

def login(member_path, role):
    members = read_csv(member_path)
    user_id = input("ID: ").strip()
    password = getpass.getpass("Password: ").strip()

    user = next((m for m in members if m['MemberID'] == user_id and m.get('Role', 'member') == role), None)

    if user and bcrypt.checkpw(password.encode(), user['PasswordHash'].encode()):
        session['role'] = role
        session['user'] = Member(**{
            "MemberID": user['MemberID'],
            "Name": user['Name'],
            "PasswordHash": user['PasswordHash'],
            "Email": user['Email'],
            "JoinDate": user['JoinDate'],
            "Role": user['Role']  # ✅ Add this line
        })
        print(f"✔ Logged in as {user['Name']} ({role})")
        return True
    else:
        print("❌ Login failed.")
        return False
