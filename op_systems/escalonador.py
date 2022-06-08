from alternancia_circular import *
#from por_prioridade import *
from loteria import *
import threading 

#Como serão adicionados os novos processos em tempo de execução? (Perguntar para o professor)

def adicionaNovoProcesso():
    pass

def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas

def escolheAlgoritmo(): 
    algoritmo = int(input("1 - Alternancia Circular\n2 - Por prioridade\n3 - Loteria\n"))
    
    if algoritmo == 1: #precisa escrever novamente no arquivo? add loop while até que acabem os processos
        alternanciaCircular(leArquivo("exemplos_entradas\\alternancia.txt"))
        
    #elif algoritmo == 2:
    #    porPrioridade(leArquivo("exemplos_entradas\\prioridades.txt"))
        
    elif algoritmo == 3:
        loteria(leArquivo("exemplos_entradas\\loteria.txt"))

    else:
        print("valor invalido")

def main():
    t1 = threading.Thread(target=escolheAlgoritmo)  
    t2 = threading.Thread(target=adicionaNovoProcesso)  
    t1.start()
    t2.start()

main()
