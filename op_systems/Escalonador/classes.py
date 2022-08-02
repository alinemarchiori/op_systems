# Esse arquivo guarda uma classe que é usada em dois
# algoritmos o por prioridade e o alternância circular

#Essa classe tem todas as características que um processo
#precisa e traz alguns métodos que facilitam a execução dos
#algoritmos
class Processo:
    def __init__(self) -> None:
        self.nome_processo = None
        self.id_unico_processo = None
        self.tempo_execucao = None
        self.prioridade = None
        self.id_usuario_dono_do_processo = None
        self.quantidade_memoria = None
        self.tempo_que_demorou_para_executar = 0

    #Esse método apenas altera os valores das variáveis
    #recebe uma lista de strings e coloca cada uma no seu lugar
    def setDetalhesProcesso(self, processo):
        self.nome_processo = processo[0]
        self.id_unico_processo = int(processo[1])
        self.tempo_execucao = int(processo[2])
        self.prioridade = int(processo[3])
        self.id_usuario_dono_do_processo = int(processo[4])
        self.quantidade_memoria = int(processo[5])
        self.tempo_que_demorou_para_executar = int(processo[2])

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

    #serve para quando dar print no objeto ele não retornar 
    #uma referência de memória e retornar uma string com alguns detalhes importantes
    def __repr__(self) -> str:
        return f'Processo em execucao: {self.nome_processo}\nTempo restante: {self.tempo_execucao}\nPrioridade: {self.prioridade}\n'
