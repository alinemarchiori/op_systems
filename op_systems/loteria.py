############################################################# NÃO ESTÁ PRONTO ############################################################
#falta testar função para o input em tempo de execução

import random
import time

nome_do_processo = []
tempo_de_cada_processo = []
lista_de_bilhetes_processo = [] #bilhete de cada processo
cpu=None

total_de_bilhetes=0
lista_bilhetes_teto = [] #limite superior 
lista_de_bilhetes = [] # bilhetes de 1 até n 
tempo_decorrido = 0
Nome= []
Tempo= []

def criaProcesso():
    processo = input()
    global nome_do_processo, tempo_de_cada_processo, lista_de_bilhetes_processo
    lista_elementos_do_processo = processo.split("|")
    nome_do_processo.append(lista_elementos_do_processo[0])
    tempo_de_cada_processo.append(int(lista_elementos_do_processo[2]))
    lista_de_bilhetes_processo.append(int(lista_elementos_do_processo[3]))

def loteria(lista_linhas):
    global nome_do_processo, tempo_de_cada_processo, lista_de_bilhetes_processo,cpu
    global total_de_bilhetes, lista_bilhetes_teto,lista_de_bilhetes,tempo_decorrido,Nome,Tempo
    
    loteria, cpu = lista_linhas[0].split("|")
    lista_linhas.remove(lista_linhas[0])
    cpu = int(cpu)
    #pegando os dados inceridos
    for linha in lista_linhas:
        lista_elementos_do_processo = linha.split("|")
        nome_do_processo.append(lista_elementos_do_processo[0])
        tempo_de_cada_processo.append(int(lista_elementos_do_processo[2]))
        lista_de_bilhetes_processo.append(int(lista_elementos_do_processo[3]))

    #total de bilhetes 
    for i in lista_de_bilhetes_processo:
        total_de_bilhetes+=i
    

    #lista de bilhetes
    if lista_de_bilhetes==None:
        i=1 
    else:
        i=len(lista_de_bilhetes)+1
    while i<=total_de_bilhetes:
        lista_de_bilhetes.append(i)
        i+=1
    
    #limite superior de cada processo para achar o bilhete
    p = 0 #posição na lista de processos
    contador_de_bilhetes=None
    while total_de_bilhetes>0:
        if contador_de_bilhetes ==None:
            contador_de_bilhetes = lista_de_bilhetes_processo[p]
        else:
            contador_de_bilhetes += lista_de_bilhetes_processo[p]
        lista_bilhetes_teto.append(contador_de_bilhetes)
        total_de_bilhetes-=lista_de_bilhetes_processo[p]
        p+=1
    

    #definindo processo a ser executado
    
    while len(tempo_de_cada_processo)>0:
        
        #escolhe bilhete
        escolha = None
        escolha = random.randint(0,len(lista_de_bilhetes)-1)

        bilhete = lista_de_bilhetes [escolha]
        print("Bilhete sorteado: ",bilhete)

        #encontrar o processo a partir do intervalo 
        contador_de_intervalo = 0 
        for i in lista_bilhetes_teto:
            if bilhete > i:
                contador_de_intervalo+=1
        print("Nome: ",nome_do_processo[contador_de_intervalo])
        
        tempo = tempo_de_cada_processo[contador_de_intervalo]
        print("Tempo restante: ", tempo)
        
        if  tempo>0:
            tempo-=cpu
            print("Tempo atualizado do processo: ",tempo)
            tempo_decorrido+=cpu
        tempo_de_cada_processo[contador_de_intervalo] = tempo
        print("Processos restantes: ",len(tempo_de_cada_processo))
        print("\n\n")
        time.sleep(1)
        if tempo_de_cada_processo[contador_de_intervalo] <=0:
            Nome.append(nome_do_processo[contador_de_intervalo])
            Tempo.append(tempo_decorrido)
            del(tempo_de_cada_processo[contador_de_intervalo])
            del(lista_de_bilhetes_processo[contador_de_intervalo])
            del(lista_bilhetes_teto[contador_de_intervalo])
            #substiturir pela função total de bilhetes
            total_de_bilhetes = 0
            #total de bilhetes 
            for i in lista_de_bilhetes_processo:
                total_de_bilhetes+=i
            
            lista_de_bilhetes=[]
            #lista de bilhetes
            if lista_de_bilhetes==None:
                i=1 
            else:
                i=len(lista_de_bilhetes)+1
            while i<=total_de_bilhetes:
                lista_de_bilhetes.append(i)
                i+=1
