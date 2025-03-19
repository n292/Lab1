import csv
import os
from security import text_security

class LoginUser:
    def __init__(self, email, password, role):
        self.email = email
        self.password = self.encrypt_password(password)
        self.role = role

    def to_list(self):
        return [self.email, self.password, self.role]

    @staticmethod
    def encrypt_password(password):
        return text_security.encrypt(password)

    @staticmethod
    def decrypt_password(encrypted_password):
        return text_security.decrypt(encrypted_password)

    @staticmethod
    def login(email, password):
        if not os.path.exists("login.csv"):
            return False
        with open("login.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                stored_email = row[0]
                stored_encrypted_password = row[1]
                decrypted = LoginUser.decrypt_password(stored_encrypted_password)
                if stored_email == email and decrypted == password:
                    return True
        return False

    @staticmethod
    def register_user(user):
        users = []
        if os.path.exists("login.csv"):
            with open("login.csv", "r") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    users.append(row[0])
        if user.email in users:
            print("User already exists!")
            return
        file_exists = os.path.exists("login.csv")
        with open("login.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists or os.path.getsize("login.csv") == 0:
                writer.writerow(["User_id", "Password", "Role"])
            writer.writerow(user.to_list())
        print("User registered successfully!")

def get_user_role(email):
    if not os.path.exists("login.csv"):
        return None
    with open("login.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0] == email:
                return row[2]
    return None
