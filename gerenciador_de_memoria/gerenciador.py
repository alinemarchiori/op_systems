def FIFO_beatriz():
    pass

def MRU_aline(linha):
    quantidade_molduras, quantidade_paginas, referencias = organiza_linha(linha)
    print(quantidade_molduras, quantidade_paginas, referencias)
    return 50

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
    arquivo =  leArquivo("gerenciador_de_memoria\\arquivos_entrada_e_saida\\inMemoria.txt")

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