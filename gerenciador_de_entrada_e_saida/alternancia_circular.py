import time
from classes import *

#AS THREADS NÂO ESTÂO FUNCIONANDO CORRETAMENTE

# tabela de processos -> PRONTOS E BLOQUEADOS
lista_processos_bloqueados = []
lista_de_dispositivos = []
lista_de_threads = []

# variáveis globais
lista_processos = []
lista_de_processos_para_mostrar_o_tempo = []
tempo_total = 0

#função que lê o arquivo e retorna uma lista das linhas
def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas

def mostraEstados(processo_executando_agora):
    global lista_processos_bloqueados, lista_processos
    print("\n----------------------RELATORIO-----------------------------")
    print("\nProcesso em execucao: " + str(processo_executando_agora))
    print("------------------------------------------------------------")
    print("\nProcessos bloqueados:")
    for processo in lista_processos_bloqueados:
        print(processo, "Dispositivo: " + str(processo.dispositivo))
    print("------------------------------------------------------------")
    print("\nProcessos prontos: ")
    for processo in lista_processos:
        print(processo)
    print("------------------------------------------------------------")
    print("Dispositivos existentes: ")
    for dispositivo in lista_de_dispositivos:
        print(f'\nId: {dispositivo}, processos usando: {dispositivo.processos_usando}')
    print("------------------------------------------------------------\n")

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
def alternanciaCircular(lista_de_processos_linha, tempo_de_CPU=1):
    global lista_processos, tempo_total, lista_de_threads
    #chama a função passando apenas as linhas que tem processos
    listaProcessos(lista_de_processos_linha)
    lista_processos_prontos = [processo for processo in lista_processos]

    while True:
        if len(lista_processos + lista_processos_bloqueados) > 0:
            for i in range(len(lista_processos_bloqueados)):
                tempo_total += int(tempo_de_CPU)
            #loop que executa em ordem de criação dos processos
            for i, processo in enumerate(lista_processos):
                time.sleep(1)
                tempo_total += int(tempo_de_CPU)

                '''for dispositivo in lista_de_dispositivos:
                    dispositivo.atualizaTempo(int(tempo_de_CPU))'''

                if processo.escolhe():
                #if processo.escolhe():
                    processo.escolheDispositivo(lista_de_dispositivos)
                    lista_processos.remove(processo)
                    lista_processos_bloqueados.append(processo)
                    #print(processo, processo.dispositivo, processo.dispositivo.tempo_que_demorou_para_operar, processo.dispositivo.tempo_operacao)
                    #mostraEstados(processo)
                    def callback(processo):
                        global lista_processos, lista_processos_bloqueados, tempo_total, lista_processos_prontos
                        processo.dispositivo.semmaphore.acquire()
                        processo.dispositivo.addProcesso(processo)
                        #mostraEstados(processo)
                        if processo.dispositivo:
                            processo.dispositivo.atualizaTempoInicio(tempo_total, processo)
                            while True:
                                processo.dispositivo.atualizaTempoTotal(tempo_total, processo)
                                if processo.terminouES():
                                    break
                            lista_processos_bloqueados.remove(processo)
                            lista_processos.append(processo)
                            processo.dispositivo.removeProcesso(processo)
                        processo.dispositivo.semmaphore.release()
                        #processo.liberaDispositivo()
                    processo.fazEntradaSaida(callback)
                    #lista_processos_prontos = [processo for processo in lista_processos_prontos if processo.getTempo() <= 0]
                else:
                    processo.atualizaTempoDemorado(tempo_total)
                    processo.atualizaTempo(int(tempo_de_CPU))
                    time.sleep(1)
                    if processo.getTempo() <= 0:
                        lista_processos.remove(processo)
                    #lista_processos_bloqueados = [processo for processo in lista_processos_bloqueados if processo.getTempo() <= 0]
                #lista_processos = lista_processos_prontos + lista_processos_bloqueados
                mostraEstados(processo)
                 
        else:
            #lista_de_threads.clear()
            #lista_de_dispositivos.clear()
            break
    
    return lista_de_processos_para_mostrar_o_tempo

if __name__ == '__main__':
    linhas_do_arquivo = leArquivo("gerenciador_de_entrada_e_saida/nomedoarquivo.txt")
    tempo_de_cpu, num_de_dispositivos = linhas_do_arquivo[0].split("|")
    lista_de_processos_linha = []
    
    for linha_do_arquivo in range(1,(int(num_de_dispositivos)+1)):
        linha_separada = linhas_do_arquivo[linha_do_arquivo].split("|")
        id = linha_separada[0]
        num_usos_simultaneos = int(linha_separada[1])
        tempo_operacao = int(linha_separada[2])
        lista_de_dispositivos.append(Dispositivo(id, num_usos_simultaneos, tempo_operacao))
    
    for linha_do_arquivo in range((int(num_de_dispositivos)+1), len(linhas_do_arquivo)):
        lista_de_processos_linha.append(linhas_do_arquivo[linha_do_arquivo])

    processos_para_mostrar_o_tempo = alternanciaCircular(lista_de_processos_linha, tempo_de_CPU=tempo_de_cpu)
    