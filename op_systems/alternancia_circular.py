#nomeProcesso|PID|tempoDeExecução|prioridade (ou bilhetes)|UID|qtdeMemoria
"""
    - algoritmoDeEscalonamento é o algoritmo que será utilizado para escalonar os processos
    - fraçãoDeCPU representa o período que um processo pode ficar na CPU por vez
    - nomeProcesso contém o nome do processo (i.e., firefox.exe)
    - PID é o identificador único do processo
    - tempoDeExecução informa a quantidade de tempo que um processo necessita para executar
    - prioridade (ou bilhtes) contém a prioridade do processo (ou número de bilhetes para o algoritmo da loteria)
    - UID ID do usuário dono do processo
    - qtdeMemoria informa a quantidade de memória que o processo precisa para executar (uso futuro)
"""


from multiprocessing.dummy import Process
import time

lista_processos = []

class Processo:
    def __init__(self) -> None:
        self.nome_processo = None
        self.id_unico_processo = None
        self.tempo_execucao = None
        self.prioridade = None
        self.id_usuario_dono_do_processo = None
        self.quantidade_memoria = None

    def setDetalhesProcesso(self, processo):
        self.nome_processo = processo[0]
        self.id_unico_processo = int(processo[1])
        self.tempo_execucao = int(processo[2])
        self.prioridade = int(processo[3])
        self.id_usuario_dono_do_processo = int(processo[4])
        self.quantidade_memoria = int(processo[5])

    def atualizaTempo(self, tempo_CPU):
        self.tempo_execucao -= tempo_CPU

    def getTempo(self):
        return self.tempo_execucao

    def __repr__(self) -> str:
        return f'Processo em execucao: {self.nome_processo}\nTempo restante: {self.tempo_execucao}\n'

def criaProcesso():
    pass

def getNumeroProcessosFaltantes():
    print(f'Processos em espera: {len(lista_processos)}\n')

def listaProcessos(lista_linhas):
    global lista_processos
    for processo in lista_linhas:
        objeto_processo = Processo()
        objeto_processo.setDetalhesProcesso(processo.split('|'))
        lista_processos.append(objeto_processo)
    
    return lista_processos

def alternanciaCircular(lista_de_linhas):
    global lista_processos
    _, tempo_de_CPU = lista_de_linhas[0].split("|")
    lista_de_linhas.remove(lista_de_linhas[0])
    listaProcessos(lista_de_linhas)

    while len(lista_processos) > 0:
        for processo in lista_processos:
            processo.atualizaTempo(int(tempo_de_CPU))
            print(processo)
            time.sleep(1)
            if processo.getTempo() <= 0:
                lista_processos.remove(processo)
            getNumeroProcessosFaltantes()

    return lista_processos
        

