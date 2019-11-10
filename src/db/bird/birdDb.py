import json
import os

FN = os.path.join(os.path.dirname(__file__), 'bird.txt')

# from classes.serverState import updateBird, getBird

class BirdDB:
    def getBirds(self):
        file = open(FN, "r")
        birds = json.loads(file.read())["birds"]
        file.close()
        return birds

    def writeBirds(self, birdList):
        file = open(FN, "w")
        file.write(json.dumps({"birds": birdList}))
        file.close()

