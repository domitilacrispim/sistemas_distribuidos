import os
import grpc

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc
from db.bird.birdDb import BirdDB

from classes.serverState import saveBird, getBird, getBirds, createBird, updateBird, deleteBird, initDB, initState, createLog, createSnapshot
import serverClient as delegate
from env import NODE_QT, SERVER_QT

SERVER_ID = 0


def birdHash(name):
    id = 0
    for c in name:
        id = id+(ord(c))*1661789
    return id % NODE_QT


def checkServer(name):
    return birdHash(name) == SERVER_ID


def broadcast():
    list_neigh = []
    for i in range(NODE_QT):
        if i == SERVER_ID:
            continue
        port = 5000+i
        try:
            with grpc.insecure_channel('localhost:'+str(port)) as channel:
                stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
                response = stub.greeting(
                    birdwiki_pb2.ServerInfo(serverId=SERVER_ID))

                if (response.flag == True):
                    print("SERVER", port, "RESPONDED GREETING")
                    list_neigh.append(port)

                else:
                    raise Exception

        except Exception as e:
            print(f'Server witth port {port} not found.')

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

    def greeting(self, request, context):
        print("RECIVED GREETING FROM SERVER", request.serverId)
        self.neighbours.append(5000 + request.serverId)
        print(f'My neighbours: {self.neighbours}')
        return birdwiki_pb2.Confirmation(flag=True)

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
            return delegate.getBird(request, self.neighbours)

    def createBird(self, request, context):
        print("REQUEST IS TO CREATE BIRD ", request.name)
        if (checkServer(request.name)):
            bird = createBird(request.name)
            if (bird and bird['name']):
                return birdwiki_pb2.BirdInfo(name=bird['name'],
                                             editing=bird['editing'],
                                             text=bird['text'])
            return birdwiki_pb2.BirdInfo()
        else:
            return delegate.createBird(request, self.neighbours)

    def readBird(self, request, context):
        print("REQUEST IS TO READ ", request.name)
        if (checkServer(request.name)):
            content = getBird(request.name)["text"]
            if (content):
                return birdwiki_pb2.BirdPage(name=request.name, text=content)
            return birdwiki_pb2.BirdPage()
        else:
            return delegate.readBird(request, self.neighbours)

    def editBird(self, request, context):
        print("REQUEST IS TO EDIT ", request.name)
        changeEdit = updateBird(request.name, True)
        if (checkServer(request.name)):
            if (changeEdit == True):
                content = getBird(request.name)["text"]
                if (content):
                    return birdwiki_pb2.BirdPage(name=request.name, text=content)
            return birdwiki_pb2.BirdPage()
        else:
            return delegate.editBird(request, self.neighbours)

    def saveBird(self, request, context):
        print("REQUEST IS TO SAVE ", request.name)
        changeEdit = updateBird(request.name, False)
        if (checkServer(request.name)):
            result = saveBird(request.name, request.text)
            return birdwiki_pb2.Confirmation(flag=result)
        else:
            return delegate.saveBird(request, self.neighbours)

    def deleteBird(self, request, context):
        print("REQUEST IS TO DELETE ", request.name)
        if (checkServer(request.name)):
            result = deleteBird(request.name)
            return birdwiki_pb2.Confirmation(flag=result)
        else:
            return delegate.deleteBird(request, self.neighbours)
