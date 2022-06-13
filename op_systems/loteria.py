############################################################# NÃO ESTÁ PRONTO ############################################################


import time
import random
from classes import *

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = None
tempo_total = 0

lista_de_bilhetes = []

# cria um novo processo em tempo de execução, lendo dados do terminal
def criaProcesso():
    processo = input()
    global lista_processos
    objeto_processo = Processo()
    objeto_processo.setDetalhesProcesso(processo.split('|'))
    lista_processos.append(objeto_processo)
    lista_de_processos_para_mostrar_o_tempo.append(objeto_processo)

# printa quantos processos ainda restam na fila
def getNumeroProcessosFaltantes():
    print(f'Processos em espera: {len(lista_processos)}\n')

# organiza os processos em uma lista e instancia a classe para cada processo
def listaProcessos(lista_linhas):
    global lista_processos

    for processo in lista_linhas:
        objeto_processo = Processo()
        objeto_processo.setDetalhesProcesso(processo.split('|'))
        lista_processos.append(objeto_processo)
#lista de bilhetes

def bilhetes(total_de_bilhetes):
    global lista_de_bilhetes 
    if lista_de_bilhetes==None:
        i=1 #numero do bilhete
    else:
        i=len(lista_de_bilhetes)+1
    while i<=total_de_bilhetes:
        lista_de_bilhetes.append(i)
        i+=1

#escolhe bilhete
def escolhe_bilhete():
    global lista_de_bilhetes
    escolha = random.randint(0,len(lista_de_bilhetes))
    
    return lista_de_bilhetes [escolha]

#onde a magica acontece
def loteria(lista_de_linhas):
    global lista_processos, tempo_total, lista_de_processos_para_mostrar_o_tempo
    _, tempo_de_CPU = lista_de_linhas[0].split("|") #não entendi isso 
    lista_de_linhas.remove(lista_de_linhas[0])
    listaProcessos(lista_de_linhas)
    lista_de_processos_para_mostrar_o_tempo = lista_processos
