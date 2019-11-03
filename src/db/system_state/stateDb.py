import json
import os

FN = os.path.join(os.path.dirname(__file__), 'state.txt')


class StateDB:

    def getStates(self):
        file = open(FN, "r")
        states = json.loads(file.read())['states']
        file.close()
        return states

    def writeStates(self, stateList):
        file = open(FN, "w")
        file.write(json.dumps({"states": stateList}))
        file.close()

    def addstate(self, state):
        findstate = self.getstate(state['crBio'])

        if (findstate):
            return False

        stateList = self.getstates()
        stateList.append(state)
        self.writestates(stateList)

        return True

    def getstate(self, crBio):
        stateList = self.getstates()
        for state in stateList:
            if (state['crBio'] == int(crBio)):
                return state
        return None