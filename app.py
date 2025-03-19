import os
import argparse

from entities.entities import Client, Contact, Representative


class App:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        args = parser.parse_args()

        if args.debug:
            print("Debug Mode ON\n")
            self.path = os.environ.get("FILE_PATH")
            self.path = "."
            self.consecutive_path = f"{self.path}/data/consecutivo.txt"
        else:
            self.path = os.environ.get("COTIZACIONES_PATH")
            self.consecutive_path = f"{self.path}/Z consecutivo.txt"

        self.user_path = f"{self.path}/data"
        self.footer_path = f"{self.path}/data/data.txt"

    def prompt(self):
        self.users = self.get_users()
        self.client = input("Ingrese nombre cliente: ").title()
        self.company = input("Ingrese nombre empresa: ").upper()
        self.user = input(f"Ingrese nombre asesor ({', '.join(self.users)}): ").lower()
        self.references = (
            input("Ingrese referencias a consultar (separadas por coma): ")
            .upper()
            .split(",")
        )

    def get_references(self):
        return self.references

    def get_client(self) -> Client:
        return {"company": self.company, "name": self.client}

    def get_users(self):
        users = []
        exclude = ["consecutivo", "data"]
        for x in os.listdir(self.user_path):
            if x.endswith(".txt"):
                user = x.split(".txt")[0]
                if user not in exclude:
                    users.append(user)

        return users

    def get_consecutive(self) -> int:
        file = open(self.consecutive_path, "r")
        consecutive = file.readline().strip()
        file.close()
        return int(consecutive)

    def get_contact_info(self) -> Representative:
        file = open(f"{self.user_path}/{self.user}.txt", "r")
        rep_name = file.readline()
        phone = file.readline()
        email = file.readline()
        file.close()

        return {"name": rep_name, "phone": phone, "email": email}

    def get_footer(self) -> Contact:
        file = open(self.footer_path, "r")
        address = file.readline()
        web = file.readline()
        file.close()

        representative = self.get_contact_info()

        return {
            "address": address,
            "web": web,
            "phone": representative["phone"],
            "email": representative["email"],
        }

    def create_new_consecutive(self):
        curr_consecutive = self.get_consecutive()
        new_consecutive = curr_consecutive + 1
        file = open(self.consecutive_path, "w")
        file.write(f"{new_consecutive}\n")
        file.close()
