import os
import grpc

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc
from db.bird.birdDb import BirdDB

from classes.serverState import saveBird, getBird, getBirds, updateBird, initDB, initState, createLog, createSnapshot

NODE_QT = 8
SERVER_QT = 3
SERVER_ID = 0


def birdHash(name):
    id = 0
    for c in name:
        id = id+(ord(c))*1661789
    return id % NODE_QT


def checkServer(name):
    return birdHash(name) == SERVER_ID


def get_server_request(name, addrs):
    port = 5000 + birdHash(name)
    print(f'Delegating {addrs}, {name}, {port}')

    try:
        port = [candidate for candidate in addrs if candidate >= port][0]
    except:
        port = addrs[0]
    port = 5000
    with grpc.insecure_channel('localhost:'+str(port)) as channel:
        print(f'Not my problem, calling neighbour {port}')
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        response = stub.readBird(birdwiki_pb2.BirdName(name=name))
        return response


def broadcast():
    list_neigh = []
    global SERVER_ID
    for i in range(NODE_QT):
        if i == SERVER_ID:
            continue
        port = 5000+i
        try:
            with grpc.insecure_channel('localhost:'+str(port)) as channel:
                stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
                response = stub.listBirds(birdwiki_pb2.BirdName())
                print(response)
                for _ in response:
                    pass
                list_neigh.append(port)
        except Exception as e:
            print(f'Server witth port {port} not found. Reason: {e}')

    print(f'My neighbours: {list_neigh}')
    return list_neigh


class BirdWikiServer(birdwiki_pb2_grpc.BirdWikiServicer):

    def __init__(self, server_id):
        print('STARTING SERVER')
        files = os.listdir()
        global SERVER_ID
        SERVER_ID = server_id
        self.neighbours = broadcast()

        try:
            files = [int(file.split('_')[1].split('.')[0])
                     for file in files if file.startswith('snapshot_')]
            id = max(files)
            snapshot_file = 'snapshot_' + str(max(files)) + '.txt'
            initState(id + 1)
            initDB(snapshot_file)
        except:
            createLog(0)
            createSnapshot(0)
            initState(0)

    def listBirds(self, request, context):
        print("REQUEST IS TO LIST BIRD(S)", request)
        birdList = getBirds()
        for birdKey in birdList:
            bird = birdList[birdKey]
            yield birdwiki_pb2.BirdInfo(name=bird['name'],
                                           editing=bird['editing'],
                                           text=bird['text'])

    def getBird(self, request, context):
        print("REQUEST IS TO GET BIRD ", request.name)
        if (checkServer(request.name)):
            bird = getBird(request.name)
            if (bird and bird['name']):
                return birdwiki_pb2.BirdInfo(name=bird['name'],
                                                editing=bird['editing'],
                                                text=bird['text'])
            return birdwiki_pb2.BirdInfo()
        else:
            return get_server_request(request.name, self.neighbours)

    def readBird(self, request, context):
        print("REQUEST IS TO READ ", request.name)
        content = getBird(request.name)["text"]
        if (content):
            return birdwiki_pb2.BirdPage(name=request.name, text=content)
        return birdwiki_pb2.BirdPage()

    def editBird(self, request, context):
        print("REQUEST IS TO EDIT ", request.name)
        changeEdit = updateBird(request.name, True)

        if (changeEdit == True):
            content = getBird(request.name)["text"]
            if (content):
                return birdwiki_pb2.BirdPage(name=request.name, text=content)
        return birdwiki_pb2.BirdPage()

    def saveBird(self, request, context):
        print("REQUEST IS TO SAVE ", request.name)
        changeEdit = updateBird(request.name, False)
        result = saveBird(request.name, request.text)
        return birdwiki_pb2.Confirmation(saved=result)
