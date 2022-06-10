from alternancia_circular import *
from por_prioridade import *
from loteria import *
from classes import *
import threading 

def mostraEstatisticas(lista_processoss):
    for processo in lista_processoss:
        print(processo,"Tempo que demorou para terminar: " ,processo.getTempoTotaldeExecucao())

def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas

def escolheAlgoritmo(): 
    algoritmo = int(input("1 - Alternancia Circular\n2 - Por prioridade\n3 - Loteria\n"))
    
    if algoritmo == 1: 
        lista_processoss = alternanciaCircular(leArquivo("exemplos_entradas\\testeAlternancia.txt"))
        mostraEstatisticas(lista_processoss)
        
    elif algoritmo == 2:
        lista_processoss = porPrioridade(leArquivo("exemplos_entradas\\testeAlternancia.txt"))
        print(lista_processoss)
        mostraEstatisticas(lista_processoss)
        
    elif algoritmo == 3:
        loteria(leArquivo("exemplos_entradas\\loteria.txt"))

    else:
        print("valor invalido")

def main():
    t1 = threading.Thread(target=escolheAlgoritmo)  
    t2 = threading.Thread(target=criaProcesso)  
    t1.start()
    t2.start()

main()
