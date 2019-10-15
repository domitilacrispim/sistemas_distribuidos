from __future__ import print_function
import logging
import time

import grpc

import birdwiki_pb2
import birdwiki_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        while True:
            time.sleep(3)
            try:
                # TESTE 0: LISTA DE AVES
                response = stub.listBirds(birdwiki_pb2.BirdName(name='test0'))
                print("RECEBI DO SERVER ESTAS AVES: ")
                for bird in response:
                    print("Bird: ", bird.name)

                # TESTE 1: INFORMAÇÕES DE UMA AVE
                response = stub.showBird(birdwiki_pb2.BirdName(name='test1'))
                print("\nINFO DA AVE: ")
                print(response.name)
                print(response.text)

                # TESTE 2: """"SALVANDO"""" UMA AVE
                response = stub.saveBird(birdwiki_pb2.BirdPage(name="test2", text=""))
                print("\nIS SAVED? ", response.saved)

            except KeyboardInterrupt:
                print("Goodbye")
                channel.unsubscribe(close)
                exit()

def close(channel):
    channel.close()

if __name__ == '__main__':
    logging.basicConfig()
    run()
