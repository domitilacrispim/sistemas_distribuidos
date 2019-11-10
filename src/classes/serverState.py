import time
import threading
import logging
import json
from db.bird.birdDb import BirdDB, FN

INTERVAL_MEMORY_TO_DB = 30
INTERVAL_DB_TO_SNAPSHOT= 60
SNAPSHOT_FILE = 'snapshot_{id}.txt'
LOG_FILE = 'log_{id}.txt'

logging.basicConfig(level=logging.DEBUG, filename='log_default.txt', filemode='w+')

class ServerState():

    def __init__ (self):
        self.birds = BirdDB().getBirds()

    def update_birds(self):
        print("COPYING DATA BASE TO MEMORY")
        self.birds = BirdDB().getBirds()

    
def save_state_thread():
    global state
    global running

    while running:
        try:
            time.sleep(INTERVAL_MEMORY_TO_DB)
            print("COPYING MEMORY DATA TO DATABASE")
            BirdDB().writeBirds(state.birds)
        except KeyboardInterrupt:
            break

def initState(idp):
    print("STARTING SERVER STATE TREAD")
    state_thread = threading.Thread(target = save_state_thread)
    state_thread.start()
    global id
    id = idp
    initSnapshot()

def endState():
    print("END STATE THREAD")
    global running
    running = False
    endSnapshot()

def saveBird(name, text):
    print('SAVING EDIT TO LOG')
    logging.debug('{"name": "' + name + '", "text": "' + text + '"},')
    global state
    try:
        bird = [b for b in state.birds if b["name"] == name][0]
        bird['text'] = text
        return True
    except:
        return False

def getBird(name):
    global state
    bird = [b for b in state.birds if b["name"] == name][0]
    return bird

def getBirds():
    global state
    return state.birds

def updateBird(name, editing):
    try:
        bird = [b for b in state.birds if b["name"] == name][0]
        bird["editing"] = editing
        return True
    except:
        return False

def saveSnapshot(id):
    
    global running
    while running:
        try:
            time.sleep(INTERVAL_DB_TO_SNAPSHOT)
            print("\n\nENTROU")
            file = open(FN, "r")
            birds = file.read()
            file.close()

            print('birds', birds)
            
            snapfile = SNAPSHOT_FILE.replace('{id}', str(id)) # fazer replace de id

            print('snapfile', snapfile)

            with open(snapfile, 'w+') as snapshot:
                print("CREATING SNAPSHOT N.", str(id))
                snapshot.write(birds)
                snapshot.close()
        
        except KeyboardInterrupt:
            break
        
        file_hander = logging.FileHandler(LOG_FILE.replace('{id}', str(id)), 'w+')
        log = logging.getLogger()
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(file_hander)

        print("CREATING LOG N.", str(id))
        logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE.replace('{id}', str(id)), filemode='w+')

        id += 1

def initSnapshot():
    print("STARTING SNAPSHOT THREAD")
    state_thread = threading.Thread(target = saveSnapshot, args = (id,))
    state_thread.start()

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

def endSnapshot():
    print("END SNAPSHOT THREAD")
    global running
    running = False

def executeLog():
    global id
    global state
    print("EXECUTING LOG", str(id-1))

    try: 
        file = open(LOG_FILE.replace('{id}', str(id - 1)), "r")
        content = file.read()
        print('content', content)
        file.close()

        edit_log = content.split(',\n')

        for log in edit_log:
            try:
                log_dict = json.loads(log)
                bird = [b for b in state.birds if b["name"] == log_dict['name']][0]
                bird['text'] = log_dict['text']
            except:
                pass
        
        print("SAVING LOG RESULT IN DATABASE")
        BirdDB().writeBirds(state.birds)
    except:
        print("LOG NOT SUCCESSFUL")
        pass


id = 0
state = ServerState()
running = True