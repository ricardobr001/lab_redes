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
        self.matriz_alcance = [[]]
        self.vetor_arestas = [1, 1, 2, 7, 3]
        
    def inicia_matriz(self):
         
         # Se for o processo com id 0
         if self.id == 0:
             lista = [0, 1, 3, 7]
             for i in (1,4):                
                 for j in (0,4):
                     lista.append(-1)
                 self.matriz_alcance.append(lista)
                 lista = []
        
         elif self.id == 1:
             
         # Primeiro inicializamos todo mundo com valores negativos
         for i in range(0,4):
             lista = []
             for j in range(0, 4):
                 lista.append(-1)
             self.matriz_alcance.append(lista)

    def atualiza_matriz(self):
        
        if self.id == 0:
            for i in range(0,4):
                
                
            
        
    # Definição do método que envia uma mensagem
    def envia_msg(self):

        # Gera uma mensagem aleatória
        mensagem = self.cria_msg(choice(string.letters))

        print 'Enviando a mensagem:', mensagem.msg

        # Enviando a mensagem para todas as portas
        for i in range(0,3):

            # Abrindo o socket
            meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 25000 + i)
            meu_socket.connect(server_address)

            # Enviando a mensagem e o ack para os outros processos
            mensagem_codificada = pickle.dumps(mensagem)
            meu_socket.send(mensagem_codificada)
            meu_socket.close()

# Definindo uma mensagem
class Mensagem:
    def __init__(self, clock_msg, msg, id):
        self.clock_msg = clock_msg
        self.id = id
        self.msg = msg

    def get_clock(self):
        return self.clock_msg

    def get_id(self):
        return self.id

# Definindo um ack
class Ack:
    def __init__(self, id):
        self.id = id
        self.n_acks = 0

    def get_id(self):
        return self.id

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

                    if isinstance(decodificada, (Mensagem)):
                        ack = processo.recebe_msg(decodificada)
                        processo.envia_ack(ack)

                    elif isinstance(decodificada, (Ack)):
                        processo.recebe_ack(decodificada)

                except Exception as e:
                    print 'Erro ao receber:', e
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)



        except Exception as e:
            print 'Erro ao abrir o socket:', e
            time.sleep(5)

# Definindo a thread que gera as mensagens
def thread_gera():
    global processo

    while True:
        time.sleep(10)

        try:
            processo.envia_msg()
        except Exception as e:
            print 'Erro ao enviar', e
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

# Definindo a thread do clock
def thread_clock():
    global processo

    while True:
        processo.incrementa_clock()

        time.sleep(2)

processo = Processo(int(sys.argv[2]))

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_clock, ())

    signal.pause()

if __name__ == "__main__":
sys.exit(main())