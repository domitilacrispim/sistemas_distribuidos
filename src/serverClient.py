from __future__ import print_function

import grpc

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc

from env import NODE_QT, SERVER_QT


def birdHash(name):
    id = 0
    for c in name:
        id = id+(ord(c))*1661789
    return id % NODE_QT


def getServer(name, addrs):
    port = 5000 + birdHash(name)

    try:
        port = [candidate for candidate in addrs if candidate >= port][0]
    except:
        port = addrs[0]
    port = 5000
    return port


def getBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING GET BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.getBird(birdwiki_pb2.BirdName(name=name))
        return response


def createBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING CREATE BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.createBird(birdwiki_pb2.BirdName(name=name))
        return response


def readBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING READ BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.readBird(birdwiki_pb2.BirdName(name=name))
        return response


def editBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING READ BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.editBird(birdwiki_pb2.BirdName(name=name))
        return response


def saveBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING READ BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.saveBird(
            birdwiki_pb2.BirdPage(name=name, text=request.text))
        return response


def deleteBird(request, addrs):
    name = request.name
    port = getServer(name, addrs)

    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'DELEGATING READ BIRD {name} TO SERVER {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.deleteBird(birdwiki_pb2.BirdName(name=name))
        return response
