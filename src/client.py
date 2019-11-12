from __future__ import print_function
import logging
import time

import sys
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
        # USUARIO ESCOLHE AVE
        birdName = sys.argv[1]
        if(birdName == "0"):
            raise KeyboardInterrupt
        response = stub.getBird(birdwiki_pb2.BirdName(
            name=birdName))  # PEDE AVE AO SERVIDOR

        if not response.name:  # NOME DE AVE INVÁLIDO
            print(
                f'Ave inexistente! \nEscolha uma das opcoes: \n[1] Criar ave "{birdName}" \n[2] Escolher outra ave \n[0] Sair')
            option = int(sys.argv[2])

            if (option == 0):
                raise KeyboardInterrupt
            if (option == 1):
                response = createBird(stub, birdName)
                if response.name:
                    return response
        else:
            return response  # RETORNA AVE ESCOLHIDA


def createBird(stub, birdName):
    response = stub.createBird(birdwiki_pb2.BirdName(
        name=birdName))
    if response.name:
        print(f"Pássaro {birdName} criado com sucesso!")
        return response
    else:
        print(f"Não foi possível criar pássaro {birdName}.")
        return None


# VERIFICA DISPONIBILIDADE DE EDITAR AVE
# EXIBE MENU DE OPÇÔES (ler, escolher outra ou sair) CASO AVE EM EDICAO
def checkBirdAvailability(stub, bird):
    if bird.editing == True:
        print("\nPássaro já está sendo editado.")
        print(
            "\nEscolha uma das opcoes: \n[1] Abrir para leitura \n[2] Escolher outra ave \n[0] Sair")
        option = int(sys.argv[2])

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


def editBird(stub, bird):
    response = stub.editBird(
        birdwiki_pb2.BirdName(name=bird.name))
    editor = EditorWindow(response.name, response.text, True)
    editor.run()
    response = stub.saveBird(
        birdwiki_pb2.BirdPage(name=bird.name, text=editor.content)
    )


def deleteBird(stub, bird):
    response = stub.deleteBird(birdwiki_pb2.BirdName(name=bird.name))
    if (response.flag == True):
        print(f"Ave {bird.name} deletada")
    else:
        print(f"Ave {bird.name} não pode ser deletada")


def run():
    with grpc.insecure_channel('localhost:5002') as channel:
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        # login(birdwiki_pb2_grpc.LoginUserStub(channel))

        while True:
            try:

                bird = chooseBird(stub)  # LISTA AS AVES E ESCOLHE UMA
                print(
                    "Escolha uma das opcoes: \n[1] Abrir para leitura \n[2] Editar \n[3] Deletar \n[0] Sair")
                option = int(sys.argv[2])
                if(option == 2):
                    # VERIFICA SE PODE EDITAR AVE ESCOLHIDA
                    checkBirdAvailability(stub, bird)
                elif(option == 1):
                    readBird(stub, bird)
                elif(option == 3):
                    deleteBird(stub, bird)
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
