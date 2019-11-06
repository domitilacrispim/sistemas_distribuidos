from concurrent import futures
import logging
import json
import grpc
import time
import threading

from grpcFiles import birdwiki_pb2_grpc
from grpcFiles import loginuser_pb2_grpc
from grpcFiles import systemstate_pb2_grpc

from serverFiles.birdWiki import BirdWikiServer
from serverFiles.loginUser import LoginUserServer
from serverFiles.systemState import SystemStateServer

class ServerState():

    def __init__ (self):
        self.clients = []

    def add_client(crBio, bird):
        self.clients.push((crBio, bird, time.time()))

def save_state_thread():
    print('Start')
    while True:
        time.sleep(5)
        with open("state.dat", "w+") as statefile:
            for client in state.clients:
                statefile.write(client)

state = ServerState()
print('StartA')
state_thread = threading.Thread(target = save_state_thread)
state_thread.start()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    birdwiki_pb2_grpc.add_BirdWikiServicer_to_server(BirdWikiServer(), server)
    loginuser_pb2_grpc.add_LoginUserServicer_to_server(
        LoginUserServer(), server)
    systemstate_pb2_grpc.add_SystemStateServicer_to_server(
        SystemStateServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
