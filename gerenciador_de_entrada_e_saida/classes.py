import random
from threading import Thread, Semaphore, Lock
import time
import copy

#Essa classe tem todas as características que um processo
#precisa e traz alguns métodos que facilitam a execução dos
#algoritmos
class Processo:
    def __init__(self) -> None:
        self.nome_processo = None
        self.tempo_execucao = None
        self.tempo_que_demorou_para_executar = 0
        self.id_chance_de_requisitar_e_s = 0

    #Esse método apenas altera os valores das variáveis
    #recebe uma lista de strings e coloca cada uma no seu lugar
    def setDetalhesProcesso(self, processo):
        #print(processo)
        self.nome_processo = processo[0]
        self.tempo_execucao = int(processo[1])
        self.id_chance_de_requisitar_e_s = int(processo[2])
        self.tempo_que_demorou_para_executar = int(processo[1])
        self.dispositivo = None

    def escolheDispositivo(self, lista_dispositivos):
        self.dispositivo = random.choice(lista_dispositivos)
        assert self.dispositivo != None
        #self.dispositivo.addProcesso(self)

    def liberaDispositivo(self):
        #self.dispositivo.removeProcesso(self)
        self.dispositivo = None

    def fazEntradaSaida(self, callback):
        return self.dispositivo.fazEntradaSaida(callback, self)

    def terminouES(self):
        return self.dispositivo.terminouES(self)

    #esse método recebe o tempo de cpu e a cada vez que é
    #chamado diminui esse tempo de cpu do tempo de execução inicial
    def atualizaTempo(self, tempo_CPU):
        self.tempo_execucao -= tempo_CPU

    #esse método apenas retorna o tempo de execução restante
    def getTempo(self):
        return self.tempo_execucao

    #esse método retorna o tempo total que o processo demorou
    #para executar por completo
    def getTempoTotaldeExecucao(self):
        return self.tempo_que_demorou_para_executar

    #método que vai alterando o tempo total que o processo demorou
    #pra terminar
    def atualizaTempoDemorado(self, tempo_atual):
        self.tempo_que_demorou_para_executar += tempo_atual

    #método que atualiza o tempo total, mas esse só é usado
    #no algoritmo por prioridade
    def atualizaTempoDemoradoPrioridade(self, tempo_total):
        self.tempo_que_demorou_para_executar = tempo_total

    def escolhe(self):
        chance_de_requisitar = self.id_chance_de_requisitar_e_s
        chance_de_requisitar = chance_de_requisitar/100
        return random.random() < chance_de_requisitar

    #serve para quando dar print no objeto ele não retornar 
    #uma referência de memória e retornar uma string com alguns detalhes importantes
    def __repr__(self) -> str:
        return f'{self.nome_processo}, Tempo restante: {self.tempo_execucao}'

class Dispositivo:
    def __init__(self, id, num_usos_simultaneos, tempo_operacao):
        self.id = id
        self.num_usos_simultaneos = num_usos_simultaneos
        self.tempo_operacao = tempo_operacao
        self.tempo_que_demorou_para_operar = []
        self.tempo_inicio = []
        self.processos_usando = []
        self.semmaphore = Semaphore(self.num_usos_simultaneos)
        
    #esse método recebe o tempo de cpu e a cada vez que é
    #chamado diminui esse tempo de cpu do tempo de execução inicial
    def atualizaTempoInicio(self, tempo_inicio, processo):
        self.tempo_inicio[self.processos_usando.index(processo)] = tempo_inicio

    def atualizaTempoTotal(self, tempo_total, processo):
        self.tempo_que_demorou_para_operar[self.processos_usando.index(processo)] = tempo_total

    def getTempoTotal(self, tempo_total, processo):
        return self.tempo_que_demorou_para_operar[self.processos_usando.index(processo)]

    #esse método apenas retorna o tempo de execução restante
    def terminouES(self, processo):
        if processo not in self.processos_usando:
            return True
        return self.tempo_que_demorou_para_operar[self.processos_usando.index(processo)] - self.tempo_inicio[self.processos_usando.index(processo)] >= self.tempo_operacao

    def fazEntradaSaida(self, callback, processo):
        thread = Thread(target=callback, args=(processo,))
        thread.start()
        return thread

    def addProcesso(self, processo):
        self.processos_usando.append(processo)
        self.tempo_que_demorou_para_operar.append(0)
        self.tempo_inicio.append(0)

    def removeProcesso(self, processo):
        indice = self.processos_usando.index(processo)
        self.processos_usando.pop(indice)
        self.tempo_que_demorou_para_operar.pop(indice)
        self.tempo_inicio.pop(indice)

    def __repr__(self) -> str:
        return f'{self.id}'