import bcrypt

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc

from db.user.userDb import UserDB


class LoginUserServer(birdwiki_pb2_grpc.LoginUserServicer):

    def login(self, request, context):
        user = UserDB().getUser(request.crBio)

        if (user and user['crBio']):
            # verifica senha
            if bcrypt.checkpw(request.password.encode(), user['password_hash'].encode()):

                return birdwiki_pb2.UserInfo(
                    crBio=str(user['crBio']),
                    name=user['name'],
                    password_hash=user['password_hash'])

        return birdwiki_pb2.UserInfo()
