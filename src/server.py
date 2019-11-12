from concurrent import futures
import logging
import json
import grpc

from grpcFiles import birdwiki_pb2_grpc

from serverFiles.birdWiki import BirdWikiServer
from serverFiles.loginUser import LoginUserServer

from classes.serverState import endState


def serve():
    try:
        server_id = int(input("Server ID:"))
        server_port = 5000 + server_id

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        birdwiki_pb2_grpc.add_BirdWikiServicer_to_server(
            BirdWikiServer(server_id), server)
        birdwiki_pb2_grpc.add_LoginUserServicer_to_server(
            LoginUserServer(), server)

        server.add_insecure_port('[::]:' + str(server_port))
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        endState()
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
