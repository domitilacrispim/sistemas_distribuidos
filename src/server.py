from concurrent import futures
import logging

import grpc

import birdwiki_pb2
import birdwiki_pb2_grpc

BIRDSONS = [
    birdwiki_pb2.BirdInfo(name="Sabia", editing="false", editor=""),
    birdwiki_pb2.BirdInfo(name="Pica-pau", editing="false", editor=""),
    birdwiki_pb2.BirdInfo(name="Corvo", editing="false", editor="")
]

BIRDSON = birdwiki_pb2.BirdPage(name = "Corvo", text="Corvus is a widely distributed genus of medium-sized to large birds in the family Corvidae. The genus includes species commonly known as crows, ravens, rooks and jackdaws;")

CONF = birdwiki_pb2.Confirmation(saved = True)

class BirdWikiServer(birdwiki_pb2_grpc.BirdWikiServicer):

    def listBirds(self, request, context):
        print("REQUEST IS", request)
        for bird in BIRDSONS: # TODO: TROCAR BIRDSONS PARA DB
            yield bird

    def showBird(self, request, context):
        print("REQUEST IS", request)
        return BIRDSON

    def saveBird(self, request, context):
        print("REQUEST IS", request)
        return CONF


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    birdwiki_pb2_grpc.add_BirdWikiServicer_to_server(BirdWikiServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
