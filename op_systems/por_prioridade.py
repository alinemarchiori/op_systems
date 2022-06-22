import time
from classes import*

#variáveis globais
lista_processos = []
lista_ordenada  = []
lista_de_processos_para_mostrar_o_tempo = []
termina_loop_thread_2 = True
tempo_total = 0

def getNumeroProcessosFaltantes():
    print(f'Processos em espera: {len(lista_ordenada)}\n')

#ordena a lista de processos de acordo com a prioridade, números menoressão mais prioritários
# se tiverem prioridades iguais é levado em consideração o tempo que restante de execução
def ordena_a_lista():
  global lista_ordenada
  lista_ordenada = sorted(lista_processos, key = lambda x:(x.prioridade, x.tempo_execucao))

# cria um novo processo em tempo de execução, lendo dados do terminal 
# e trata caso o processo não seja válido, além de ordenar a lista de processos 
# novamente, sempre que um processo novo é executado
def criaProcesso_por_prioridade():
  global lista_processos, lista_de_processos_para_mostrar_o_tempo, termina_loop_thread_2

  while True:
    try:
      processo = input()
      objeto_processo = Processo()
      objeto_processo.setDetalhesProcesso(processo.split('|'))
      lista_processos.append(objeto_processo)
      lista_de_processos_para_mostrar_o_tempo.append(objeto_processo)
      ordena_a_lista()

    except:
      if processo == 'sair' or processo == 'Sair':
        termina_loop_thread_2 = False
        break
      else:
        print("processo invalido")

# organiza os processos em uma lista e instancia a classe para cada processo
def listaProcessos(lista_linhas):
  global lista_processos, lista_de_processos_para_mostrar_o_tempo

  for processo in lista_linhas:
    objeto_processo = Processo()
    objeto_processo.setDetalhesProcesso(processo.split('|'))
    lista_processos.append(objeto_processo)
    lista_de_processos_para_mostrar_o_tempo.append(objeto_processo)

#com a lista já ordenada ele pega a primeira prioridade do primeiro processo da 
# lista e define que ela que vai ser executada, criando uma lista com todos os 
# processos que tem aquela prioridade para que eles sejam executados até acabarem
# se a prioridade de dois processos foram iguais ele ordena esses dois pelo tempo
def define_prioridade():
  global lista_ordenada, lista_processos
  print(lista_ordenada[0].prioridade)
  minha_prioridade = lista_ordenada[0].prioridade
  elementos_prioritarios = []

  for objeto_do_processo in lista_ordenada:
    if objeto_do_processo.prioridade == minha_prioridade:
      elementos_prioritarios.append(objeto_do_processo)
    else:
      break

  for objeto_do_processo in elementos_prioritarios:
    lista_processos.remove(objeto_do_processo)
    lista_ordenada.remove(objeto_do_processo)

  return elementos_prioritarios

# algoritmo
def porPrioridade(lista_de_linhas):
  global tempo_total
  #retira a primeira linha do arquivo, que tem o tempo de cpu e o nome do algoritmo
  prioridade, tempo_de_CPU = lista_de_linhas[0].split("|")
  lista_de_linhas.remove(lista_de_linhas[0])
  #chama a função passando apenas as linhas que tem processos e ordena a lista
  listaProcessos(lista_de_linhas)
  ordena_a_lista()
  #loop que serve para executar um processo mesmo que os outros já tenham acabado
  while termina_loop_thread_2:
    #verifica se tem algum processo para ser executado ainda
    if len(lista_processos) > 0:
      #chama a função para definir a prioridade
      lista_elementos_prioritarios = define_prioridade()
      # loops que executam todos os processos de mesma prioridade
      while len(lista_elementos_prioritarios) > 0:
        for processo in lista_elementos_prioritarios:
          tempo_total += int(tempo_de_CPU)
          processo.atualizaTempo(int(tempo_de_CPU))
          processo.atualizaTempoDemoradoPrioridade(tempo_total)
          print(processo)
          time.sleep(1)
          if processo.getTempo() <= 0:
            lista_elementos_prioritarios.remove(processo)
          getNumeroProcessosFaltantes()
        
  return lista_de_processos_para_mostrar_o_tempo