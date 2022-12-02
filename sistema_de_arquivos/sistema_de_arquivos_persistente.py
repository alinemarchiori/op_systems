#O seu disco rígido possui uma capacidade de 256MB 
#Os blocos para armazenamento de dados possuem 4KB. 

from datetime import datetime

user = ''

# no dicionario abaixo são guardados os inodes,
# cada inode gasta 2 KB de memória, e o sistema
# reserva espaço para 10000 inodes
gerenciamento_inodes = {}
gerenciamento_blocos = {} 
tabela_inodes_e_blocos_livres_ocupados = []


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

'''
Nome do arquivo/diretório ..............-> 128 caracteres -> 128 bytes
Diretório ou arquivo ...................-> 2 caracteres   -> 2 bytes
Criador  ...............................-> 44 caracteres  -> 44 bytes
Dono  ..................................-> 40 caracteres  -> 40 bytes
Tamanho ................................-> numero inteiro -> 4 bytes
Data de criação ........................-> 16 caracteres  -> 16 bytes
Data de modificação ....................-> 16 caracteres  -> 16 bytes
Permissões de acesso ...................-> 50 caracteres  -> 50 bytes
TOTAL DO INODE por enquanto...............................-> 300 bytes

Sobraram 1700 bytes 
Se usar 3 caracteres para endereçar 566 endereços de blocos ou outros inodes
Equivalendo a um arquivo de 2264 Kb ou 2264000 bytes 
                        OU 
Equivalendo a um diretório que aponta para 566 inodes(diretorios/arquivos)

# Se for DIRETÓRIO
Apontadores para blocos ................-> 0 KB
Apontador para eventual outro i-node ...-> 2264 Kb

# Se for arquivo
Apontadores para blocos ................-> definir conforme o uso
Apontador para eventual outro i-node ...-> definir conforme o uso

TOTAL DO INODE ...........................................-> 2000 bytes
'''

def calcula_tamanho(string = str) -> int:
    pass

def inode(
        nome = str,
        caminho = str,
        data_de_criacao = None,
        data_de_modificacao = None,
        ):
    if gerenciamento_inodes[nome]:
        if nome.endswith('.txt'):
            print('Erro : O arquivo ' + nome + ' já existe')
        else:
            print('Erro : O Diretório ' + nome + ' já existe')
    else:
        if nome.endswith('.txt'):
            gerenciamento_inodes[nome] = [caminho, user, None, data_de_criacao, data_de_modificacao, None, tamanho, []]
        else:
            gerenciamento_inodes[nome] = [caminho, user, None, data_de_criacao, data_de_modificacao, None, tamanho, []]            


def main():
    global user
    user = input("Digite o nome do usuário: ")
    caminho = 'raiz/'

    while True:
        
        comando = input()
        comando_separado = comando.split(' ')
        nome = comando_separado[1]
        
        
        # comandos sobre arquivos
        # Criar arquivo (touch arquivo) 
        if comando_separado[0] == "touch":
            data_e_hora_atuais = datetime.now()
            data_de_criacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
            data_de_modificacao = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
            if not nome.endswith('.txt'):
                nome += '.txt'
            inode(nome, caminho, None, data_de_criacao, data_de_modificacao, None)
            
        # Remover arquivo (rm arquivo)
        elif comando_separado[0] == "rm":
            if gerenciamento_inodes[nome]:
                gerenciamento_inodes.pop(nome)
            
            else:
                print('Erro : O arquivo ' + nome + ' não existe')
                        
        # Escrever no arquivo (echo "conteudo legal" >> arquivo)
        elif comando.startswith("echo"):
            #verifica_se_o_arquivo_existe_no_diretorio(comando_separado[-1], atual)
            pass

        # Ler arquivo (cat arquivo)
        elif comando_separado[0] == "cat":
            if gerenciamento_inodes[nome]:
                print(gerenciamento_inodes[nome][-1])
            else:
                print('Erro : O arquivo ' + nome + ' não existe')

        # Copiar arquivo (cp arquivo1 arquivo2)
        elif comando_separado[0] == "cp":
            if gerenciamento_inodes[nome]:
                nome_atual = comando_separado[2]
                conteudo_anterior = gerenciamento_inodes.pop(nome)
                gerenciamento_inodes[nome_atual] = conteudo_anterior
                gerenciamento_inodes[nome] = conteudo_anterior

            
        # Renomear arquivo (mv arquivo1 arquivo2)
        elif comando_separado[0] == "mv":
            if gerenciamento_inodes[nome]:
                if not gerenciamento_inodes[comando_separado[2]]:
                    nome_atual = comando_separado[2]
                    conteudo_anterior = gerenciamento_inodes.pop(nome)
                    gerenciamento_inodes[nome_atual] = conteudo_anterior
                else:
                     print('Erro: O nome ' + comando_separado[2] + ' já está em uso')
                
        
        # comandos sobre diretorios
        # Criar diretório (mkdir diretorio)
        elif comando.startswith("mkdir"):#eu
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
        elif comando.startswith("rmdir"):
            diretorio_novo = comando_separado(1)
        # Listar o conteúdo de um diretório (ls diretório)
        elif comando.startswith("ls"):
            pass
        # Trocar de diretório (cd diretorio) *Não esquecer dos arquivos especiais . e ..
        elif comando.startswith("cd"):
            #TODO em algum momento atualizar a variavel atual
            atual = '' #nome do diretorio buscado
        # Renomear diretorio (mv diretorio1 diretorio2) 
        elif comando.startswith("mv"):
            pass


main()