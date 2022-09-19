import time
import os

class Pagina:
    def __init__(self, nome):
        self.nome = nome
        self.tempo_inicial_na_memoria = 0
        self.tempo_final_na_memoria = 0

    def set_tempo_inicial(self):
        self.tempo_inicial_na_memoria = time.process_time_ns()

    def zera_tempo(self):
        self.tempo_inicial_na_memoria = 0
        self.tempo_final_na_memoria = 0

    def get_tempo(self):
        self.tempo_final_na_memoria = time.process_time_ns()
        return self.tempo_final_na_memoria - self.tempo_inicial_na_memoria

    def __repr__(self) -> str:
        return f'Pagina: {self.nome}'


def FIFO_beatriz():
    pass


# FALAR PARA O PROFESSOR QUE O ARQUIVO NÃO ESTÁ CERTO, as colunas estão trocadas
def MRU_aline(linha): 
    quantidade_molduras, quantidade_paginas, referencias = organiza_linha(linha)
    tabela_de_paginas = [Pagina(nome) for nome in range(1, quantidade_paginas + 1)]
    mapa_de_bits = []
    numero_de_trocas_de_paginas = 0

    #para cada uma das referencias da lista de referencias é realizada
    #a verificação se a página está ou não na memória
    for referencia in referencias:
        pagina_em_questao = tabela_de_paginas[referencia - 1]
        
        #verifica se a página já está na memória
        if pagina_em_questao in mapa_de_bits:
            pass
        
        #se não estiver, verifica se a memória está cheia e insere a página na memória
        elif len(mapa_de_bits) < quantidade_molduras:
            mapa_de_bits.append(pagina_em_questao)
            pagina_em_questao.set_tempo_inicial()
            numero_de_trocas_de_paginas += 1

        #caso a memória estiver cheia, é necessário fazer a troca de páginas
        elif len(mapa_de_bits) >= quantidade_molduras:
            pagina_a_ser_removida = mapa_de_bits[0]
            tempo_na_memoria = 0

            #loop que verifica qual das páginas está a mais tempo na memória e guarda ela
            for pagina in mapa_de_bits:
                
                if pagina.get_tempo() > tempo_na_memoria:
                    tempo_na_memoria = pagina.get_tempo()
                    pagina_a_ser_removida = pagina
                    #print(mapa_de_bits, pagina, pagina.get_tempo(), pagina_em_questao)
            
            #depois de encontrar a página a ser removida, é zerado o tempo dela e 
            #ela é substituída da memória pela página que está sendo referenciada
            pagina_a_ser_removida.zera_tempo()
            mapa_de_bits.remove(pagina_a_ser_removida)
            mapa_de_bits.append(pagina_em_questao)
            pagina_em_questao.set_tempo_inicial()
            numero_de_trocas_de_paginas += 1
 
    return numero_de_trocas_de_paginas


def NUF_cris():
    pass


def OTIMO_breno():
    pass


#recebe uma linha em string e retorna a quantidade de molduras, quantidade de paginas 
#e uma lista de inteiros que correspondem às referências das paginas durante a 
#execução do processo
def organiza_linha(linha):
    quantidade_molduras, quantidade_paginas, referencias = linha.split('|') 
    referencias = referencias.split(' ') 
    return (
        int(quantidade_molduras), 
        int(quantidade_paginas), 
        [int(referencia) for referencia in referencias]
    )


#função para formatar a saída
def mostra_na_tela(lista, menor_valor):
    nomes = ['FIFO', 'MRU', 'NUF']
    return (
        f'{lista[0]}|{lista[1]}|{lista[2]}|{lista[3]}|{nomes[lista.index(menor_valor)]}'
    )


#função que lê o arquivo e retorna uma lista das linhas
def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas


def main():
    caminho = os.path.join("gerenciador_de_memoria", "arquivos_entrada_e_saida", "inMemoria.txt")
    arquivo =  leArquivo(caminho)

    for linha in arquivo:
        '''
        #chama todas as funções passando a linha com os dados
        fifo = FIFO_beatriz()
        mru = MRU_aline()
        nuf = NUF_cris()
        otimo = OTIMO_breno()
        '''
        #apenas para fins de teste
        fifo = 200
        mru = MRU_aline(linha)
        nuf = 100
        otimo = 2

        # armazena os resultados em uma lista
        lista_trocas_por_processo = [fifo, mru, nuf, otimo]

        #pega o menor valor da lista excluindo o ótimo
        menor_valor = min(lista_trocas_por_processo[:3])

        #verifica se deu empate
        if lista_trocas_por_processo[:3].count(menor_valor) > 1:
            print(f'{fifo}|{mru}|{nuf}|{otimo}|empate')
        
        else:
            print(mostra_na_tela(lista_trocas_por_processo, menor_valor))
            
main()           