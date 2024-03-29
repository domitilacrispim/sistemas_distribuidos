import time
import threading
import logging
import json
import os
from db.bird.birdDb import BirdDB, FN
from utils.crudEnum import CrudEnum
from env import INTERVAL_MEMORY_TO_DB, INTERVAL_DB_TO_SNAPSHOT


SNAPSHOT_FILE = 'snapshot_{id}.txt'
LOG_FILE = 'log_{id}.txt'

logging.basicConfig(level=logging.DEBUG,
                    filename='log_default.txt', filemode='w+')


class ServerState():

    def __init__(self):
        self.birds = BirdDB().getBirds()

    def update_birds(self):
        print("COPYING DATA BASE TO MEMORY")
        self.birds = BirdDB().getBirds()

# STATE FUNCS


def save_state_thread():
    global state
    global running

    while running:
        try:
            time.sleep(INTERVAL_MEMORY_TO_DB)
            if (running):
                print("COPYING MEMORY DATA TO DATABASE")
                BirdDB().writeBirds(state.birds)
        except KeyboardInterrupt:
            break


def initState(idp):
    print("STARTING SERVER STATE TREAD")
    state_thread = threading.Thread(target=save_state_thread)
    state_thread.start()
    global id
    id = idp
    initSnapshot()


def endState():
    print("END STATE THREAD")
    global running
    running = False
    endSnapshot()


# BIRD FUNCS
def getBirds():
    global state
    return state.birds


def getBird(name):
    try:
        global state
        bird = state.birds[name]
        return bird
    except:
        return None


def createBird(name):
    try:
        global state
        bird = {
            "name": name,
            "text": "",
            "editing": False
        }
        state.birds[name] = bird

        print('SAVING CREATE TO LOG')
        logging.debug('{"op": "' + CrudEnum.CREATE.name + '", "name": "' +
                      name + '", "text": ""},')
        return bird
    except:
        return None


def updateBird(name, editing):
    try:
        bird = state.birds[name]
        bird["editing"] = editing
        return True
    except:
        return False


def saveBird(name, text):
    print('SAVING EDIT TO LOG')
    logging.debug('{"op": "' + CrudEnum.UPDATE.name + '", "name": "' +
                  name + '", "text": "' + text + '"},')
    global state
    try:
        bird = state.birds[name]
        bird['text'] = text
        return True
    except:
        return False


def deleteBird(name):
    try:
        global state
        state.birds.pop(name)

        print('SAVING DELETE TO LOG')
        logging.debug('{"op": "' + CrudEnum.DELETE.name + '", "name": "' +
                      name + '", "text": ""},')
        return True
    except:
        return False


# SNAPSHOT FUNCS
def saveSnapshot(id):

    global running
    while running:
        try:
            time.sleep(INTERVAL_DB_TO_SNAPSHOT)
            if (running):
                createSnapshot(id)

        except KeyboardInterrupt:
            break

        if (running):
            createLog(id)
            id += 1


def createSnapshot(id):
    file = open(FN, "r")
    birds = file.read()
    file.close()
    snapfile = SNAPSHOT_FILE.replace('{id}', str(id))  # fazer replace de id

    with open(snapfile, 'w+') as snapshot:
        print("CREATING SNAPSHOT N.", str(id))
        snapshot.write(birds)
        snapshot.close()

    deleteSnapshot(id)


def deleteSnapshot(id):
    if id > 2:
        try:
            print("DELETING SNAPSHOT", str(id - 3))
            os.remove(SNAPSHOT_FILE.replace('{id}', str(id - 3)))
        except:
            pass


def initSnapshot():
    print("STARTING SNAPSHOT THREAD")
    state_thread = threading.Thread(target=saveSnapshot, args=(id,))
    state_thread.start()


def endSnapshot():
    print("END SNAPSHOT THREAD")
    global running
    running = False


# DB FUNCS
def initDB(filename):
    print("LOADING ", filename, "INTO DATABASE")
    file = open(filename, "r")
    content = file.read()
    file.close()

    db = open(FN, 'w+')
    db.write(content)
    db.close()

    global state
    state.update_birds()
    executeLog()


# LOG FUNCS
def createLog(id):
    file_hander = logging.FileHandler(LOG_FILE.replace('{id}', str(id)), 'w+')

    log = logging.getLogger()
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(file_hander)

    print("CREATING LOG N.", str(id))
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE.replace(
        '{id}', str(id)), filemode='w+')

    deleteLog(id)


def deleteLog(id):
    if id > 2:
        try:
            print("DELETING LOG", str(id - 3))
            os.remove(LOG_FILE.replace('{id}', str(id - 3)))
        except:
            pass


def executeLog():
    global id
    global state
    print("EXECUTING LOG", str(id-1))

    try:
        file = open(LOG_FILE.replace('{id}', str(id - 1)), "r")
        content = file.read()
        file.close()

        edit_log = content.split(',\n')

        for log in edit_log:
            try:
                log_dict = json.loads(log)
                op = log_dict['op']
                birdName = log_dict['name']
                birdText = log_dict['text']

                if (op == CrudEnum.UPDATE.name):
                    bird = state.birds[birdName]
                    bird['text'] = log_dict['text']

                elif (op == CrudEnum.CREATE.name):
                    createBird(birdName)

                elif (op == CrudEnum.DELETE.name):
                    deleteBird(birdName)
            except:
                pass

        print("SAVING LOG RESULT IN DATABASE")
        BirdDB().writeBirds(state.birds)
        createSnapshot(id)
        createLog(id)
        id += 1

    except:
        print("LOG NOT SUCCESSFUL")
        pass


id = 0
state = ServerState()
running = True
