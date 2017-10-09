#coding: utf-8
# python 2.7
# Desenvolvido apenas para 3 processos, rodando nas portas 25000, 25001 e 25002
# Com os IDs sendo 0, 1 e 2 respectivamente
# Executar o programa passando no argumento a porta e o seu ID
# Ex: python Process.py 25000 1
# Ou iniciar o start.py (Necessário sistema linux)


###################################################################
# Nome: Gabriel Piovani Moreira dos Santos          RA: 552216    #
# Nome: Ricardo Mendes Leal Junior                  RA: 562262    #
###################################################################


from random import *
import socket
import string
import thread
import pickle
import sys
import signal
import time
# import os

# Definindo um processo
class Processo:

    # Um processo terá seu ID, sua tabela de alcance e o vetor de suas arestas
    def __init__(self, id):
        self.id = id
        self.alcance = []
        self.atualizados = 0

    # Definição do método que inicia o nó 0
    def rinit0(self):

        # Inicializa o vetor de alcance do processo
        self.alcance[0] = Conteudo(0, 0)
        self.alcance[1] = Conteudo(1, 0)
        self.alcance[2] = Conteudo(3, 0)
        self.alcance[3] = Conteudo(7, 0)

    # Definição do método que inicia o nó 1
    def rinit1(self):

        # Inicializa o vetor de alcance do processo
        self.alcance[0] = Conteudo(1, 1)
        self.alcance[1] = Conteudo(0, 1)
        self.alcance[2] = Conteudo(1, 1)
        self.alcance[3] = Conteudo(-1, 1)

    # Definição do método que inicia o nó 2
    def rinit2(self):

        # Inicializa o vetor de alcance do processo
        self.alcance[0] = Conteudo(3, 2)
        self.alcance[1] = Conteudo(1, 2)
        self.alcance[2] = Conteudo(0, 2)
        self.alcance[3] = Conteudo(2, 2)

    # Definição do método que inicia o nó 3
    def rinit3(self):

        # Inicializa o vetor de alcance do processo
        self.alcance[0] = Conteudo(7, 3)
        self.alcance[1] = Conteudo(-1, 3)
        self.alcance[2] = Conteudo(2, 3)
        self.alcance[3] = Conteudo(0, 3)

    # Definição do método que envia o vetor alcance para outro processo
    def envia_alcance(self, id):

        mensagem = Mensagem(self.alcance, id)

        # Abrindo o socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 25000 + id)
        meu_socket.connect(server_address)

        # Enviando a mensagem e o ack para os outros processos
        mensagem_codificada = pickle.dumps(mensagem)
        meu_socket.send(mensagem_codificada)
        meu_socket.close()

    # Definição do método que envia a flag de atualização a seus processos adjacentes
    def envia_flag(self, flag, id):

        # Abrindo o socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 25000 + id)
        meu_socket.connect(server_address)

        # Enviando a mensagem e o ack para os outros processos
        mensagem_codificada = pickle.dumps(flag)
        meu_socket.send(mensagem_codificada)
        meu_socket.close()

    # Definição do método que atualiza o vetor de alcance do processo
    def atualiza_alcance(self, msg):

        # Flag que ira marcar caso haja uma atualização
        flag = False

        #Andando o vetor alcance do processo
        for i in range(len(msg)):

            # Se o meu alcance atual for maior que o novo alcance recebido, atualizo meu alcance
            if self.alcance[i] > msg.alcance[i]:
                flag = True
                self.alcance[i] = msg.alcance[i]

        # Se houve uma atualização, retorna verdadeiro
        if flag:
            return flag

        # Caso contrário, retorna falso
        return flag


# Definindo uma mensagem
class Mensagem:
    def __init__(self, alcance, id):
        self.alcance = alcance
        self.id = id

# Definindo um conteúdo
class Conteudo:
    def __init__(self, valor, id):
        self.valor = valor
        self.id = id

# Definindo a thread que recebe dados
def thread_recebe():

    while True:
        serverPort = int(sys.argv[1])

        # Criando o socket
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:

            # O socket fica ouvindo o meio
            serverSocket.bind(('',serverPort))
            serverSocket.listen(1)

            while True:

                # Aceita uma conexão
                connectionSocket, addr = serverSocket.accept()

                try:

                    # Recebe os dados e os decodifica
                    data = connectionSocket.recv(1024)
                    decodificada = pickle.loads(data)
                    # processo.atualiza_alcance(decodificada)

                    # Ou é uma mensagem com o vetor alcance
                    if isinstance(decodificada, (Mensagem)):
                        flag = processo.atualiza_alcance(decodificada)
                        processo.envia_flag(flag)

                        if flag:
                            processo.atualizados = 0

                    # Ou é uma mensagem com a flag de atualização
                    else:
                        if not decodificada:
                            processo.atualizados += 1
                        else:
                            processo.atualizados = 0

                except Exception as e:
                    print 'Erro ao receber:', e
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)



        except Exception as e:
            print 'Erro ao abrir o socket:', e
            time.sleep(5)

# Definindo a thread que gera as mensagens
def thread_inicia():
    global processo

    while True:

        try:
            # Aguarda uma entrada do usuário para iniciar
            raw_input()

            processo.envia_alcance(processo.id)
        except Exception as e:
            print 'Erro ao enviar', e
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

processo = Processo(int(sys.argv[1]))

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_inicia, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())
