import json
import secrets
from cryptography.fernet import Fernet, InvalidToken
import os


def main():
    manager = PasswordManager()

    while True:
        clear_screen()
        print("Sites:", ", ".join(site for site in manager.passwords))
        print("1. Add Password")
        print("2. Get Password")
        print("3. Remove Password")
        print("4. Save & Quit")

        choice = input("Select a Function: ")

        if choice == "1":
            account = input("Site: ")
            print(manager.add(account))
        elif choice == "2":
            account = input("Site: ")
            print(manager.get(account))
        elif choice == "3":
            account = input("Site: ")
            print(manager.remove(account))
        elif choice == "4":
            data = encrypt(manager.passwords)
            save_data(data)
            break
        else:
            print("Please enter a correct number")

        input("Press enter to continue")


class PasswordManager:
    def __init__(self):
        data = load_data()
        self.passwords = decrypt(data) if data else {}

    def add(self, account):
        if account in self.passwords:
            return f"{account} already exists."
        self.passwords[account] = generate_password()
        return f"{account} is added"

    def get(self, account):
        if account in self.passwords:
            return self.passwords[account]
        return f"{account} not found."

    def remove(self, account):
        if account in self.passwords:
            if input("Sure to delete? (yes/no) ").lower() == "yes":
                del self.passwords[account]
                return f"{account} is removed"
            return "Operation is canceled"
        return f"{account} not found"


def generate_password():
    return secrets.token_urlsafe(12)


def save_data(data, file_name="passwords.txt"):
    with open(file_name, "wb") as file:
        file.write(data)


def load_data(file_name="passwords.txt"):
    try:
        with open(file_name, "rb") as file:
            data = file.read()
        return data if data else {}
    except FileNotFoundError:
        return {}


def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as file:
        file.write(key)


def get_key():
    try:
        with open("key.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        generate_key()
        return get_key()


def encrypt(data):
    key = get_key()
    fernet = Fernet(key)
    encode = json.dumps(data).encode()
    encrypted = fernet.encrypt(encode)
    return encrypted


def decrypt(data):
    try:
        key = get_key()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
        decode = json.loads(decrypted.decode())
        return decode
    except InvalidToken:
        return {}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()
