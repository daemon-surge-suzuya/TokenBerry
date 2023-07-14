import getpass
import json
import os
import hashlib
import pyperclip

PASSWORD_FILE = "password.txt"
PAT_FILE = "pats.json"

def copy_token_to_clipboard():
    print("=====================================")
    try:
        with open(PASSWORD_FILE, "r") as password_file:
            password = password_file.read()
    except FileNotFoundError:
        print("Password file not found. Deleting 'pats.json' file...")
        delete_pats_file()
        return

    if not password:
        print("Password not set. Deleting 'pats.json' file...")
        delete_pats_file()
        return

    entered_password = getpass.getpass("Enter your password: ")
    try:
        with open(PAT_FILE, "r") as file:
            encrypted_data = json.load(file)
            decrypted_data = decrypt_data(encrypted_data, entered_password)
            if decrypted_data is None:
                return
    except FileNotFoundError:
        print("No PATs found.")
        return

    if not decrypted_data:
        print("No PATs found.")
        return

    token_name = input("Enter the name of the token you want to copy: ")
    token_password = None

    for pat in decrypted_data:
        if pat["name"] == token_name:
            token_password = pat["password"]
            break

    if token_password:
        pyperclip.copy(token_password)
        print(f"The token '{token_name}' has been copied to the clipboard.")
    else:
        print(f"No token found with the name '{token_name}'.")

def input_password():
    check = getpass.getpass("Enter your password: ").encode('utf-8')
    encoded_check = hashlib.sha256(check).hexdigest()
    with open(PASSWORD_FILE, "r") as password:
        x = password.read()
        if x != encoded_check:
            print("Wrong Password!")
            exit()

def set_password():
    if os.path.exists(PASSWORD_FILE):
        print("Password already set!")
        return
    password = getpass.getpass("Enter a password: ").encode('utf-8')
    confirm_password = getpass.getpass("Confirm password: ").encode('utf-8')

    if password != confirm_password:
        print("Passwords do not match!")
        return
    else:
        with open(PASSWORD_FILE, "w") as pas:
            encoded = hashlib.sha256(confirm_password).hexdigest()
            pas.write(encoded)

def encrypt_data(data, password):
    encoded_data = json.dumps(data).encode('utf-8')
    encoded_password = hashlib.sha256(password.encode('utf-8')).digest()
    cipher = hashlib.sha256(encoded_password).hexdigest()
    encrypted_data = bytearray()

    for i in range(len(encoded_data)):
        encrypted_data.append(encoded_data[i] ^ (i % 256))

    return {"cipher": cipher, "data": encrypted_data.hex()}

def decrypt_data(encrypted_data, password):
    encoded_password = hashlib.sha256(password.encode('utf-8')).digest()
    cipher = hashlib.sha256(encoded_password).hexdigest()

    if encrypted_data["cipher"] != cipher:
        print("Wrong Password!")
        return None

    encrypted_data = bytearray.fromhex(encrypted_data["data"])
    decrypted_data = bytearray()

    for i in range(len(encrypted_data)):
        decrypted_data.append(encrypted_data[i] ^ (i % 256))

    return json.loads(decrypted_data.decode('utf-8'))

def write_PAT():
    print("===================================")
    name = input("Enter the name of the PAT: ")
    token = getpass.getpass("Enter the PAT: ")
    password = getpass.getpass("Enter your password: ")

    try:
        with open(PAT_FILE, "r") as file:
            encrypted_data = json.load(file)
            decrypted_data = decrypt_data(encrypted_data, password)
            if decrypted_data is None:
                return
    except FileNotFoundError:
        decrypted_data = []

    decrypted_data.append({"name": name, "password": token})
    encrypted_data = encrypt_data(decrypted_data, password)

    with open(PAT_FILE, "w") as file:
        json.dump(encrypted_data, file)

def display_pats():
    print("=====================================")
    try:
        with open(PASSWORD_FILE, "r") as password_file:
            password = password_file.read()
    except FileNotFoundError:
        print("Password file not found. Deleting 'pats.json' file...")
        delete_pats_file()
        return

    if not password:
        print("Password not set. Deleting 'pats.json' file...")
        delete_pats_file()
        return

    entered_password = getpass.getpass("Enter your password: ")
    try:
        with open(PAT_FILE, "r") as file:
            encrypted_data = json.load(file)
            decrypted_data = decrypt_data(encrypted_data, entered_password)
            if decrypted_data is None:
                return
    except FileNotFoundError:
        print("No PATs found.")
        return

    if not decrypted_data:
        print("No PATs found.")
        return

    print("PAT List:")
    for pat in decrypted_data:
        print(f"{pat['name']}: ********")

def delete_PAT_by_name():
    print("=======================================")
    name = input("Enter the name of the PAT: ")
    entered_password = getpass.getpass("Enter your password: ")
    try:
        with open(PAT_FILE, "r") as file:
            encrypted_data = json.load(file)
            decrypted_data = decrypt_data(encrypted_data, entered_password)
            if decrypted_data is None:
                return
    except FileNotFoundError:
        print("No PATs found.")
        return

    # Find the PAT with the specified name
    found = False
    for pat in decrypted_data:
        if pat["name"] == name:
            decrypted_data.remove(pat)
            found = True
            break

    if not found:
        print(f"No PAT found with the name '{name}'.")
        return

    encrypted_data = encrypt_data(decrypted_data, entered_password)

    with open(PAT_FILE, "w") as file:
        json.dump(encrypted_data, file)

    print(f"PAT '{name}' deleted successfully.")

def delete_pats_file():
    if os.path.exists(PAT_FILE):
        os.remove(PAT_FILE)
        print(f"'{PAT_FILE}' file deleted.")

def main():
    if not os.path.exists(PASSWORD_FILE):
        set_password()

    input_password()

    if not os.path.exists(PASSWORD_FILE):
        print("Password file not found. Deleting 'pats.json' file...")
        delete_pats_file()

    while True:
            print("Berry PAT Manager")
            print("=====================")
            print("1. Create new PAT")
            print("2. Display PAT")
            print("3. Copy token to clipboard")
            print("4. Delete PAT")
            print("5. Exit")
            choice = input("Choice: ")

            if choice == '1':
                write_PAT()
            elif choice == '2':
                display_pats()
            elif choice == '3':
                copy_token_to_clipboard()
            elif choice == '4':
                delete_PAT_by_name()
            elif choice == '5':
                exit()
            else:
                print("Invalid choice. Please try again.")

main()
