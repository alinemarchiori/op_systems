from alternancia_circular import *
from por_prioridade import *
from loteria import *
from classes import *
import threading 

algoritmo = 0

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

#função da thread 2 que fica esperando o usuário informar
#qual algoritmo que ele quer para poder chamar a função de
#crair processo corretamente
def identificaAlgoritmo():
    while True:
        if algoritmo == 1:
            criaProcesso_alternancia_circular()
            break
        elif algoritmo == 2:
            criaProcesso_por_prioridade()
            break
        elif algoritmo == 3:
            criaProcesso_loteria()
            break

#Essa função fica na thread 1 e espera que o usuário
#informa qual algoritmo ele quer usar
def escolheAlgoritmo():
    global algoritmo
    algoritmo = int(input("1 - Alternancia Circular\n2 - Por prioridade\n3 - Loteria\n"))
    
    if algoritmo == 1: 
        lista_processoss = alternanciaCircular(leArquivo("exemplos_entradas\\testeAlternancia.txt"))
        mostraEstatisticas(lista_processoss)
        
    elif algoritmo == 2:
        lista_processoss = porPrioridade(leArquivo("exemplos_entradas\\testeAlternancia.txt"))
        mostraEstatisticas(lista_processoss)
        
    elif algoritmo == 3:
        loteria(leArquivo("exemplos_entradas\\testeAlternancia.txt"))
        #mostra o tempo que cada processo deorou para executar 
        print("Nome do processo // tempo demorado para execução total") 
        for i in range(len(Nome)):
            print(Nome[i],"//",Tempo [i])

    else:
        print("valor invalido")

#função principal que usa as threads
def main():
    t1 = threading.Thread(target=escolheAlgoritmo)  
    t2 = threading.Thread(target=identificaAlgoritmo)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

main()
