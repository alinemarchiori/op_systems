import time
from classes import *
from escalonador import *
from threading import Thread, Semaphore, Lock
import random
# tabela de processos -> PRONTOS E BLOQUEADOS
lista_processos_prontos = []
lista_processos_bloqueados = []
lista_de_dispositivos = []

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = []
tempo_total = 0

#função que lê o arquivo e retorna uma lista das linhas
def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas

# tabela de processos -> PRONTOS E BLOQUEADOS


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
def alternanciaCircular(lista_de_linhas, tempo_de_CPU=1):
    global lista_processos, tempo_total
    #retira a primeira linha do arquivo, que tem o tempo de cpu e o nome do algoritmo
    #tempo_de_CPU, _ = lista_de_linhas[0].split("|")
    #lista_de_linhas.remove(lista_de_linhas[0])
    #chama a função passando apenas as linhas que tem processos
    listaProcessos(lista_de_linhas)
    #linhas_do_arquivo = leArquivo("nomedoarquivo.txt")
    linhas_do_arquivo = lista_de_linhas
    #tempo_de_cpu, num_de_dispositivos = linhas_do_arquivo[0].split("|")
    lista_de_processos = [linhas_do_arquivo[0]]
    
    for linha_do_arquivo in range(1,(int(num_de_dispositivos)+1)):
        linha_separada = linhas_do_arquivo[linha_do_arquivo].split("|")
        id = linha_separada[0]
        num_usos_simultaneos = int(linha_separada[1])
        tempo_operacao = int(linha_separada[2])
        lista_de_dispositivos.append(Dispositivo(id, num_usos_simultaneos, tempo_operacao))
    
    for linha_do_arquivo in range((int(num_de_dispositivos)+1), len(linhas_do_arquivo)):
        lista_de_processos.append(linhas_do_arquivo[linha_do_arquivo])

    chance_de_requisitar = 80#TODO: pegar esse valor do arquivo
    chance_de_requisitar = chance_de_requisitar/100
    '''if random.random() < chance_de_requisitar:
        #TODO: botar o processo como bloqueado, e sortear o dispositivo e momento que ele deve ser executado.
        pass
    else:
        alternanciaCircular()'''


    #loop que serve para executar um processo mesmo que os outros já tenham acabado
    while True:
        #verifica se tem algum processo para ser executado ainda
        #print(lista_de_dispositivos)
        if len(lista_processos) > 0:
            #loop que executa em ordem de criação dos processos
            for processo in lista_processos:
                tempo_total += int(tempo_de_CPU)
                if processo.escolhe():
                    processo.escolheDispositivo(lista_de_dispositivos)
                    lista_processos.remove(processo) #TODO: lembrar de colocar o processo de volta depois que executar entrada e saida
                    lista_processos_bloqueados.append(processo)
                    processo.fazEntradaSaida()
                else:
                    processo.atualizaTempoDemorado(tempo_total)
                    processo.atualizaTempo(int(tempo_de_CPU))
                    #print(processo)
                    #print(lista_de_dispositivos)
                    time.sleep(1)
                    if processo.getTempo() <= 0:
                        lista_processos.remove(processo)
                getNumeroProcessosFaltantes()
        else:
            for dispositivo in lista_de_dispositivos:
                dispositivo.thread.join()
            break
    
    return lista_de_processos_para_mostrar_o_tempo

if __name__ == '__main__':
    linhas_do_arquivo = leArquivo("gerenciador_de_entrada_e_saida/nomedoarquivo.txt")
    tempo_de_cpu, num_de_dispositivos = linhas_do_arquivo[0].split("|")
    #lista_de_processos = [linhas_do_arquivo[0]]
    lista_de_processos = []
    
    for linha_do_arquivo in range(1,(int(num_de_dispositivos)+1)):
        linha_separada = linhas_do_arquivo[linha_do_arquivo].split("|")
        id = linha_separada[0]
        num_usos_simultaneos = int(linha_separada[1])
        tempo_operacao = int(linha_separada[2])
        lista_de_dispositivos.append(Dispositivo(id, num_usos_simultaneos, tempo_operacao))
    
    for linha_do_arquivo in range((int(num_de_dispositivos)+1), len(linhas_do_arquivo)):
        lista_de_processos.append(linhas_do_arquivo[linha_do_arquivo])
    alternanciaCircular(lista_de_processos, tempo_de_CPU=tempo_de_cpu)
    exit()
    processo_em_execucao = alternanciaCircular(lista_de_processos)
    #print(next(processo_em_execucao))
    #print(next(processo_em_execucao))
    for i in range(len(lista_de_processos)):
        proximo = next(processo_em_execucao)
        #print(proximo)

    chance_de_requisitar = 80#TODO: pegar esse valor do arquivo
    chance_de_requisitar = chance_de_requisitar/100
    if random.random() < chance_de_requisitar:
        #TODO: botar o processo como bloqueado, e sortear o dispositivo e momento que ele deve ser executado.
        pass
    else:
        pass
        #alternanciaCircular()