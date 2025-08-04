import argparse
import os
import time

from app_utils import str2bool
from entities.entities import Client, Contact, Representative
from lock_file import lock_file, unlock_file
from log import logger

MAX_RETRIES = 20
DELAY_SECONDS = 1


class App:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        parser.add_argument("--test", action="store_true", help="Enable test mode")
        parser.add_argument(
            "-l",
            "--load_test",
            type=int,
            default=None,
            help="Loop scrapper and log result",
        )
        parser.add_argument(
            "-c", "--concurrent_tasks", type=int, default=3, help="Max concurrent tasks"
        )
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

        self.lock_path = f"{self.consecutive_path}.lock"

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
        logger.info(f"cotizacion: {self.references}")

    def prompt_not_found(self, not_found: list[str]) -> bool:
        retry = (
            input(
                f"Las siguientes referencias no pudieron ser extraidas {not_found}\nDesea intentar extraerlas nuevamente? [S/N]: "
            )
            .strip()
            .lower()
        )

        if retry == "s":
            return True
        else:
            return False

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
        wait_attempts = 20
        delay = 0.5

        for i in range(wait_attempts):
            if not os.path.exists(self.lock_path):
                break
            print(f"⏳ Leyendo consecutivo... ({i + 1}/{wait_attempts})")
            time.sleep(delay)
        else:
            raise TimeoutError("Could not read: lock held too long")

        if not os.path.exists(self.consecutive_path):
            return 0

        with open(self.consecutive_path, "r") as f:
            return int(f.read().strip() or 0)

    def acquire_drive_lock(self, lock_path):
        for attempt in range(MAX_RETRIES):
            try:
                fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return True
            except FileExistsError:
                print(f"⚠️ Guardando consecutivo ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(DELAY_SECONDS)
        return False

    def release_drive_lock(self, lock_path):
        if os.path.exists(lock_path):
            os.remove(lock_path)

    def increment_consecutive(self):
        if not self.acquire_drive_lock(self.lock_path):
            raise TimeoutError("Could not acquire lock after several retries.")

        try:
            if not os.path.exists(self.consecutive_path):
                with open(self.consecutive_path, "w") as f:
                    f.write("0\n")

            with open(self.consecutive_path, "r+") as f:
                lock_file(f)  # cross-platform file lock (in-process safety)
                try:
                    current = int(f.read().strip() or 0)
                    next_val = current + 1
                    f.seek(0)
                    f.truncate()
                    f.write(f"{next_val}\n")
                    f.flush()
                finally:
                    unlock_file(f)
        finally:
            self.release_drive_lock(self.lock_path)
