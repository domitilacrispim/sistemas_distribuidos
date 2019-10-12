import json
import bcrypt


class User:
    def __init__(self, crBio, name, password):
        self.crBio = crBio
        self.name = name
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash)

    def addUserDb(self, db):
        userDict = {
            "crBio": self.crBio,
            "name": self.name,
            "password_hash": self.password_hash
        }

        db.addUser(userDict)
