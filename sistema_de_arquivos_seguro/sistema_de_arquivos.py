#O seu disco rígido possui uma capacidade de 256MB 
#Os blocos para armazenamento de dados possuem 4KB. 

from datetime import datetime
import os.path
#import pickle
import pickle
import os
import hashlib


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
            if self.tabela_inodes_e_blocos_livres_ocupados[posicao] == "0":
                return posicao      
        return None

    def transformaTabelaemString(self):
        return " ".join(self.tabela_inodes_e_blocos_livres_ocupados)

    def transformaStringemTabela(self, string):
        self.tabela_inodes_e_blocos_livres_ocupados = string.split(" ")

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
caminho_atual_str = 'home/'
caminho_endereco = 0
caminho_memoria_diretorio_atual = 0

def gera_sal():
    return os.urandom(32)

def criptografa_senha(senha, sal):
    return hashlib.pbkdf2_hmac('sha512', senha.encode('utf-8'), sal, 100000)

def ler_arquivo(nome, binario=False):
    global gerenciamento_blocos, gerenciamento_inodes, lista_enderecos_blocos
    if verifica_se_arquivo_existe(nome):
        conteudo_inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
        lista_enderecos_blocos = conteudo_inode_arquivo[-1]
        if not binario:
            return ''.join(map(str, [gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos]))
        else:
            #print(gerenciamento_blocos[lista_enderecos_blocos[0]])
            return b''.join([gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos])
    else:
        print('Erro : O arquivo ' + nome + ' não existe')

def ler_arquivo_de_senhas():
    conteudo = []
    indices = range(len(ler_arquivo_de_usuarios()))
    for indice in indices:
        conteudo.append(ler_arquivo(f'shadow_{indice}.txt', binario=True))
    return conteudo

def ler_senha_e_sal(lista_de_senhas, indice):
    #senha_criptografada_e_sal = lista_de_senhas[indice]
    senha_criptografada_e_sal = ler_arquivo(f"shadow_{indice}.txt", binario=True)
    #print(senha_criptografada_e_sal)
    sal = senha_criptografada_e_sal[:32]
    senha_criptografada = senha_criptografada_e_sal[32:]
    return senha_criptografada, sal

def escrever_no_arquivo(nome, conteudo, binario=False):
    global gerenciamento_inodes
    global gerenciamento_blocos
    global lista_enderecos_blocos
    conteudo_arquivo = conteudo
    '''conteudo_arquivo = ''
    copiar = 0
    for caracter in conteudo:               
        if caracter == '"' or caracter == "'":
            copiar += 1
        if copiar == 1:
            conteudo_arquivo += caracter
    conteudo_arquivo += '"'''
    conteudo_novo = ''
    conteudo_existente = ''
    if verifica_se_arquivo_existe(nome):
        inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
        lista_enderecos_blocos = inode_arquivo[-1]
        if len(inode_arquivo[-1]) > 0:
            if not binario:
                conteudo_novo = ''
                conteudo_existente = ''
                conteudo_existente = ''.join(map(str, [
                    gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos
                ]))
                conteudo_novo = conteudo_arquivo
                conteudo_arquivo = conteudo_existente + "\n" + conteudo_novo
            else:
                conteudo_novo = b''
                conteudo_existente = b''
                conteudo_existente = b''.join(map(bytes, [
                    gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos
                ]))
                conteudo_novo = conteudo_arquivo
                conteudo_arquivo = conteudo_existente + conteudo_novo
            
            desaloca_blocos(lista_enderecos_blocos)
            lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo))
        else:
            lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo))
        if len(lista_enderecos) <= 425:
            muda_data_modificacao(verifica_se_arquivo_existe(nome))
            inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
            del inode_arquivo[-1]
            inode_arquivo.append(lista_enderecos)
            gerenciamento_inodes[verifica_se_arquivo_existe(nome)] = inode_arquivo
            muda_tamanho_arquivo(verifica_se_arquivo_existe(nome))
            escreveNaMemoria()
        else:
            desaloca_blocos(lista_enderecos)
            print("Você excedeu o tamanho máximo permitido de arquivo.")
    else:
        print('Erro : O arquivo ' + nome + ' não existe. Crie o arquivo antes de escrever.')

def salva_senha_no_arquivo(senha_original, indice_usuario):
    sal = gera_sal()
    senha_criptografada = criptografa_senha(senha_original, sal)
    escrever_no_arquivo(f'shadow_{indice_usuario}.txt', sal + senha_criptografada, binario=True)

def criar_arquivo(nome, criador=USER, permissoes="00", dono=USER):
    global gerenciamento_blocos, gerenciamento_inodes, TABELA
    if not nome.endswith('.txt') and not nome.endswith('.bin'):
        nome += '.txt'
    if verifica_se_arquivo_existe(nome):
        print("Arquivo já existe")
    else:
        caminho_endereco = TABELA.getPosicaoLivreInode()
        TABELA.setOcupado(caminho_endereco)
        data_de_criacao, data_de_modificacao = data_hora_atual()

        add_info_inode(
            caminho_endereco, # endereco na memoria onde o arquivo está
            nome,
            caminho_atual_str, 
            data_de_criacao, 
            data_de_modificacao,
            criador,
            permissoes,
            dono
        )
        # adiciona endereco do arquivo no inode do diretorio
        add_endereco_no_diretorio(caminho_endereco)
        escreveNaMemoria()

def criar_diretorio(nome, criador=USER, permissoes="00", dono=USER):
    global caminho_atual_str, TABELA, gerenciamento_inodes, gerenciamento_blocos
    diretorio_novo = nome
    if nome.endswith('.txt'):
        print("Erro: nome do diretorio não pode conter extensão .txt")
    else:
        if verifica_se_arquivo_existe(diretorio_novo):
            print("Erro: diretório já existe")
        else:
            caminho_endereco = TABELA.getPosicaoLivreInode()
            TABELA.setOcupado(caminho_endereco)
            data_de_criacao, data_de_modificacao = data_hora_atual()

            add_info_inode(
                caminho_endereco, # endereco na memoria onde o arquivo está
                diretorio_novo,
                caminho_atual_str+f"{nome}/",
                data_de_criacao, 
                data_de_modificacao,
                criador,
                permissoes,
                dono
            )
            # adiciona endereco do arquivo no inode do diretorio
            add_endereco_no_diretorio(caminho_endereco)
            #caminho_memoria_diretorio_atual = caminho_endereco
            #caminho_atual_str = caminho_atual_str+f"{nome}/"
            #caminho_atual_diretorio_string = verifica_se_arquivo_existe(diretorio_novo)
            escreveNaMemoria()

def criar_usuario(usuario, senha):
    escrever_no_arquivo('passwd.txt', usuario)
    indice = len(ler_arquivo_de_usuarios()) - 1
    criar_arquivo(f"shadow_{indice}.txt", criador='root', permissoes='root')
    salva_senha_no_arquivo(senha, indice)
    criar_diretorio(usuario, usuario, "00", usuario)

def ler_arquivo_de_usuarios():
    conteudo = ler_arquivo('passwd.txt')
    return conteudo.strip().split('\n')

def verifica_se_usuario_existe(usuario, lista_de_usuarios):
    return usuario in lista_de_usuarios

def indice_de_usuario(usuario, lista_de_usuarios):
    return lista_de_usuarios.index(usuario)

def autentica_usuario(usuario, senha, lista_de_usuarios, lista_de_senhas):
    indice_usuario = indice_de_usuario(usuario, lista_de_usuarios)
    senha_correta_criptografada, sal = ler_senha_e_sal(lista_de_senhas, indice_usuario)
    #print('senha correta criptografada', senha_correta_criptografada)
    #print('senha', senha)
    #print('sal', sal)
    #print('senha criptografada', criptografa_senha(senha, sal))
    return senha_correta_criptografada == criptografa_senha(senha, sal)

def verifica_se_usuario_pode_escrever(usuario, inode):
    #print(inode[4], inode[7])
    return inode[4] == usuario or inode[7][1] == '1'

def verifica_se_usuario_pode_ler(usuario, inode):
    return inode[4] == usuario or inode[7][0] == '1'

def escreveNaMemoria():
    global gerenciamento_blocos, gerenciamento_inodes, TABELA
    arq_pickle = {}
    arq_pickle.update(gerenciamento_inodes)
    arq_pickle.update(gerenciamento_blocos)
    arq_pickle["TABELA"] = TABELA.transformaTabelaemString()
    str_final = pickle.dumps(arq_pickle)
    dic = pickle.loads(str_final)
    with open('sistema.pickle', 'wb') as file:
        pickle.dump(dic, file)


def leArquivopickle():
    global gerenciamento_blocos, gerenciamento_inodes, TABELA
    with open('sistema.pickle', 'rb') as file:
        dados = pickle.load(file)
    TABELA.transformaStringemTabela(dados["TABELA"])
    #print(dados.keys())
    for indice in range(0, 2500):
        gerenciamento_inodes[indice] = dados[int(indice)]
    for indice in range(2500, 62500):
        gerenciamento_blocos[indice] = dados[int(indice)]


def cria_inodes_blocos():
    global gerenciamento_inodes, gerenciamento_blocos
    if not (os.path.isfile('sistema.pickle')):
        for i in range(2500):
            gerenciamento_inodes[i] = []

        for j in range(2500, 62500):
            gerenciamento_blocos[j] = ''


def corta_conteudo(string = str) -> list:
    return [string[i:4000+i:] for i in range(0,len(string),4000)]


def aloca_blocos(lista_blocos = list) -> list:
    global TABELA, gerenciamento_blocos
    enderecos = []
    for conteudo in lista_blocos:
        posicao_livre = TABELA.getPosicaoLivreBloco()
        enderecos.append(posicao_livre)
        TABELA.setOcupado(posicao_livre)
        gerenciamento_blocos[posicao_livre] = conteudo

    return enderecos


def verifica_se_arquivo_existe(nome_arquivo):
    global gerenciamento_inodes
    conteudo_diretorio = gerenciamento_inodes[caminho_memoria_diretorio_atual]
    lista_enderecos = conteudo_diretorio[-1]
    if len(lista_enderecos):
        for endereco in lista_enderecos:
            info_inode_arquivo = gerenciamento_inodes[endereco]
            if info_inode_arquivo[0] == nome_arquivo:
                return endereco
    return None
    

# O inode contêm a seguinte estrutura:
'''
Nome do arquivo/diretório .......................0
Diretorios anteriores ...........................1
Endereço do diretório que está localizado .......2
Criador .........................................3
Dono ............................................4
Data de criação .................................5
Data de modificação .............................6
Permissões de acesso ............................7 (primeiro bit de leitura privada ou publica, e segundo de escrita privada ou publica)
Tamanho do arquivo ..............................8
Apontadores para blocos/inodes ..................9
'''


def add_info_inode(
        endereco_memoria = int,
        nome = str,
        caminho = str,
        data_de_criacao = str,
        data_de_modificacao = str,
        criador=USER,
        permissoes="00",
        dono=USER
    ):
    
    tamanho = 2000 #bytes (tamanho do inode)
    gerenciamento_inodes[endereco_memoria] = [
        nome, 
        caminho,
        endereco_memoria,
        criador, 
        dono, 
        data_de_criacao, 
        data_de_modificacao, 
        permissoes, 
        tamanho,
        []
    ]



def data_hora_atual():
    data_e_hora_atuais = datetime.now()
    data_de_criacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    data_de_modificacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    return data_de_criacao, data_de_modificacao


def inicia_sistema_do_zero():
    global caminho_atual_str, caminho_endereco, caminho_memoria_diretorio_atual, TABELA
    cria_inodes_blocos()

    data_de_criacao, data_de_modificacao = data_hora_atual()
    caminho_atual_str = 'home/' # caminho até o arquivo
    caminho_endereco = 0        # endereco na memoria onde o diretorio atual está
    caminho_memoria_diretorio_atual = 0
    TABELA.setOcupado(0)

    add_info_inode(
        caminho_endereco, 
        'home',
        caminho_atual_str, 
        data_de_criacao, 
        data_de_modificacao,
        'root',
        '00',
        'root'
        )

    #criar_arquivo('shadow.txt', 'root', 'root')
    criar_arquivo('passwd.txt', 'root', 'root')


def add_endereco_no_diretorio(endereco_arquivo_ou_diretorio):
    global gerenciamento_inodes
    conteudo_inode = gerenciamento_inodes[caminho_memoria_diretorio_atual]
    conteudo_inode[-1].append(endereco_arquivo_ou_diretorio)


def desaloca_inode(endereco_inode):
    global gerenciamento_inodes, TABELA
    conteudo_inode_diretorio = gerenciamento_inodes[caminho_memoria_diretorio_atual]
    conteudo_inode = gerenciamento_inodes[endereco_inode]
    if conteudo_inode[0].endswith('.txt'):
        conteudo_inode_diretorio[-1].remove(endereco_inode)
        desaloca_blocos(conteudo_inode[-1])
        TABELA.setLivre(endereco_inode)
        gerenciamento_inodes[endereco_inode] = []
        escreveNaMemoria()
    else:
        if len(conteudo_inode[-1]) > 0:
            print("Erro: só pode remover diretórios vazios.")
        else:
            conteudo_inode_diretorio[-1].remove(endereco_inode)
            TABELA.setLivre(endereco_inode)
            gerenciamento_inodes[endereco_inode] = []
            escreveNaMemoria()


def desaloca_blocos(lista_blocos = list):
    global TABELA
    if len(lista_blocos):
        for bloco in lista_blocos:
            TABELA.setLivre(bloco)


def recebe_endereco_retorna_dados(conteudo):
    global gerenciamento_inodes
    conteudo_inode = gerenciamento_inodes[conteudo]
    return conteudo_inode[0], conteudo_inode[5], conteudo_inode[6], conteudo_inode[8]


def muda_data_modificacao(endereco):
    global gerenciamento_inodes
    conteudo_inode = gerenciamento_inodes[endereco]
    _, data_modificacao = data_hora_atual()
    conteudo_inode[6] = data_modificacao
    gerenciamento_inodes[endereco] = conteudo_inode

def muda_tamanho_arquivo(endereco):
    global gerenciamento_inodes
    conteudo_inode = gerenciamento_inodes[endereco]
    tamanho = len(conteudo_inode[-1])
    conteudo_inode[8] = tamanho*4000 + 2000
    gerenciamento_inodes[endereco] = conteudo_inode

def main():
    global USER, caminho_atual_str, caminho_endereco, caminho_memoria_diretorio_atual
    lista_enderecos_blocos = []
    while True:
        USER = input("Digite o nome do usuário: ")
        senha_original = input("Digite a sua senha: ")
        if not (os.path.isfile('sistema.pickle')):
            inicia_sistema_do_zero()
            criar_usuario('root', senha_original)
            criar_usuario(USER, senha_original)
            escreveNaMemoria()
            break
        else:
            leArquivopickle()
            if not verifica_se_usuario_existe(USER, ler_arquivo_de_usuarios()):
                criar_usuario(USER, senha_original)
            if verifica_se_usuario_existe(USER, ler_arquivo_de_usuarios()) and autentica_usuario(USER, senha_original, ler_arquivo_de_usuarios(), ler_arquivo_de_senhas()):
                print("Login efetuado com sucesso.")
                break
            else:
                print("Senha inválida.")
    
    destino = f"home/{USER}"
    lista_diretorios = destino.split('/')
    for diretorio in lista_diretorios:
        if diretorio != "" and verifica_se_arquivo_existe(diretorio):
            conteudo_inode_diretorio = gerenciamento_inodes[verifica_se_arquivo_existe(diretorio)]
            caminho_atual_str = conteudo_inode_diretorio[1]    # caminho até o arquivo
            caminho_endereco = conteudo_inode_diretorio[2]     # endereco na memoria onde o diretorio atual está
            caminho_memoria_diretorio_atual = conteudo_inode_diretorio[2]

    while True:
        #print(gerenciamento_inodes[0], gerenciamento_inodes[1], gerenciamento_inodes[2], gerenciamento_inodes[3])
        #print(gerenciamento_blocos[2500],gerenciamento_blocos[2501],gerenciamento_blocos[2502],gerenciamento_blocos[2503])
        caminho_atual_diretorio_string = gerenciamento_inodes[caminho_memoria_diretorio_atual]
        #print(caminho_atual_diretorio_string, caminho_memoria_diretorio_atual)
        #destino = f"{USER}"
        #conteudo_inode_diretorio = gerenciamento_inodes[verifica_se_arquivo_existe(destino)]
        #caminho_atual_str = conteudo_inode_diretorio[1]    # caminho até o arquivo
        #caminho_endereco = conteudo_inode_diretorio[2]     # endereco na memoria onde o diretorio atual está
        #caminho_memoria_diretorio_atual = conteudo_inode_diretorio[2]
        #caminho_memoria_diretorio_atual = caminho_endereco
        #caminho_atual_str = caminho_atual_str+f"{nome}/"
        #caminho_atual_diretorio_string = verifica_se_arquivo_existe(diretorio_novo)
        comando = input(f'{caminho_atual_diretorio_string[1]}~:')
        comando_separado = ["pass"]

        if len(comando) > 0:
            comando_separado = comando.split(' ')
            if not comando.startswith('ls') and len(comando_separado) != 1:
                nome = comando_separado[1]
            
        # comandos sobre arquivos
        # Criar arquivo (touch arquivo) 
        if comando_separado[0] == "touch":
            if len(comando_separado) > 1: 
                if not nome.endswith('.txt'):
                    nome += '.txt'
                if verifica_se_arquivo_existe(nome):
                    print("Arquivo já existe")
                else:
                    caminho_endereco = TABELA.getPosicaoLivreInode()
                    TABELA.setOcupado(caminho_endereco)
                    data_de_criacao, data_de_modificacao = data_hora_atual()

                    add_info_inode(
                        caminho_endereco, # endereco na memoria onde o arquivo está
                        nome,
                        caminho_atual_str, 
                        data_de_criacao, 
                        data_de_modificacao,
                        USER,
                        '00',
                        USER
                    )
                    # adiciona endereco do arquivo no inode do diretorio
                    add_endereco_no_diretorio(caminho_endereco)
                    escreveNaMemoria()

            
        # Remover arquivo (rm arquivo)
        elif comando_separado[0] == "rm":
            if verifica_se_arquivo_existe(nome):
                desaloca_inode(verifica_se_arquivo_existe(nome))
            else:
                print('Erro : O arquivo ' + nome + ' não existe')
            

        # Escrever no arquivo (echo "conteudo legal" >> arquivo)
        elif comando_separado[0] == "echo":
            if len(comando_separado) > 1:
                conteudo_arquivo = ''
                copiar = 0
                for caracter in comando:               
                    if caracter == '"' or caracter == "'":
                        copiar += 1
                    if copiar == 1:
                        conteudo_arquivo += caracter
                conteudo_arquivo += '"'

                if comando_separado[-2] == ">>":
                    conteudo_novo = ''
                    conteudo_existente = ''
                    nome = comando_separado[-1]
                    if verifica_se_arquivo_existe(nome):
                        inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
                        if not verifica_se_usuario_pode_escrever(USER, inode_arquivo):
                            print("Permissão negada.")
                            continue
                        lista_enderecos_blocos = inode_arquivo[-1]
                        if len(inode_arquivo[-1]) > 0:
                            conteudo_existente = ''.join(map(str, [
                                gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos
                            ]))
                            conteudo_novo = conteudo_arquivo[1:-1:]
                            conteudo_arquivo = conteudo_existente + "\n" + conteudo_novo
                            
                            desaloca_blocos(lista_enderecos_blocos)
                            lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo))
                        else:
                            lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo[1:-1:]))
                        if len(lista_enderecos) <= 425:
                            muda_data_modificacao(verifica_se_arquivo_existe(nome))
                            inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
                            del inode_arquivo[-1]
                            inode_arquivo.append(lista_enderecos)
                            gerenciamento_inodes[verifica_se_arquivo_existe(nome)] = inode_arquivo
                            muda_tamanho_arquivo(verifica_se_arquivo_existe(nome))
                            escreveNaMemoria()
                        else:
                            desaloca_blocos(lista_enderecos)
                            print("Você excedeu o tamanho máximo permitido de arquivo.")
                    else:
                        print('Erro : O arquivo ' + nome + ' não existe. Crie o arquivo antes de escrever.')
                else:
                    print("Comando inválido")
            else:
                print("Comando inválido")

        # Ler arquivo (cat arquivo)
        elif comando_separado[0] == "cat":
            if verifica_se_arquivo_existe(nome):
                conteudo_inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome)]
                if not verifica_se_usuario_pode_ler(USER, conteudo_inode_arquivo):
                    print("Permissao negada.")
                    continue
                lista_enderecos_blocos = conteudo_inode_arquivo[-1]
                #print(gerenciamento_blocos.keys())
                #exit()
                print(''.join(map(str, [gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos])))
                
            else:
                print('Erro : O arquivo ' + nome + ' não existe')

        # Copiar arquivo (cp arquivo1 arquivo2)
        elif comando_separado[0] == "cp":
            if len(comando_separado) == 3:
                nome_primeiro_arquivo = comando_separado[1]
                nome_segundo_arquivo = comando_separado[2]
                if verifica_se_arquivo_existe(nome_primeiro_arquivo):
                    if not nome_segundo_arquivo.endswith('.txt'):
                        nome_segundo_arquivo += '.txt'
                    if not verifica_se_arquivo_existe(nome_segundo_arquivo):
                        conteudo_inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome_primeiro_arquivo)]
                        lista_enderecos_blocos = conteudo_inode_arquivo[-1]
                        criador = conteudo_inode_arquivo[3]
                        dono = conteudo_inode_arquivo[4]
                        permissoes = conteudo_inode_arquivo[7]
                        conteudo_arquivo_um = ''.join(map(str, [gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos]))
                        caminho_endereco = TABELA.getPosicaoLivreInode()
                        TABELA.setOcupado(caminho_endereco)
                        data_de_criacao, data_de_modificacao = data_hora_atual()

                        add_info_inode(
                            caminho_endereco, # endereco na memoria onde o arquivo está
                            nome_segundo_arquivo,
                            caminho_atual_str, 
                            data_de_criacao, 
                            data_de_modificacao,
                            criador,
                            permissoes,
                            dono
                        )
                        # adiciona endereco do arquivo no inode do diretorio
                        add_endereco_no_diretorio(caminho_endereco)
                        lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo_um))
                        inode_arquivo = gerenciamento_inodes[caminho_endereco]
                        del inode_arquivo[-1]
                        inode_arquivo.append(lista_enderecos)
                        muda_tamanho_arquivo(verifica_se_arquivo_existe(nome_segundo_arquivo))
                        escreveNaMemoria()

                    else:
                        conteudo_inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome_primeiro_arquivo)]
                        lista_enderecos_blocos = conteudo_inode_arquivo[-1]
                        conteudo_arquivo_um = ''.join(map(str, [gerenciamento_blocos[endereco] for endereco in lista_enderecos_blocos]))
                        lista_enderecos = aloca_blocos(corta_conteudo(conteudo_arquivo_um))
                        inode_arquivo = gerenciamento_inodes[verifica_se_arquivo_existe(nome_segundo_arquivo)]
                        muda_data_modificacao(verifica_se_arquivo_existe(nome_segundo_arquivo))
                        del inode_arquivo[-1]
                        inode_arquivo.append(lista_enderecos)
                        muda_tamanho_arquivo(verifica_se_arquivo_existe(nome_segundo_arquivo))
                        escreveNaMemoria()
                else:
                    print('Erro : O arquivo ' + nome_primeiro_arquivo + ' não existe')  
            else:
                print("Comando inválido")
            
        # Renomear arquivo (mv arquivo1 arquivo2)
        elif comando_separado[0] == "mv":
            if len(comando_separado) == 3:
                novo_nome = comando_separado[2]
                if verifica_se_arquivo_existe(nome):
                    if nome.endswith('.txt'):              # muda nome de arquivo
                        if not novo_nome.endswith('.txt'):
                            novo_nome += '.txt'
                        if not verifica_se_arquivo_existe(novo_nome):
                            endereco = verifica_se_arquivo_existe(nome)
                            conteudo_inode_arquivo = gerenciamento_inodes[endereco]
                            if not verifica_se_usuario_pode_escrever(USER, conteudo_inode_arquivo):
                                print("Permissao negada.")
                                continue
                            conteudo_inode_arquivo[0] = novo_nome
                            gerenciamento_inodes[endereco] = conteudo_inode_arquivo
                            muda_data_modificacao(endereco)
                            escreveNaMemoria()
                        else:
                            print('Erro: O nome ' + novo_nome + ' já está em uso')
                    else:                                  # muda nome de diretorio
                        if not verifica_se_arquivo_existe(novo_nome):
                            endereco = verifica_se_arquivo_existe(nome)
                            conteudo_inode = gerenciamento_inodes[endereco]
                            conteudo_inode[0] = novo_nome
                            gerenciamento_inodes[endereco] = conteudo_inode
                            muda_data_modificacao(endereco)
                            escreveNaMemoria()
                        else:
                            print('Erro: O nome ' + novo_nome + ' já está em uso')
                else:
                    print('Erro : O arquivo/diretorio ' + nome + ' não existe')    
            else:
                print("Comando inválido")

        # comandos sobre diretorios
        # Criar diretório (mkdir diretorio)
        elif comando.startswith("mkdir"):
            if len(comando_separado) > 1:
                diretorio_novo = comando_separado[1]
                if nome.endswith('.txt'):
                    print("Erro: nome do diretorio não pode conter extensão .txt")
                else:
                    if verifica_se_arquivo_existe(diretorio_novo):
                        print("Erro: diretório já existe")
                    else:
                        caminho_endereco = TABELA.getPosicaoLivreInode()
                        TABELA.setOcupado(caminho_endereco)
                        data_de_criacao, data_de_modificacao = data_hora_atual()

                        add_info_inode(
                            caminho_endereco, # endereco na memoria onde o arquivo está
                            diretorio_novo,
                            caminho_atual_str+f"{nome}/",
                            data_de_criacao, 
                            data_de_modificacao
                        )
                        # adiciona endereco do arquivo no inode do diretorio
                        add_endereco_no_diretorio(caminho_endereco)
                        caminho_memoria_diretorio_atual = caminho_endereco
                        caminho_atual_str = caminho_atual_str+f"{nome}/"
                        caminho_atual_diretorio_string = verifica_se_arquivo_existe(diretorio_novo)
                        escreveNaMemoria()
            else:
                print("Comando inválido")
        
        # Remover diretório (rmdir diretorio) - só funciona se diretório estiver vazio
        elif comando.startswith("rmdir"):
            if verifica_se_arquivo_existe(nome):
                desaloca_inode(verifica_se_arquivo_existe(nome))
            else:
                print('Erro : O arquivo ' + nome + ' não existe')


        # Listar o conteúdo de um diretório (ls diretório)
        elif comando.startswith("ls"):
            conteudo_inode_diretorio = gerenciamento_inodes[caminho_memoria_diretorio_atual]
            conteudo_diretorio = conteudo_inode_diretorio[-1]
            for conteudo in conteudo_diretorio:
                nome, data_de_criacao, data_de_modificacao, tamanho = recebe_endereco_retorna_dados(conteudo)
                if nome.endswith('.txt'):
                    print(f'\narq   {nome}    criado em: {data_de_criacao}    modificado em: {data_de_modificacao}   tamanho: {tamanho} bytes')
                else:
                    print(f'\ndir   {nome}    criado em: {data_de_criacao}    modificado em: {data_de_modificacao}   tamanho: {tamanho} bytes')


        # Trocar de diretório (cd diretorio) *Não esquecer dos arquivos especiais . e ..
        elif comando.startswith("cd"): 
            if len(comando_separado) == 1:
                print("Digite o nome do diretorio")
            else:
                destino = comando_separado[1]
                if destino == '.':
                    caminho_atual_str = 'home/' # caminho até o arquivo
                    caminho_endereco = 0        # endereco na memoria onde o diretorio atual está
                    caminho_memoria_diretorio_atual = 0
                elif destino == '..':
                    if caminho_atual_str == 'home/':
                        pass
                    else:
                        lista_diretorios = caminho_atual_str[:-1:].split('/')
                        atual = lista_diretorios[-1]
                        lista_diretorios.remove(atual)
                        lista_diretorios.remove('home')
                        caminho_atual_str = 'home/' # caminho até o arquivo
                        caminho_endereco = 0        # endereco na memoria onde o diretorio atual está
                        caminho_memoria_diretorio_atual = 0
                        for diretorio in lista_diretorios:
                            #print(diretorio, gerenciamento_inodes[verifica_se_arquivo_existe(diretorio)])
                            if diretorio != "" and verifica_se_arquivo_existe(diretorio):
                                conteudo_inode_diretorio = gerenciamento_inodes[verifica_se_arquivo_existe(diretorio)]
                                caminho_atual_str = conteudo_inode_diretorio[1]    # caminho até o arquivo
                                caminho_endereco = conteudo_inode_diretorio[2]     # endereco na memoria onde o diretorio atual está
                                caminho_memoria_diretorio_atual = conteudo_inode_diretorio[2]
                else:
                    numero = destino.count('/')
                    if numero == 0 and verifica_se_arquivo_existe(destino):
                        conteudo_inode_diretorio = gerenciamento_inodes[verifica_se_arquivo_existe(destino)]
                        caminho_atual_str = conteudo_inode_diretorio[1]    # caminho até o arquivo
                        caminho_endereco = conteudo_inode_diretorio[2]     # endereco na memoria onde o diretorio atual está
                        caminho_memoria_diretorio_atual = conteudo_inode_diretorio[2]
                    else:
                        lista_diretorios = destino.split('/')
                        for diretorio in lista_diretorios:
                            if diretorio != "" and verifica_se_arquivo_existe(diretorio):
                                conteudo_inode_diretorio = gerenciamento_inodes[verifica_se_arquivo_existe(diretorio)]
                                caminho_atual_str = conteudo_inode_diretorio[1]    # caminho até o arquivo
                                caminho_endereco = conteudo_inode_diretorio[2]     # endereco na memoria onde o diretorio atual está
                                caminho_memoria_diretorio_atual = conteudo_inode_diretorio[2]
                            else:
                                print(f'Erro: diretorio {diretorio} não existe.')
        elif comando_separado[0] == "exit":
            escreveNaMemoria()
            break
        else:
            pass

main()