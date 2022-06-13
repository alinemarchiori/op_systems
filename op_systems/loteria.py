############################################################# NÃO ESTÁ PRONTO ############################################################


import time
import random
from classes import *

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = None
tempo_total = 0

lista_de_bilhetes = []
total_de_bilhetes = 0

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

def bilhetes():
    global lista_de_bilhetes,total_de_bilhetes 
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

#bilhetes de cada processo
def bilhetes_de_cada_processo():
    global total_de_bilhetes
    contador_de_bilhetes=None
    lista_bilhetes_por_processo = []
    p = 0 #posição na lista de processos
    while total_de_bilhetes>0:
        if contador_de_bilhetes ==None:
            contador_de_bilhetes = lista_processos[p].prioridade
        else:
            contador_de_bilhetes += lista_processos[p].prioridade
        lista_bilhetes_por_processo.append(contador_de_bilhetes)
        total_de_bilhetes-=lista_processos[p].prioridade
        p+=1
    # pegar a quantidade de bilhetes processo a processo e adicionar na lista acima a partir do contador 
    # exemplo lista_bilhetes_por_contador =[6,10,15,21]
    # cada posição é o limite de cada processo, ou seja, limite processo 1 é de 1 até 6, processo 2 é de 7 até 10 e assim sucessivamente

#onde a magica acontece
def loteria(lista_de_linhas):
    global lista_processos, tempo_total, lista_de_processos_para_mostrar_o_tempo,lista_de_bilhetes,total_de_bilhetes
    _, tempo_de_CPU = lista_de_linhas[0].split("|") 
    lista_de_linhas.remove(lista_de_linhas[0])
    listaProcessos(lista_de_linhas)
    lista_de_processos_para_mostrar_o_tempo = lista_processos
