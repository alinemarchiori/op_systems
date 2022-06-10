class Processo:
    def __init__(self) -> None:
        self.nome_processo = None
        self.id_unico_processo = None
        self.tempo_execucao = None
        self.prioridade = None
        self.id_usuario_dono_do_processo = None
        self.quantidade_memoria = None
        self.tempo_que_demorou_para_executar = 0

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

    def getTempoTotaldeExecucao(self):
        return self.tempo_que_demorou_para_executar

    def atualizaTempoDemorado(self, tempo_atual):
        self.tempo_que_demorou_para_executar += tempo_atual

    def __repr__(self) -> str:
        return f'Processo em execucao: {self.nome_processo}\nTempo restante: {self.tempo_execucao}\nPrioridade: {self.prioridade}\n'
