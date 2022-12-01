#O seu disco rígido possui uma capacidade de 256MB 
#Os blocos para armazenamento de dados possuem 4KB. 

user = ''

sistema_de_arquivos = {}

def tamanho():
    pass

def inode(
        nome = str,
        caminho = str,
        #dono = None,
        data_de_criacao = None,
        data_de_modificacao = None,
        #permissoes_de_acesso = None,
        ):
    if sistema_de_arquivos[nome]:
        if nome.endswith('.txt'):
            print('Erro : O arquivo ' + nome + ' já existe')
        else:
            print('Erro : O Diretório ' + nome + ' já existe')
    else:
        if nome.endswith('.txt'):
            sistema_de_arquivos[nome] = [caminho, user, None, data_de_criacao, data_de_modificacao, None, tamanho, []]
        else:
            sistema_de_arquivos[nome] = [caminho, user, None, data_de_criacao, data_de_modificacao, None, tamanho, []]            


def main():
    global user
    user = input("Digite o nome do usuário: ")
    caminho = 'raiz/'

    while True:
        #print(str(diretorio_raiz.nome_atual)+'> ', end='')
        
        comando = input(str(atual.nome_atual))
        comando_separado = comando.split(' ')
        nome = comando_separado[1]
        
        
        # comandos sobre arquivos
        # Criar arquivo (touch arquivo) 
        if comando_separado[0] == "touch":
            data_de_criacao = ''
            data_de_modificacao = ''
            if not nome.endswith('.txt'):
                nome += '.txt'
            inode(nome, caminho, None, data_de_criacao, data_de_modificacao, None)
            
        # Remover arquivo (rm arquivo)
        elif comando_separado[0] == "rm":
            if sistema_de_arquivos[nome]:
                sistema_de_arquivos.pop(nome)
            
            else:
                print('Erro : O arquivo ' + nome + ' não existe')
                        
        # Escrever no arquivo (echo "conteudo legal" >> arquivo)
        elif comando.startswith("echo"):
            verifica_se_o_arquivo_existe_no_diretorio(comando_separado[-1], atual)


        # Ler arquivo (cat arquivo)
        elif comando_separado[0] == "cat":
            if sistema_de_arquivos[nome]:
                print(sistema_de_arquivos[nome][-1])
            else:
                print('Erro : O arquivo ' + nome + ' não existe')

        # Copiar arquivo (cp arquivo1 arquivo2)
        elif comando_separado[0] == "cp":
            if sistema_de_arquivos[nome]:
                nome_atual = comando_separado[2]
                conteudo_anterior = sistema_de_arquivos.pop(nome)
                sistema_de_arquivos[nome_atual] = conteudo_anterior
                sistema_de_arquivos[nome] = conteudo_anterior

            
        # Renomear arquivo (mv arquivo1 arquivo2)
        elif comando_separado[0] == "mv":
            if sistema_de_arquivos[nome]:
                if not sistema_de_arquivos[comando_separado[2]]:
                    nome_atual = comando_separado[2]
                    conteudo_anterior = sistema_de_arquivos.pop(nome)
                    sistema_de_arquivos[nome_atual] = conteudo_anterior
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