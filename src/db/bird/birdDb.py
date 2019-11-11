import json
import os

FN = os.path.join(os.path.dirname(__file__), 'bird.txt')


class BirdDB:
    def getBirds(self):
        file = open(FN, "r")
        birds = json.loads(file.read())['birds']

        file.close()
        return birds

    def writeBirds(self, birdsDict):
        file = open(FN, "w")
        file.write(json.dumps({"birds": birdsDict}))
        file.close()
