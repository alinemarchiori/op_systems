import time
from classes import*

lista_processos = []
lista_ordenada  = []
lista_de_processos_para_mostrar_o_tempo = None

def getNumeroProcessosFaltantes():
    print(f'Processos em espera: {len(lista_ordenada)}\n')

def ordena_a_lista():
  global lista_ordenada
  lista_ordenada = sorted(lista_processos, key = lambda x:(x.prioridade, x.tempo_execucao))

def criaProcesso():
    processo = input()
    global lista_processos
    objeto_processo = Processo()
    objeto_processo.setDetalhesProcesso(processo.split('|'))
    lista_processos.append(objeto_processo)
    lista_de_processos_para_mostrar_o_tempo.append(objeto_processo)
    ordena_a_lista()

def listaProcessos(lista_linhas):
  global lista_processos
  for processo in lista_linhas:
    objeto_processo = Processo()
    objeto_processo.setDetalhesProcesso(processo.split('|'))
    lista_processos.append(objeto_processo)

def define_prioridade():
  global lista_ordenada, lista_processos
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

def porPrioridade(lista_de_linhas):
  global lista_de_processos_para_mostrar_o_tempo
  prioridade, tempo_de_CPU = lista_de_linhas[0].split("|")
  lista_de_linhas.remove(lista_de_linhas[0])
  listaProcessos(lista_de_linhas)
  lista_de_processos_para_mostrar_o_tempo = lista_processos
  ordena_a_lista()
  while len(lista_processos) > 0:
    lista_elementos_prioritarios = define_prioridade()
    while len(lista_elementos_prioritarios) > 0:
      for processo in lista_elementos_prioritarios:
          processo.atualizaTempo(int(tempo_de_CPU))
          print(processo)
          time.sleep(1)
          if processo.getTempo() <= 0:
            lista_elementos_prioritarios.remove(processo)
          getNumeroProcessosFaltantes()
  return lista_de_processos_para_mostrar_o_tempo
