#O seu disco rígido possui uma capacidade de 256MB => 64000 inodes
#Os blocos para armazenamento de dados possuem 4KB. 

class Inode:
    def __init__(self) -> None:
        self.nome_arquivo = None #Nome do arquivo/diretório
        self.diretorio = None
        self.diretorio_ou_arquivo = None #diretorio = False, arquivo = True
        self.criador = None
        self.dono = None
        self.tamanho = None
        self.data_de_criacao = None
        self.data_de_modificacao = None
        self.permissoes_de_acesso = None #Permissões de acesso (dono e outros usuários - leitura, escrita, execução)
        self.apontadores_para_blocos = None
        self.apontador_para_outro_inode = None

class Diretorios:
    def __init__(self) -> None:
        self.nome_atual = None
        self.diretorio_anterior = None
        self.proximo_diretorio = None

    def criaDiretorio(self, nome, anterior):
        self.nome = nome
        self.diretorio_anterior = anterior
  
class SistemadeArquivos:
    def __init__(self, tamanho_do_bloco) -> None:
        pass

    def criaPasta(self):
        pass

    def excluiPasta(self):
        pass


def main():

    diretorio_atual = Diretorios()
    diretorio_atual.criaDiretorio("/", None)
    inode_raiz = Inode()
    inode_raiz.nome_arquivo = diretorio_atual.nome
    inodes = []
    inodes.append(inode_raiz)

    while True:
        comando = input()#TODO: fazer ele printar o diretorio atual
        comando_separado = comando.split(' ')
        # comandos sobre arquivos
        # Criar arquivo (touch arquivo)
        if comando.startswith("touch"):
            nome_arquivo = comando_separado[1]
            inode = Inode()
            inode.nome_arquivo = nome_arquivo
            inode.diretorio = diretorio_atual
            inodes.append(inode)

        # Remover arquivo (rm arquivo)
        elif comando.startswith("rm"):
            nome_arquivo = comando_separado[1]
            for inode in inodes:
                pass
            
        # Escrever no arquivo (echo "conteudo legal" >> arquivo)
        elif comando.startswith("echo"):
            pass
        # Ler arquivo (cat arquivo)
        elif comando.startswith("cat"):
            pass
        # Copiar arquivo (cp arquivo1 arquivo2)
        elif comando.startswith("cp"):
            pass
        # Renomear arquivo (mv arquivo1 arquivo2)
        elif comando.startswith("mv"):
            pass
        
        # comandos sobre diretorios
        # Criar diretório (mkdir diretorio)
        elif comando.startswith("mkdir"):
            pass
        # Remover diretório (rmdir diretorio) - só funciona se diretório estiver vazio
        elif comando.startswith("rmdir"):
            pass
        # Listar o conteúdo de um diretório (ls diretório)
        elif comando.startswith("ls"):
            pass
        # Trocar de diretório (cd diretorio) *Não esquecer dos arquivos especiais . e ..
        elif comando.startswith("cd"):
            pass
        # Renomear diretorio (mv diretorio1 diretorio2) 
        elif comando.startswith("mv"):
            pass


main()