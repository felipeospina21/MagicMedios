class User:
    def __init__(self, path):
        self.path = path

    def create(self, name, phone, email):
        try:
            with open(f"{self.path}/{name}.txt", "w") as f:
                f.write(name)
                f.write(phone)
                f.write(email)
        except FileNotFoundError:
            print("No se encuentra la ruta")
