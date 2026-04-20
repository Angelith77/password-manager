import hashlib
import os

MASTER_FILE = "master.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def master_menu():
    while True:
        print("\n1. New user")
        print("2. Existing user")
        print("0. Exit")

        choice = input("Choose: ")

        #  خروج
        if choice == "0":
            print("Goodbye!")
            exit()

        #  مستخدم جديد
        elif choice == "1":
            if os.path.exists(MASTER_FILE):
                print("Master password already exists!")
                continue

            while True:
                new_pass = input("Enter new master password (or 0 to go back): ")
                if new_pass == "0":
                    break

                confirm = input("Confirm password: ")

                if new_pass != confirm:
                    print("Passwords do not match!")
                    continue

                with open(MASTER_FILE, "w") as file:
                    file.write(hash_password(new_pass))

                print("Master password created successfully!")
                return  # يدخل البرنامج

        #  مستخدم قديم
        elif choice == "2":
            if not os.path.exists(MASTER_FILE):
                print("No master password found! Please register first.")
                continue

            while True:
                entered = input("Enter master password (or 0 to go back): ")

                if entered == "0":
                    break

                with open(MASTER_FILE, "r") as file:
                    saved = file.read()

                if hash_password(entered) == saved:
                    print("Access granted!")
                    return  # يدخل البرنامج
                else:
                    print("Wrong password!")

        else:
            print("Invalid choice!")

def print_accounts(accounts):
	print("Your accounts: ")
	for i,acc in enumerate(accounts,1):
		hidden_password = "*" * len(acc[2])
		print(i,"|",acc[0],"|", acc[1],"|",hidden_password)
	print("--------------------------")



def save_accounts(accounts):
	with open("password.txt","w") as file:
		for acc in accounts:
			file.write(acc[0] +"," + acc[1] +"," + acc[2]  +  "\n")
def load_passwords():
	accounts = []
	try:
		with open("password.txt","r") as file:
			for line in file:
				data = line.strip().split(",")
				accounts.append(data)
	except FileNotFoundError:
		pass
	return accounts
master_menu()
accounts=load_passwords()
while True:

	print("1.Add account")
	print("2.Show accounts ")
	print("3.Delete account")
	print("4.Search account")
	print("5.Edit account")
	print("6.exit")
	print("----------------------")
	try:
		choice = int(input("choose number: "))
	except ValueError:
		print("please enter a valid number!")
		continue
	if choice == 1:
		while True:

			website=input("enter website: (or 0 to go back) ")
			if website == "0":
				break
			username=input("enter username: (or 0 to go back)")
			if username == "0":
				break
			password=input("enter password: (or 0 to go back)")
			if password == "0":
				break
			accounts.append([website,username,password])
			print("Account added successfully!")
			save_accounts(accounts)
			print_accounts(accounts)
			break
	elif choice == 2:
		while True:
			if len(accounts) == 0:
				print("no accounts !")
				break
			print_accounts(accounts)
			input("Press Enter to return to main menu...")

			break

	elif choice == 3:
		while True:
			if len(accounts) == 0:
				print("no accounts !")
				break
			print_accounts(accounts)
			input_number=input("choose the account number you want to delete:(or 0 to go back) ")
			if input_number == "0":
				break

			try:
				number = int(input_number)
			except ValueError:
				print("please enter a valid number!")
				continue

			if number <1 or number > len(accounts):
				print("please enter a valid number!")
				continue

			accounts.pop(number-1)
			print("the account deleted successfully!")
			print_accounts(accounts)
			save_accounts(accounts)
			break

	elif choice == 4:
		while True:
			search=input("What is the account you want to search about ? (or 0 to go back):")
			found = False
			if search == "0":
				break
			for acc in accounts :
				if acc[0]== search:
					print_accounts([acc])
					found= True
					break
			if not found:
				print("account not found!")
			print("------------------------")
			break
	elif choice == 5:
		while True:
			print_accounts(accounts)
			edit=input("enter the account number you want to change: (or 0 to go back) :")
			if edit=="0":
				break
			try:
				number = int(edit)
			except ValueError:
				print("please enter a valid number!")
				continue
			if number < 1 or number > len(accounts):
				print("Invalid number!")
				continue
			new_username=input("input your new username:(press 0 if you don't want to change the username)")
			if new_username != "0":
				accounts[number - 1][1] = new_username
			change_pass = input("Do you want to change the password? (y/n): ")

			if change_pass.lower() == "y":
				while True:
					current=input("Enter your current password:")
					if current != accounts[number-1][2]:
						print("Wrong password!")
						continue
					new_password=input("Enter your new password:")
					confirm_password=input("Re-Enter your new password:")

					if new_password != confirm_password:
						print("Passwords do not match!")
						continue


					accounts[number-1][2] = new_password


					print("account edited successfully!")
					break
			save_accounts(accounts)
			print_accounts(accounts)

			break


	elif choice == 6:
		option = input("Are you sure you want to exit? (y/n): ")
		if option.lower() == "y":
			print("Thank you, you're logged out.")
			break
		elif option.lower() == "n":
			continue
		else:
			print("Invalid option, returning to main menu.")
			continue

	else:
		print("Please choose a valid option from 1 to 6.")

