from escalonador import *
from threading import Thread, Semaphore, Lock
import random
# tabela de processos -> PRONTOS E BLOQUEADOS
lista_processos_prontos = []
lista_processos_bloqueados = []
lista_de_dispositivos = []

class Dispositivo:
    def __init__(self, id, num_usos_simultaneos, tempo_operacao):
        self.id = id
        self.num_usos_simultaneos = num_usos_simultaneos
        self.tempo_operacao = tempo_operacao
        self.thread = Thread(target=self._on_run)
        self.semmaphore = Semaphore(self.num_usos_simultaneos)

    def _on_run(self):
        with self.semmaphore:
            pass

def main():
    linhas_do_arquivo = leArquivo("nomedoarquivo.txt")
    tempo_de_cpu, num_de_dispositivos = linhas_do_arquivo[0].split("|")
    
    for linha_do_arquivo in range(1,(int(num_de_dispositivos)+1)):
        linha_separada = linha_do_arquivo.split("|")
        id = linha_separada[0]
        num_usos_simultaneos = linha_separada[1]
        tempo_operacao = linha_separada[2]
        lista_de_dispositivos.append(Dispositivo(id, num_usos_simultaneos, tempo_operacao))
    
    processo_em_execucao = alternanciaCircular()
    chance_de_requisitar = 80#TODO: pegar esse valor do arquivo
    chance_de_requisitar = chance_de_requisitar/100
    if random.random() < chance_de_requisitar:
        #TODO: botar o processo como bloqueado, e sortear o dispositivo e momento que ele deve ser executado.
        pass
    else:
        alternanciaCircular()


# lê arquivo
# chama o escalonador
# quando o processo estiver executando, sorteia pra saber se vai fazer entrada e saída
# SE entrada e saída == TRUE:
#     Sorteia dispositivo
#     Sorteia momento que vai realizar
#     "Executa"
#     fazer_entrada_e_saida()
# SENÃO:
#     "Executa"



# cada dispositivo vai ter uma thread (acho que foi isso que o professor sugeriu)

# as threads podem ser criadas antes de chamar o escalonador e poder ser guardadas numa lista
# quando sortear o dispositivo, apenas pegamos a thread que tiver o índice correspondendo ao 
# número do dispositivo e chamamos a função de fazer entrada e saída (só uma ideia)


"""
fazer_entrada_e_saida():
    while True:
        chegou algo na fila
        executa E/S
        processo => PRONTO
"""



# tarefas:

# ler e tratar os dados do arquivo
# enumerar os dispositivos (uma thread para cada dispositivo)
# bloquear os dispositivos que estão no seu limite de processos
# controlar o tempo de cada processo (executando e fazendo E/S)
# atualizar lista de bloqueado e pronto
# 