import hashlib
import os

USERS_FILE = "users.txt"

# ================= HASH =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= USERS =================
def load_users():
    users = []
    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                users.append(line.strip().split(","))
    except FileNotFoundError:
        pass
    return users

def save_user(username, password):
    with open(USERS_FILE, "a") as file:
        file.write(username + "," + hash_password(password) + "\n")

# ================= LOGIN SYSTEM (مع رجعة) =================
def login():
    while True:
        print("\n1. New user")
        print("2. Existing user")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "0":
            exit()

        #  NEW USER
        elif choice == "1":
            username = input("Enter username (or 0 to go back): ")
            if username == "0":
                continue

            users = load_users()
            for u in users:
                if u[0] == username:
                    print("Username already exists!")
                    break
            else:
                while True:
                    password = input("Enter password (or 0 to go back): ")
                    if password == "0":
                        break

                    confirm = input("Confirm password: ")

                    if password != confirm:
                        print("Passwords do not match!")
                        continue

                    save_user(username, password)
                    print("User created successfully!")
                    return username

        #  EXISTING USER
        elif choice == "2":
            while True:
                username = input("Username (or 0 to go back): ")
                if username == "0":
                    break

                password = input("Password (or 0 to go back): ")
                if password == "0":
                    break

                users = load_users()

                for u in users:
                    if u[0] == username and u[1] == hash_password(password):
                        print("Login successful!")
                        return username

                print("Wrong username or password!")

        else:
            print("Invalid choice!")

# ================= ACCOUNTS =================
def get_file(username):
    return f"{username}.txt"

def load_accounts(username):
    accounts = []
    try:
        with open(get_file(username), "r") as file:
            for line in file:
                accounts.append(line.strip().split(","))
    except FileNotFoundError:
        pass
    return accounts

def save_accounts(username, accounts):
    with open(get_file(username), "w") as file:
        for acc in accounts:
            file.write(",".join(acc) + "\n")

def print_accounts(accounts):
    print("\nYour accounts:")
    for i, acc in enumerate(accounts, 1):
        hidden_password = "*" * 6
        print(i, "|", acc[0], "|", acc[1], "|", hidden_password)
    print("----------------------")

# ================= START =================
current_user = login()
accounts = load_accounts(current_user)

while True:
    print("\n1.Add account")
    print("2.Show accounts")
    print("3.Delete account")
    print("4.Search account")
    print("5.Edit account")
    print("6.Exit")

    choice = input("Choose: ")

    # ================= ADD =================
    if choice == "1":
        website = input("Website (0 to go back): ")
        if website == "0":
            continue

        username = input("Username (0 to go back): ")
        if username == "0":
            continue

        password = input("Password (0 to go back): ")
        if password == "0":
            continue

        accounts.append([website, username, hash_password(password)])
        save_accounts(current_user, accounts)
        print("Account added successfully!")

    # ================= SHOW =================
    elif choice == "2":
        if not accounts:
            print("No accounts!")
        else:
            print_accounts(accounts)
            input("Press Enter to go back...")

    # ================= DELETE =================
    elif choice == "3":
        print_accounts(accounts)

        num = input("Enter number (0 to go back): ")
        if num == "0":
            continue

        try:
            num = int(num)
        except ValueError:
            print("Invalid number!")
            continue

        if num < 1 or num > len(accounts):
            print("Invalid number!")
            continue

        accounts.pop(num - 1)
        save_accounts(current_user, accounts)
        print("Deleted successfully!")

    # ================= SEARCH =================
    elif choice == "4":
        search = input("Search (0 to go back): ")
        if search == "0":
            continue

        found = False
        for acc in accounts:
            if search.lower() in acc[0].lower():
                print_accounts([acc])
                found = True

        if not found:
            print("Not found!")

    # ================= EDIT (مع تحقق كامل) =================
    elif choice == "5":
        print_accounts(accounts)

        num = input("Enter account number (0 to go back): ")
        if num == "0":
            continue

        try:
            num = int(num)
        except ValueError:
            print("Invalid number!")
            continue

        if num < 1 or num > len(accounts):
            print("Invalid number!")
            continue

        #  تحقق الباسورد الحالي
        current = input("Enter current password: ")
        if hash_password(current) != accounts[num-1][2]:
            print("Wrong password!")
            continue

        new_username = input("New username (or 0 to skip): ")
        if new_username != "0":
            accounts[num-1][1] = new_username

        new_password = input("New password (or 0 to skip): ")
        if new_password == "0":
            save_accounts(current_user, accounts)
            continue

        confirm = input("Confirm password: ")

        if new_password != confirm:
            print("Passwords do not match!")
            continue

        accounts[num-1][2] = hash_password(new_password)

        save_accounts(current_user, accounts)
        print("Updated successfully!")

    # ================= EXIT =================
    elif choice == "6":
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() == "y":
            break

    else:
        print("Invalid choice!")(2)
