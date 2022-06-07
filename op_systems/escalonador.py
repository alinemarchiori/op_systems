from alternancia_circular import *
from por_prioridade import *
from loteria import *

#PONTOS A SEREM RESOLVIDOS

# - caminho do arquivo padrão
# - 

def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas

def escolheAlgoritmo(): 
    algoritmo = int(input("1 - Alternancia Circular\n2 - Por prioridade\n3 - Loteria\n"))
    
    if algoritmo == 1:
        alternanciaCircular(leArquivo("alternancia.txt"))
        
#    elif algoritmo == 2:
#        porPrioridade(leArquivo("prioridades.txt"))
        
    elif algoritmo == 3:
        loteria(leArquivo("loteria.txt"))

    else:
        print("valor invalido")

def main():
    escolheAlgoritmo()

main()