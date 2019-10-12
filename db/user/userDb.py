import json


class UserDB:

    def getUsers(self):
        file = open("user.txt", "r")
        users = json.loads(file.read())['users']
        file.close()
        return users

    def writeUsers(self, userList):
        file = open("user.txt", "w")
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
        user = filter(lambda user: user.crBio == crbio, userList)
        return user
