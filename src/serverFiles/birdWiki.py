from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc
from db.bird.birdDb import BirdDB


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

    def editBird(self, request, context):
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
