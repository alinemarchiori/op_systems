

#Transforma o arquivo em uma lista
def ler_arq():
  arq = open('prioridades.txt', 'r')
  lista = arq.readlines()
  new_lista =[]
  for linha in lista:
    linha = linha.rstrip('\n')
    new_lista.append(linha)
  arq = arq.close()
  return new_lista

#Encontra o tipo da lista
def type_alg():
  list_of_process = ler_arq()
  type_my_alg = list_of_process[0]
  selection = type_my_alg.split("|")
  return selection

#lista de listas
def list_of_list():
  arq = ler_arq()
  arq.pop(0)
  new_list =[]
  tam = len(arq)
  for i in range(tam):
    new_list.append([arq[i]])
  arq = []
  for i in range(tam):
    aux = new_list[i]
    aux_1 = aux[0]
    arq.append(aux_1.split("|"))
  for i in arq:
    i[1],i[2],i[3],i[4],i[5] = int(i[1]),int(i[2]),int(i[3]),int(i[4]),int(i[5])
  return arq

#organizando por prioridade e por menor tempo
def org_priority():
  my_list = list_of_list()
  my_list_sorted = sorted(my_list, key = lambda x:(x[3], x[2]))
  return my_list_sorted

def temp(period):
    list_sorted = select_priority()
    print(list_sorted)
    #for process in list_sorted:
     #   process[2] -= int(period)
      #  repre(process)
       # if process[2] <= 0:
        #    break

def select_priority():
    list_sorted = org_priority()
    first_priority = list_sorted[0][3]
    list_element_priority = []
    for element in list_sorted:
        if element[3] == first_priority:
            list_element_priority.append(element)
            print(list_element_priority)
            global_list.remove(element)   
        else:
            break
    return list_element_priority

def repre(process):
  element_list = process
  print('Process Number: ' + element_list[0] + ' ID Process: ' +  str(element_list[1]) + 'Period:' + str(element_list[2]))

#função principal
def main():
  alg_esc = type_alg()
  if (alg_esc[0] == 'prioridade'):
    period = alg_esc[1]
    while len(global_list) >= 0:
        temp(period)
    

  
global_list_aux = org_priority()
global_list = global_list_aux
main()