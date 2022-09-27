from dataclasses import dataclass


class Keychain:
    def __init__(self, text, logo):
        self.text = text
        self.logo = logo


@dataclass
class User:
    surname: str
    name: str
    email: str
    company: str
    department: str
    phone: str
    role: str
    keychain: Keychain

    def __repr__(self):
        return "User()"

    def __str__(self):
        return f"member of User {self.surname}, {self.name}, {self.email}, {self.company}, {self.department}, {self.phone}, {self.role}"

    # @property
    # def keychain(self):
    #     return self.keychain
    #
    # @keychain.setter
    # def keychain(self, keychain):
    #     self.keychain = keychain
