import argparse
import os

from app_utils import str2bool
from entities.entities import Client, Contact, Representative


class App:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        parser.add_argument("--test", action="store_true", help="Enable test mode")
        parser.add_argument(
            "-H",
            "--headless",
            type=str2bool,
            default=True,
            help="Run in headless mode (true/false)",
        )
        self.args = parser.parse_args()
        self.path = os.environ.get("COTIZACIONES_PATH")
        self.user_path = f"{self.path}/data"
        self.footer_path = f"{self.path}/data/data.txt"

        if self.args.debug:
            print("Debug Mode ON\n")
            self.consecutive_path = f"{self.path}/data/consecutivo.txt"
        else:
            self.consecutive_path = f"{self.path}/Z consecutivo.txt"

    def prompt(self):
        if self.args.debug or self.args.test:
            self.client = "test"
            self.company = "test"
            self.user = "sergio"
        else:
            self.users = self.get_users()
            self.client = input("Ingrese nombre cliente: ").title()
            self.company = input("Ingrese nombre empresa: ").upper()
            self.user = input(
                f"Ingrese nombre asesor ({', '.join(self.users)}): "
            ).lower()

        self.references = (
            input("Ingrese referencias a consultar (separadas por coma): ")
            .upper()
            .split(",")
        )

    def get_saving_path(self):
        if self.args.debug:
            return "./cotizaciones/cotización_TEST.pptm"

        if self.args.test:
            return f"{self.path}/z-test-borrar.pptm"

        return f"{self.path}/Cotización N°{self.get_consecutive()} - {self.company} - Magic Medios SAS.pptm"

    def get_references(self):
        return [ref.strip() for ref in self.references]

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

    def get_consecutive(self) -> int:
        file = open(self.consecutive_path, "r")
        consecutive = file.readline().strip()
        file.close()
        return int(consecutive)

    def create_new_consecutive(self):
        if not self.args.test:
            curr_consecutive = self.get_consecutive()
            new_consecutive = curr_consecutive + 1
            file = open(self.consecutive_path, "w")
            file.write(f"{new_consecutive}\n")
            file.close()
