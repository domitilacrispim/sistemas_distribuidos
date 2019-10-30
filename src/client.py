from __future__ import print_function
import logging
import time

import grpc

import birdwiki_pb2
import birdwiki_pb2_grpc

import loginuser_pb2
import loginuser_pb2_grpc


# EFETUA LOGIN DE USUARIO
# FICA EM LOOP ENQUANTO LOGIN FALHA (nome ou senha incorretos)
# TODO (baixa prioridade): OPÇÂO DE SAIR
def login(stub):
    print("\n --- LOGIN ---")

    while(True):
        crBio = input("crBio: ")
        password = input("Senha: ")

        response = stub.login(loginuser_pb2.UserLogin(
            crBio=crBio, password=password))

        if not response.crBio:
            print("Usuário ou senha incorretos. Tente Novamente\n\n")
        else:
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
        birdName = input("Escolha uma ave para editar: ")

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
        print("Pássaro já está sendo editado.")
        print(
            "Escolha uma das opcoes: \n[1] Abrir para leitura \n[2] Escolher outra ave \n[0] Sair")
        option = int(input())

        if option == 1:
            readBird(stub, bird)

        if option == 0:
            raise KeyboardInterrupt

    else:
        editBird(stub, bird)


# LER DADOS DE UMA AVE
# TODO: REQUISITAR AO BANCO A LEITURA DA AVE
def readBird(stub, bird):
    print("LER AVE ", bird.name)
    # response = stub.showBird(
    #     birdwiki_pb2.BirdName(name='test1'))
    # print("\nINFO DA AVE: ")
    # print(response.name)
    # print(response.text)

# EDITAR DADOS DE UMA AVE
# TODO: REQUISITAR AO BANCO A EDIÇÂO DA AVE
def editBird(stub, bird):
    print("EDITAR AVE ", bird.name)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = birdwiki_pb2_grpc.BirdWikiStub(channel)
        login(loginuser_pb2_grpc.LoginUserStub(channel))

        while True:
            time.sleep(1)
            try:

                bird = chooseBird(stub)  # LISTA AS AVES E ESCOLHE UMA
                checkBirdAvailability(stub, bird) # VERIFICA SE PODE EDITAR AVE ESCOLHIDA

                # # TESTE 2: """"SALVANDO"""" UMA AVE
                # response = stub.saveBird(
                #     birdwiki_pb2.BirdPage(name="test2", text=""))
                # print("\nIS SAVED? ", response.saved)

            except KeyboardInterrupt:
                print("Goodbye")
                channel.unsubscribe(close)
                exit()


def close(channel):
    channel.close()


if __name__ == '__main__':
    logging.basicConfig()
    run()
