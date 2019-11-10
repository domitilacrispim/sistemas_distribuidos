from concurrent import futures
import logging
import json
import grpc

from grpcFiles import birdwiki_pb2_grpc
from grpcFiles import loginuser_pb2_grpc

from serverFiles.birdWiki import BirdWikiServer
from serverFiles.loginUser import LoginUserServer

from classes.serverState import endState


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        birdwiki_pb2_grpc.add_BirdWikiServicer_to_server(BirdWikiServer(), server)
        loginuser_pb2_grpc.add_LoginUserServicer_to_server(LoginUserServer(), server)
    
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        endState()
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
