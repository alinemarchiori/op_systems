import time
from classes import *

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = None
tempo_total = 0

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

# algoritmo propriamente dito
def alternanciaCircular(lista_de_linhas):
    global lista_processos, tempo_total, lista_de_processos_para_mostrar_o_tempo
    _, tempo_de_CPU = lista_de_linhas[0].split("|")
    lista_de_linhas.remove(lista_de_linhas[0])
    listaProcessos(lista_de_linhas)
    lista_de_processos_para_mostrar_o_tempo = lista_processos
    
    while len(lista_processos) > 0:
        for processo in lista_processos:
            tempo_total += 1
            processo.atualizaTempoDemorado(tempo_total)
            processo.atualizaTempo(int(tempo_de_CPU))
            print(processo)
            #time.sleep(1)
            if processo.getTempo() <= 0:
                lista_processos.remove(processo)
            getNumeroProcessosFaltantes()
    
    return lista_de_processos_para_mostrar_o_tempo
