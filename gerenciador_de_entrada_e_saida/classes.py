import random
from threading import Thread, Semaphore, Lock
import time

# Esse arquivo guarda uma classe que é usada em dois
# algoritmos o por prioridade e o alternância circular

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

    def liberaDispositivo(self):
        self.dispositivo = None

    def fazEntradaSaida(self, callback):
        self.dispositivo.fazEntradaSaida(callback)

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
        return random.random() < chance_de_requisitar #TODO: acho que precisa de um intervalo de numeros
    #serve para quando dar print no objeto ele não retornar 
    #uma referência de memória e retornar uma string com alguns detalhes importantes
    def __repr__(self) -> str:
        return f'Processo em execucao: {self.nome_processo}\nTempo que demorou para executar: {self.tempo_que_demorou_para_executar}\n'

class Dispositivo:
    def __init__(self, id, num_usos_simultaneos, tempo_operacao):
        self.id = id
        self.num_usos_simultaneos = num_usos_simultaneos
        self.tempo_operacao = tempo_operacao
        self.tempo_que_demorou_para_operar = 0
        #print(type(self.num_usos_simultaneos))
        self.semmaphore = Semaphore(self.num_usos_simultaneos)
        
    #esse método recebe o tempo de cpu e a cada vez que é
    #chamado diminui esse tempo de cpu do tempo de execução inicial
    def atualizaTempo(self, tempo_CPU):
        self.tempo_operacao -= tempo_CPU

    #esse método apenas retorna o tempo de execução restante
    def getTempo(self):
        return self.tempo_operacao
    
    #método que vai alterando o tempo total que o processo demorou
    #pra terminar
    def atualizaTempoDemorado(self, tempo_atual):
        self.tempo_que_demorou_para_operar += tempo_atual

    def fazEntradaSaida(self, callback):
        thread = Thread(target=callback)
        thread.start()