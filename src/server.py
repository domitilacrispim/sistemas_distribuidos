from concurrent import futures
import logging
import json
import grpc

from grpcFiles import birdwiki_pb2_grpc
from grpcFiles import loginuser_pb2_grpc
from grpcFiles import systemstate_pb2_grpc

from serverFiles.birdWiki import BirdWikiServer
from serverFiles.loginUser import LoginUserServer
from serverFiles.systemState import SystemStateServer


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
