from alternancia_circular import *
from classes import *

#função que mostra os tempos que cada um demorou no final
def mostraEstatisticas(lista_processoss):
    print("--------------------------------------------------")
    for processo in lista_processoss:
        print(processo,"Tempo que demorou para terminar: ", processo.getTempoTotaldeExecucao())
    print("--------------------------------------------------")


#função que lê o arquivo e retorna uma lista das linhas
def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas
        

def main():
    
    lista_processoss = alternanciaCircular(leArquivo("C:\\Users\\aline\\Documents\\repositorios\\op_sistems_clone\\gerenciador_de_entrada_e_saida\\alternancia.txt"))
    mostraEstatisticas(lista_processoss)

main()
