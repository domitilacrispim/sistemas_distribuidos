from concurrent import futures
import logging
import json
import grpc

import birdwiki_pb2
import birdwiki_pb2_grpc

import loginuser_pb2
import loginuser_pb2_grpc

import systemstate_pb2
import systemstate_pb2_grpc

from db.system_state.stateDb import StateDB
from db.user.userDb import UserDB
from db.bird.birdDb import BirdDB
import bcrypt


class BirdWikiServer(birdwiki_pb2_grpc.BirdWikiServicer):

    def listBirds(self, request, context):
        print("REQUEST IS TO LIST BIRD(S)", request)
        birdList = BirdDB().getBirds()
        for bird in birdList:
            yield birdwiki_pb2.BirdInfo(name=bird['name'], editing=bird['editing'], editor=bird['editor'])

    def getBird(self, request, context):
        print("REQUEST IS TO GET BIRD ", request.name)
        bird = BirdDB().getBird(request.name)

        if (bird and bird['name']):
            return birdwiki_pb2.BirdInfo(name=bird['name'], editing=bird['editing'], editor=bird['editor'])
        return birdwiki_pb2.BirdInfo()

    def readBird(self, request, context):
        print("REQUEST IS TO READ ", request.name)
        content = BirdDB().getBirdFile(request.name)
        if (content):
            return birdwiki_pb2.BirdPage(name=request.name, text=content)
        return birdwiki_pb2.BirdPage()

    def editBird (self, request, context):
        print("REQUEST IS TO EDIT ", request.name)
        changeEdit = BirdDB().updateBird(request.name, True)
        
        if (changeEdit == True): 
            content = BirdDB().getBirdFile(request.name)
            if (content):
                return birdwiki_pb2.BirdPage(name=request.name, text=content)
        return birdwiki_pb2.BirdPage()

    def saveBird(self, request, context):
        print("REQUEST IS TO SAVE ", request.name)
        changeEdit = BirdDB().updateBird(request.name, False)
        result = BirdDB().saveBirdFile(request.name, request.text)
        return birdwiki_pb2.Confirmation(saved=result)
    

class LoginUserServer(loginuser_pb2_grpc.LoginUserServicer):

    def login(self, request, context):
        user = UserDB().getUser(request.crBio)

        if (user and user['crBio']):
            # verifica senha
            if bcrypt.checkpw(request.password.encode(), user['password_hash'].encode()):

                return loginuser_pb2.UserInfo(
                    crBio=str(user['crBio']),
                    name=user['name'],
                    password_hash=user['password_hash'])

        return loginuser_pb2.UserInfo()

class SystemStateServer(systemstate_pb2_grpc.SystemStateServicer):
    def saveState(self, request, context):
       #TODO salvar estado no banco
       print("REQUEST IS TO SAVE STATE")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    birdwiki_pb2_grpc.add_BirdWikiServicer_to_server(BirdWikiServer(), server)
    loginuser_pb2_grpc.add_LoginUserServicer_to_server(LoginUserServer(), server)
    systemstate_pb2_grpc.add_SystemStateServicer_to_server(SystemStateServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
