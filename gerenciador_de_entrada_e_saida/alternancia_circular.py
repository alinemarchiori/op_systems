import time
from classes import *

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = []
tempo_total = 0


# printa quantos processos ainda restam na fila
def getNumeroProcessosFaltantes():
    print(f'Processos em espera: {len(lista_processos)}\n')

# organiza os processos em uma lista e instancia a classe para cada processo
def listaProcessos(lista_linhas):
    global lista_processos, lista_de_processos_para_mostrar_o_tempo

    for processo in lista_linhas:
        objeto_processo = Processo()
        objeto_processo.setDetalhesProcesso(processo.split('|'))
        lista_de_processos_para_mostrar_o_tempo.append(objeto_processo)
        lista_processos.append(objeto_processo)

# algoritmo propriamente dito
def alternanciaCircular(lista_de_linhas):
    global lista_processos, tempo_total
    #retira a primeira linha do arquivo, que tem o tempo de cpu e o nome do algoritmo
    _, tempo_de_CPU = lista_de_linhas[0].split("|")
    lista_de_linhas.remove(lista_de_linhas[0])
    #chama a função passando apenas as linhas que tem processos
    listaProcessos(lista_de_linhas)
    #loop que serve para executar um processo mesmo que os outros já tenham acabado
    while True:
        #verifica se tem algum processo para ser executado ainda
        if len(lista_processos) > 0:
            #loop que executa em ordem de criação dos processos
            for processo in lista_processos:
                tempo_total += int(tempo_de_CPU)
                processo.atualizaTempoDemorado(tempo_total)
                processo.atualizaTempo(int(tempo_de_CPU))
                print(processo)
                time.sleep(1)
                if processo.getTempo() <= 0:
                    lista_processos.remove(processo)
                getNumeroProcessosFaltantes()
        else:
            break
    
    return lista_de_processos_para_mostrar_o_tempo
