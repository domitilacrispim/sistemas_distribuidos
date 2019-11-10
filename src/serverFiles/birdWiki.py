import os

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc
from db.bird.birdDb import BirdDB

from classes.serverState import saveBird, getBird, getBirds, updateBird, initDB, initState


class BirdWikiServer(birdwiki_pb2_grpc.BirdWikiServicer):

    def __init__(self):
        print('STARTING SERVER')
        files = os.listdir()

        try:
            files = [int(file.split('_')[1].split('.')[0]) for file in files if file.startswith('snapshot_')]
            id = max(files)           
            snapshot_file = 'snapshot_' + str(max(files)) + '.txt'
            initState(id + 1)
            initDB(snapshot_file)
        except:
            initState(0)
        

    def listBirds(self, request, context):
        print("REQUEST IS TO LIST BIRD(S)", request)
        birdList = getBirds()
        for bird in birdList:
            yield birdwiki_pb2.BirdInfo(name=bird['name'], editing=bird['editing'], editor=bird['editor'], text=bird['text'])


    def getBird(self, request, context):
        print("REQUEST IS TO GET BIRD ", request.name)
        bird = getBird(request.name)

        if (bird and bird['name']):
            return birdwiki_pb2.BirdInfo(name=bird['name'], editing=bird['editing'], editor=bird['editor'], text=bird['text'])
        return birdwiki_pb2.BirdInfo()

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
