import json
import os

FN = os.path.join(os.path.dirname(__file__), 'bird.txt')


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
        for bird in birdList:
            if (bird['name'] == name):
                return bird
        return None

    def getBirdFile(self, name):
        content = ""
        birdList = self.getBirds()
        bird = [b for b in birdList if b["name"] == name][0]

        with open(
            os.path.dirname(os.path.abspath(__file__)) + f"/files/{bird['name']}.txt", "r", encoding="utf-8"
        ) as file:
            content = file.read()
        
        return content
    
    def saveBirdFile(self, name, text):
        try:
            with open(
                os.path.dirname(os.path.abspath(__file__)) + f"/files/{name}.txt", "w", encoding="utf-8"
            ) as file:
                file.write(text)
                file.close()
                return True
        except:
            return False