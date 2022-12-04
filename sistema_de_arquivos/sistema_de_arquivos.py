#O seu disco rígido possui uma capacidade de 256MB => 64000 inodes
#Os blocos para armazenamento de dados possuem 4KB. 

class Inode:
    def __init__(self,nome) -> None:
        self.nome = nome #Nome do arquivo/diretório
        self.diretorio = None #no caso de diretórios talvez tenha que apontar para o diretório anterior 

        self.criador = None
        self.dono = None
        self.tamanho = None
        self.data_de_criacao = None
        self.data_de_modificacao = None
        self.permissoes_de_acesso = None #Permissões de acesso (dono e outros usuários - leitura, escrita, execução)
        self.lista_dos_blocos_que_ocupa = [] #colocar aqui os blocos de memória que o arquivo vai ocupar 
        self.apontador_para_outro_inode = [] #em formato de lista pq um arquivo pode precisar de n inodes   

class Diretorios: #lista de arquivos e de inodes 
    def __init__(self,nome):
        self.nome_atual = nome
        self.diretorio_anterior = None
        self.proximos_diretorios = []
        self.inodes_do_diretorio_atual = []
        self.arquivos_do_diretorio = [] #guardar todos os nomes de arquivos desse diretório
        
    def criaDiretorio(self, nome):
        self.proximos_diretorios.append(Diretorios(nome))
        self.inodes_do_diretorio_atual.append(Inode(nome))
  
class SistemadeArquivos:
    def __init__(self, tamanho_do_bloco: int, nome_raiz: str):
        self.tamanho_do_bloco = tamanho_do_bloco
        self.diretorio_raiz = Diretorios(nome_raiz)
        self.diretorio_raiz.inodes_do_diretorio_atual.append(Inode(nome_raiz))

def main():
    
    raiz = SistemadeArquivos(256, '/')
    atual = raiz.diretorio_raiz #diretório atual
    nome_do_diretorio_atual = ''
    while True:
        #print(str(diretorio_raiz.nome_atual)+'> ', end='')
        nome_do_diretorio_atual += atual.nome_atual
        comando = input(str(atual.nome_atual))
        comando_separado = comando.split(' ')
        
        # comandos sobre arquivos
        
        # Criar arquivo (touch arquivo)
        
        if comando.startswith("touch"):
            
            novo_inode = Inode(comando_separado[1])
            novo_inode.nome = comando_separado[1]
            novo_inode.diretorio = atual.nome_atual
            atual.inodes_do_diretorio_atual.append(novo_inode)
            
        # Remover arquivo (rm arquivo)
        elif comando.startswith("rm"):#eu
            for i in atual.inodes_do_diretorio_atual:
                if i.nome == comando_separado[1]:
                    atual.inodes_do_diretorio_atual.remove(i)            
            
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