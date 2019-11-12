from __future__ import print_function
import logging
import time

import grpc

from grpcFiles import birdwiki_pb2
from grpcFiles import birdwiki_pb2_grpc

from classes.editor import EditorWindow

user = ''

# EFETUA LOGIN DE USUARIO
# FICA EM LOOP ENQUANTO LOGIN FALHA (nome ou senha incorretos)
# TODO (baixa prioridade): OPÇÂO DE SAIR


def login(stub):
    print("\n --- LOGIN ---")
    global user

    while(True):
        crBio = input("crBio: ")
        password = input("Senha: ")

        response = stub.login(birdwiki_pb2.UserLogin(
            crBio=crBio, password=password))

        if not response.crBio:
            print("Usuário ou senha incorretos. Tente Novamente\n\n")
        else:
            user = response.crBio
            print("Usuário ", response.name, " logado com sucesso.")
            break

# LISTAGEM E ESCOLHA DE AVE
# FICA EM LOOP ENQUANTO NOME INFORMADO FOR INVALIDO


def chooseBird(stub):
    print("\n --- ESCOLHA UMA AVE ---")

    while True:
        # PEDE AVES PARA SERVIDOR
        response = stub.listBirds(birdwiki_pb2.BirdName())

        print("\nAves disponíveis: ")  # EXIBE AVES
        for bird in response:
            print(bird.name)

        # USUARIO ESCOLHE AVE
        birdName = input("Escolha uma ave ou digite 0 para sair: ")
        if(birdName == "0"):
            raise KeyboardInterrupt
        response = stub.getBird(birdwiki_pb2.BirdName(
            name=birdName))  # PEDE AVE AO SERVIDOR

        if not response.name:  # NOME DE AVE INVÁLIDO
            print("Ave inválida. Tente Novamente\n")
        else:
            return response  # RETORNA AVE ESCOLHIDA


# VERIFICA DISPONIBILIDADE DE EDITAR AVE
# EXIBE MENU DE OPÇÔES (ler, escolher outra ou sair) CASO AVE EM EDICAO
def checkBirdAvailability(stub, bird):
    if bird.editing == True:
        print("\nPássaro já está sendo editado.")
        print(
            "\nEscolha uma das opcoes: \n[1] Abrir para leitura \n[2] Escolher outra ave \n[0] Sair")
        option = int(input())

        if option == 1:
            readBird(stub, bird)

        if option == 0:
            raise KeyboardInterrupt

    else:
        editBird(stub, bird)


# LER DADOS DE UMA AVE
def readBird(stub, bird):
    response = stub.readBird(
        birdwiki_pb2.BirdName(name=bird.name))
    EditorWindow(response.name, response.text, False).run()

# EDITAR DADOS DE UMA AVE
# TODO: REQUISITAR AO BANCO A EDIÇÂO DA AVE


def editBird(stub, bird):
    response = stub.editBird(
        birdwiki_pb2.BirdName(name=bird.name))
    editor = EditorWindow(response.name, response.text, True)
    editor.run()
    response = stub.saveBird(
        birdwiki_pb2.BirdPage(name=bird.name, text=editor.content)
    )
    print(response.saved)


def run():
    with grpc.insecure_channel('localhost:5006') as channel:
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        login(birdwiki_pb2_grpc.LoginUserStub(channel))

        while True:
            try:

                bird = chooseBird(stub)  # LISTA AS AVES E ESCOLHE UMA
                print(
                    "Escolha uma das opcoes: \n[1] Abrir para leitura \n[2] Editar \n[0] Sair")
                option = int(input())
                if(option == 2):
                    # VERIFICA SE PODE EDITAR AVE ESCOLHIDA
                    checkBirdAvailability(stub, bird)
                elif(option == 1):
                    readBird(stub, bird)
                else:
                    raise KeyboardInterrupt

            except KeyboardInterrupt:
                print("Goodbye")
                channel.unsubscribe(close)
                exit()


def close(channel):
    channel.close()


if __name__ == '__main__':
    logging.basicConfig()
    run()
