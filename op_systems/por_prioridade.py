import time

#Encontra o tipo da lista
def type_alg():
  list_of_process = ler_arq()
  type_my_alg = list_of_process[0]
  selection = type_my_alg.split("|")
  return selection

#lista de listas
def list_of_list(lista):
  arq = lista
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
def org_priority(lista):
  my_list = list_of_list(lista)
  my_list_sorted = sorted(my_list, key = lambda x:(x[3], x[2]))
  return my_list_sorted

def select_priority():
    global global_list
    first_priority = global_list[0][3]
    list_element_priority = []
    for element in global_list:
        if element[3] == first_priority:
          list_element_priority.append(element)
        else:
          break
    for process in list_element_priority :
      global_list.remove(process)
    return list_element_priority

def tim(period, list_sorted):
  while len(list_sorted):
    time.sleep(1)
    for process in list_sorted:
        process[2] -= int(period)
        repre(process)
        if process[2] <= 0:
          list_sorted.remove(process)

def repre(process):
  element_list = process
  if element_list[2] >= 0:
    print( ' ID Process: ' +  str(element_list[1]) + ' Priority: ' +  str(element_list[3]) +' Time left: ' + str(element_list[2]))

#função principal
def porPrioridade(lista_de_linhas):
  minha_lista = list_of_list(lista_de_linhas)
  if (minha_lista[0] == 'prioridade'):
    period = alg_esc[1]
    while len(global_list) > 0:
        tim(period, select_priority())
    print(global_list)
    

  
global_list_aux = org_priority(lista)
global_list = global_list_aux
main()
