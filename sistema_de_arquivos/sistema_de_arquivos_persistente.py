#O seu disco rígido possui uma capacidade de 256MB 
#Os blocos para armazenamento de dados possuem 4KB. 

from datetime import datetime
import os.path

# no dicionario abaixo são guardados os inodes e os blocos,
# cada inode gasta 2 KB de memória, e o sistema
# reserva espaço para 2500 inodes e 62500 blocos de 4 KB
gerenciamento_inodes = {}
gerenciamento_blocos = {} 

# A ideia por trás do dicionário é ter a chave dos blocos e dos inodes
# sendo o endereço deles na memória, as posições começam 
# no zero e vão até o final da quantidade de memória disponível, 
# facilitando o acesso e a busca tendo uma complexidade constante

# QUESTÕES IMPORTANTES
# quanto de arquivo cabe em cada inode?
# 2264 KB ou 2264000 bytes ou 566 endereços

# quantos inodes eu preciso ter para endereçar toda a memória
# foram separados 5000 KB para armazenar os inodes 
# equivalendo a 2500 inodes

# quantos blocos e quanta memoria para blocos?
# 250 MB = 250000 KB = 62500 blocos de 4 KB

# quanto de memória minha tabela de inodes e blocos livres vai ocupar?
# 2500   caracteres (0's = livre ou 1's = ocupado) para os inodes
# 60000 caracteres (0's = livre ou 1's = ocupado) para os blocos
# Resultando em 62500 bytes na memmória = 63 KB

# nesta lista são armazenadas as informações de quais blocos 
# estão livres e quais estão ocupados, sendo uma matriz de zeros e uns
class Tabela:
    def __init__(self) -> None:    
        self.tabela_inodes_e_blocos_livres_ocupados = ["0"]*62500

    def setOcupado(self, indice = int):
        self.tabela_inodes_e_blocos_livres_ocupados[indice] = "1"

    def setLivre(self, indice = int):
        self.tabela_inodes_e_blocos_livres_ocupados[indice] = "0"

    def getPosicaoLivreInode(self):
        for posicao in range(0, 2500):
            if self.tabela_inodes_e_blocos_livres_ocupados[posicao] == "0":
                return posicao
        return None
    
    def getPosicaoLivreBloco(self):
        for posicao in range(2500, len(self.tabela_inodes_e_blocos_livres_ocupados)):
            if self.tabela_inodes_e_blocos_livres_ocupados[posicao] == "1":
                return posicao
        return None

    def transformaTabelaemString(self):
        return " ".join(self.tabela_inodes_e_blocos_livres_ocupados)

'''
Nome do arquivo/diretório ..............-> 128 caracteres -> 128 bytes
Diretório ou arquivo ...................-> 1 caracteres   -> 1 bytes
Criador  ...............................-> 44 caracteres  -> 44 bytes
Dono  ..................................-> 40 caracteres  -> 40 bytes
Tamanho ................................-> numero inteiro -> 4 bytes
Data de criação ........................-> 16 caracteres  -> 16 bytes
Data de modificação ....................-> 16 caracteres  -> 16 bytes
Permissões de acesso ...................-> 50 caracteres  -> 50 bytes
TOTAL DO INODE por enquanto...............................-> 300 bytes

Sobraram 1700 bytes 
Se usar um inteiro para endereçar 425 endereços de blocos ou outros inodes
Equivalendo a um arquivo de 1700 Kb ou 1700000 bytes 
                        OU 
Equivalendo a um diretório que aponta para 425 inodes(diretorios/arquivos)

# Se for DIRETÓRIO
Apontadores para blocos ................-> 0 KB
Apontador para eventual outro i-node ...-> 1700 KB

# Se for arquivo
Apontadores para blocos ................-> definir conforme o uso
Apontador para eventual outro i-node ...-> definir conforme o uso

TOTAL DO INODE ...........................................-> 2000 bytes = 2 KB
'''

USER = ''
TABELA = Tabela()
caminho_atual_str = 'raiz/'
caminho_endereco = 0
caminho_memoria_diretorio_atual = 0


def cria_inodes_blocos():
    global gerenciamento_inodes, gerenciamento_blocos
    if not (os.path.isfile('sistema.json')):
        for i in range(2500):
            gerenciamento_inodes[i] = []

        for j in range(2500, 62500):
            gerenciamento_blocos[j] = ''
    

def calcula_tamanho(string = str) -> int:
    pass


def verifica_se_tem_extensao(nome):  
    if nome.endswith('.txt'):
        return 'a'
    return 'd'


def corta_conteudo(string = str) -> list:
    return [string[i:4000+i:] for i in range(0,len(string),4000)]


def aloca_blocos(lista_blocos = list) -> list:
    global TABELA, gerenciamento_blocos
    enderecos = []

    for conteudo in lista_blocos:
        posicao_livre = TABELA.getPosicaoLivreInode()
        enderecos.append(posicao_livre)
        TABELA.setOcupado(posicao_livre)
        gerenciamento_blocos[posicao_livre] = conteudo

    return enderecos


def verifica_se_arquivo_existe():
    pass


# O inode contêm a seguinte estrutura:
'''
Nome do arquivo/diretório .......................0
Diretorios anteriores ...........................1
Variavel que indica se é arquivo ou diretório ...2
Criador .........................................3
Dono ............................................4
Tamanho .........................................5
Data de criação .................................6
Data de modificação .............................7
Permissões de acesso ............................8
Tamanho do arquivo ..............................9
Apontadores para blocos/inodes ..................10
'''


def add_info_inode(
        endereco_memoria = int,
        nome = str,
        diretorio_ou_arquivo = str,
        caminho = str,
        data_de_criacao = str,
        data_de_modificacao = str,
    ):
    
    tamanho = 2000 #bytes (tamanho do inode)
    gerenciamento_inodes[endereco_memoria] = [
            nome, 
            caminho,
            diretorio_ou_arquivo,
            USER, 
            "system", 
            data_de_criacao, 
            data_de_modificacao, 
            USER, 
            tamanho,
            []
        ]
    #print(gerenciamento_inodes[endereco_memoria])


def data_hora_atual():
    data_e_hora_atuais = datetime.now()
    data_de_criacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    data_de_modificacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    return data_de_criacao, data_de_modificacao


def inicia_sistema_do_zero():
    global caminho_atual_str, caminho_endereco, caminho_memoria_diretorio_atual, TABELA
    cria_inodes_blocos()

    data_de_criacao, data_de_modificacao = data_hora_atual()
    caminho_atual_str = 'raiz/' # caminho até o arquivo
    caminho_endereco = 0        # endereco na memoria onde o diretorio atual está
    caminho_memoria_diretorio_atual = 0
    TABELA.setOcupado(0)

    add_info_inode(
        caminho_endereco, 
        'raiz', 
        'd',
        caminho_atual_str, 
        data_de_criacao, 
        data_de_modificacao
        )


def add_endereco_no_diretorio(endereco_arquivo_ou_diretorio):
    global gerenciamento_inodes
    conteudo_inode = gerenciamento_inodes[caminho_memoria_diretorio_atual]
    conteudo_inode[-1].append(endereco_arquivo_ou_diretorio)


def main():
    global USER, caminho_atual_str, caminho_endereco, caminho_memoria_diretorio_atual
    USER = input("Digite o nome do usuário: ")

    if not (os.path.isfile('sistema.json')):
        inicia_sistema_do_zero()

    while True:
        print(gerenciamento_inodes)
        #print(gerenciamento_blocos)
        comando = input(gerenciamento_inodes[caminho_memoria_diretorio_atual])
        print()
        comando_separado = comando.split(' ')
        nome = comando_separado[1]
        
        
        # comandos sobre arquivos
        # Criar arquivo (touch arquivo) 
        if comando_separado[0] == "touch":
            
            if not nome.endswith('.txt'):
                nome += '.txt'

            caminho_endereco = TABELA.getPosicaoLivreInode()
            TABELA.setOcupado(caminho_endereco)
            data_de_criacao, data_de_modificacao = data_hora_atual()

            add_info_inode(
                caminho_endereco, # endereco na memoria onde o diretorio atual está
                nome, 
                'a',
                caminho_atual_str, 
                data_de_criacao, 
                data_de_modificacao
            )
            # adiciona endereco do arquivo no inode do diretorio
            add_endereco_no_diretorio(caminho_endereco)

            
        # Remover arquivo (rm arquivo)
        elif comando_separado[0] == "rm": #TODO: arrumar
            if gerenciamento_inodes[nome]:
                gerenciamento_inodes.pop(nome)
            
            else:
                print('Erro : O arquivo ' + nome + ' não existe')
                        
        # Escrever no arquivo (echo "conteudo legal" >> arquivo)
        elif comando.startswith("echo"): #TODO: arrumar
            #verifica_se_o_arquivo_existe_no_diretorio(comando_separado[-1], atual)
            pass

        # Ler arquivo (cat arquivo)
        elif comando_separado[0] == "cat": #TODO: arrumar
            if gerenciamento_inodes[nome]:
                print(gerenciamento_inodes[nome][-1])
            else:
                print('Erro : O arquivo ' + nome + ' não existe')

        # Copiar arquivo (cp arquivo1 arquivo2)
        elif comando_separado[0] == "cp": #TODO: arrumar
            if gerenciamento_inodes[nome]:
                nome_atual = comando_separado[2]
                conteudo_anterior = gerenciamento_inodes.pop(nome)
                gerenciamento_inodes[nome_atual] = conteudo_anterior
                gerenciamento_inodes[nome] = conteudo_anterior

            
        # Renomear arquivo (mv arquivo1 arquivo2)
        elif comando_separado[0] == "mv": #TODO: arrumar
            if gerenciamento_inodes[nome]:
                if not gerenciamento_inodes[comando_separado[2]]:
                    nome_atual = comando_separado[2]
                    conteudo_anterior = gerenciamento_inodes.pop(nome)
                    gerenciamento_inodes[nome_atual] = conteudo_anterior
                else:
                     print('Erro: O nome ' + comando_separado[2] + ' já está em uso')
                
        
        # comandos sobre diretorios
        # Criar diretório (mkdir diretorio)
        elif comando.startswith("mkdir"): #TODO: arrumar
            diretorio_novo = comando_separado[1]
            a =  0
            if atual.nome_atual != diretorio_novo:
                
                for i in atual.proximos_diretorios:
                    
                    if i.nome_atual == diretorio_novo:
                        a = 1
                        print('diretório existente')
                        break
                    
                if a == 0 :
                    atual.criaDiretorio(diretorio_novo)

            else:
                print('diretório existente')
            
        
        # Remover diretório (rmdir diretorio) - só funciona se diretório estiver vazio
        elif comando.startswith("rmdir"): #TODO: arrumar
            diretorio_novo = comando_separado(1)
        # Listar o conteúdo de um diretório (ls diretório)
        elif comando.startswith("ls"): #TODO: arrumar
            pass
        # Trocar de diretório (cd diretorio) *Não esquecer dos arquivos especiais . e ..
        elif comando.startswith("cd"): #TODO: arrumar
            #TODO em algum momento atualizar a variavel atual
            atual = '' #nome do diretorio buscado
        # Renomear diretorio (mv diretorio1 diretorio2) 
        elif comando.startswith("mv"): #TODO: arrumar
            pass


main()