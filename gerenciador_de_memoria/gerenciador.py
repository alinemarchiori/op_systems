tempo = 0

class Pagina:
    def __init__(self, nome):
        self.nome = nome
        self.tempo_inicial_na_memoria = 0
        self.tempo_final_na_memoria = 0

    def set_tempo_inicial(self, tempo):
        self.tempo_inicial_na_memoria = tempo

    def zera_tempo(self):
        self.tempo_inicial_na_memoria = 0
        self.tempo_final_na_memoria = 0

    def get_tempo(self, tempo):
        self.tempo_final_na_memoria = tempo
        return self.tempo_final_na_memoria - self.tempo_inicial_na_memoria

    def __repr__(self) -> str:
        return f'Pagina: {self.nome}'

def FIFO_beatriz(linha):
    numero_molduras, numero_paginas, ordem_acesso = organiza_linha(linha) #pega numero de molduras, paginas e a ordem que são acessadas do arquivo
    moldura = [None]*numero_molduras #lista de molduras
    posicao = 0 #posição na lista de molduras  
    posicao2 = 0 #posição na lista de paginas 
    trocas = 0
    chave = 0 

    while True:
        
        if posicao >= numero_molduras: #reseta posição na lista de molduras 
            posicao = 0 
        
        chave = 0
        for i in moldura:#verifica se a pagina já está na lista de molduras 
            
            if i == ordem_acesso[posicao2]:
                chave+=1
                
        if chave == 0:# se não está ela entra na lista de molduras 
            moldura[posicao] = ordem_acesso[posicao2] 
            posicao+=1
            trocas +=1
        posicao2+=1

        
        if posicao2 >= len(ordem_acesso): #finaliza o looping quando chega no final da lista de paginas
            break
    return trocas


def MRU_aline(linha): 
    quantidade_molduras, quantidade_paginas, referencias = organiza_linha(linha)
    tabela_de_paginas = [Pagina(nome) for nome in range(1, quantidade_paginas + 1)]
    mapa_de_bits = []
    numero_de_trocas_de_paginas = 0
    global tempo

    #para cada uma das referencias da lista de referencias é realizada
    #a verificação se a página está ou não na memória
    for referencia in referencias:
        pagina_em_questao = tabela_de_paginas[referencia - 1]
        
        #verifica se a página já está na memória
        if pagina_em_questao in mapa_de_bits:
            pagina_em_questao.set_tempo_inicial(tempo)
        
        #se não estiver, verifica se a memória está cheia e insere a página na memória
        elif len(mapa_de_bits) < quantidade_molduras:
            mapa_de_bits.append(pagina_em_questao)
            pagina_em_questao.set_tempo_inicial(tempo)
            numero_de_trocas_de_paginas += 1

        #caso a memória estiver cheia, é necessário fazer a troca de páginas
        elif len(mapa_de_bits) >= quantidade_molduras:
            pagina_a_ser_removida = mapa_de_bits[0]
            tempo_na_memoria = 0

            #loop que verifica qual das páginas está a mais tempo na memória e guarda ela
            for pagina in mapa_de_bits:
                
                if pagina.get_tempo(tempo) > tempo_na_memoria:
                    tempo_na_memoria = pagina.get_tempo(tempo)
                    pagina_a_ser_removida = pagina
                    #print(mapa_de_bits, pagina, pagina.get_tempo(), pagina_em_questao)
            
            #depois de encontrar a página a ser removida, é zerado o tempo dela e 
            #ela é substituída da memória pela página que está sendo referenciada
            pagina_a_ser_removida.zera_tempo()
            mapa_de_bits.remove(pagina_a_ser_removida)
            mapa_de_bits.append(pagina_em_questao)
            pagina_em_questao.set_tempo_inicial(tempo)
            numero_de_trocas_de_paginas += 1

        tempo += 1
 
    return numero_de_trocas_de_paginas


def NUF_cris():
    pass


def OTIMO_breno(linha):
  #Função para zerar páginas já usadas 
  def zera_elemento(pagina):
    pag = tabela_paginas.index(pagina)
    tabela_paginas[pag] = 0
    return

  #Função para retornar a pagina mais distante
  def encontra_pagina_distante(tabela_de_molduras, tabela_paginas):
        maior_tempo_e_pagina = [0,0]
        #Loop para encontrar a página que será usada daqui mais tempo
        for Mold_pagina in tabela_de_molduras:
          contador = 0
          if (Mold_pagina not in tabela_paginas):
              maior_tempo_e_pagina[1] = Mold_pagina
              return maior_tempo_e_pagina[1]
          for Pag_pagina in tabela_paginas:
            if (Pag_pagina == 0):
              contador = 0
            else:
              contador += 1
              if (Mold_pagina == Pag_pagina):
                if (contador > maior_tempo_e_pagina[0]):
                  maior_tempo_e_pagina[0] = contador - 1
                  maior_tempo_e_pagina[1] = Mold_pagina
                  break
                else:
                  break
       
        return maior_tempo_e_pagina[1]

  quantidade_molduras, quantidade_paginas, tabela_paginas = organiza_linha(linha)
  tabela_de_molduras = [ 0 for pagina in range(1, quantidade_molduras + 1)]
  trocas = 0

  for pagina in tabela_paginas:

    #Verifica se existe espaço vazio na memória
    if (0 in tabela_de_molduras):
      #Se existir, e a página ainda não está na memória, inclui a página na memória e incrementa a troca
      #Zera as páginas que já foram para a memória
      if (pagina not in tabela_de_molduras):
        for index in range(len(tabela_de_molduras)):
          if (tabela_de_molduras[index] == 0):
            tabela_de_molduras[index] = pagina
            zera_elemento(pagina)
            trocas += 1 
            break 
          else:
            pass
      #Se existir, mas a página já está na memória, zera na lista de páginas
      else:
        zera_elemento(pagina)
    
    #Se não existir espaço vazio, verifica se a página já está na memória
    else:
      #Se já estiver, zera na lista de páginas
      if (pagina in tabela_de_molduras):
        zera_elemento(pagina)

      #Se não estiver, haverá a troca
      else:
        melhor_substituicao = encontra_pagina_distante(tabela_de_molduras, tabela_paginas)
        index_troca = tabela_de_molduras.index(melhor_substituicao)
        tabela_de_molduras[index_troca] = pagina
        trocas += 1
        zera_elemento(pagina)

  return trocas



#recebe uma linha em string e retorna a quantidade de molduras, quantidade de paginas 
#e uma lista de inteiros que correspondem às referências das paginas durante a 
#execução do processo
def organiza_linha(linha):
    quantidade_molduras, quantidade_paginas, referencias = linha.split('|') 
    referencias = referencias.split(' ') 
    return (
        int(quantidade_molduras), 
        int(quantidade_paginas), 
        [int(referencia) for referencia in referencias]
    )


#função para formatar a saída
def mostra_na_tela(lista, menor_valor):
    nomes = ['FIFO', 'MRU', 'NUF']
    return (
        f'{lista[0]}|{lista[1]}|{lista[2]}|{lista[3]}|{nomes[lista.index(menor_valor)]}'
    )


#função que lê o arquivo e retorna uma lista das linhas
def leArquivo(nomedoarquivo):
    arquivo = open(nomedoarquivo,'r')
    linhas = arquivo.readlines()
    return linhas


def main():
    arquivo =  leArquivo("arquivos_entrada_e_saida\\inMemoria.txt")

    for linha in arquivo:
        '''
        #chama todas as funções passando a linha com os dados
        fifo = FIFO_beatriz()
        mru = MRU_aline()
        nuf = NUF_cris()
        otimo = OTIMO_breno()
        '''
        #apenas para fins de teste
        fifo = FIFO_beatriz(linha)
        mru = MRU_aline(linha)
        nuf = 100
        otimo = OTIMO_breno(linha)

        # armazena os resultados em uma lista
        lista_trocas_por_processo = [fifo, mru, nuf, otimo]

        #pega o menor valor da lista excluindo o ótimo
        menor_valor = min(lista_trocas_por_processo[:3])

        #verifica se deu empate
        if lista_trocas_por_processo[:3].count(menor_valor) > 1:
            print(f'{fifo}|{mru}|{nuf}|{otimo}|empate')
        
        else:
            print(mostra_na_tela(lista_trocas_por_processo, menor_valor))
            
main()           
