import json
import os


class BirdDB:
    def getBirds(self):
        file = open(os.path.dirname(os.path.abspath(__file__)) + "/bird.txt", "r")
        birds = json.loads(file.read())["birds"]
        file.close()
        return birds

    def writeBirds(self, birdList):
        file = open("bird.txt", "w")
        file.write(json.dumps({"birds": birdList}))
        file.close()

    def addBird(self, bird):
        findBird = self.getBird(bird["name"])

        if not findBird:
            birdList = self.getBirds()
            birdList.append(bird)
            self.writeBirds(birdList)

        file = open(f"./files/{bird['name']}.txt", "w+")
        return file

    def getBird(self, name):
        birdList = self.getBirds()
        bird = filter(lambda bird: bird.name == name, birdList)
        return bird

    def getBirdFile(self, name):
        content = ""
        birdList = self.getBirds()
        print(birdList)
        bird = [b for b in birdList if b["name"] == name][0]
        print(bird, os.path.dirname(os.path.abspath(__file__)) + f"/files/{bird['name']}.txt")
        with open(
            os.path.dirname(os.path.abspath(__file__)) + f"/files/{bird['name']}.txt", "r"
        ) as file:
            content = file.read()
        return content
