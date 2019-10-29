import json
import os

FN = os.path.join(os.path.dirname(__file__), 'user.txt')


class UserDB:

    def getUsers(self):
        file = open(FN, "r")
        users = json.loads(file.read())['users']
        file.close()
        return users

    def writeUsers(self, userList):
        file = open(FN, "w")
        file.write(json.dumps({"users": userList}))
        file.close()

    def addUser(self, user):
        findUser = self.getUser(user['crBio'])

        if (findUser):
            return False

        userList = self.getUsers()
        userList.append(user)
        self.writeUsers(userList)

        return True

    def getUser(self, crBio):
        userList = self.getUsers()
        for user in userList:
            if (user['crBio'] == int(crBio)):
                return user
        return None
