import threading
import logging
import random
import time


contas = [] #lista de contas bancárias existentes
lista_de_locks = []
lista_de_semaforos = []
def cria_lock():
    lista_de_locks.append(threading.Lock())

def cria_semaphore

S = threading.Semaphore(5)
lock = threading.Lock()
format = "%(asctime)s: %(message)s"
logging.basicConfig(
    format=format, 
    level=logging.INFO, 
    datefmt="%H:%M:%S"
)

#classe conta, que guarda todas as características de uma conta
class Conta:
    def __init__(self, id):
        self.id = id
        self.status = True #variavel que guarda um boleano para saber se a conta está em uso para debito ou credito
        self.saldo = 0.0

    def debito(self, valor): # função solicitada
        self.saldo -= valor

    def credito(self, valor): # função solicitada
        self.saldo += valor
    
    def consulta(self): # função solicitada
        return self.saldo

    def altera_status(self): #funcão que altera o status da conta, usada quando vai fazer as operaçõesde debito ou credito
        if self.status:
            self.status = False
        else:
            self.status = True


# função que cria contas para que nelas sejam realizadas as operações
# o número de contas criadas é definido pelo unuário e depois de criadas
# são armazenadas na lista para serem acessadas aleatóriamente pelas threads
def cria_contas(quantidade_de_contas):
    global contas

    for id in range(quantidade_de_contas):
        
        conta = Conta(id)
        contas.append(conta)

# função que sorteia qual operação a thread vai realizar na conta
def sorteia_operacoes():
    return random.choice(['consulta', 'credito', 'debito'])

# função que sorteia o valor que será creditado ou debitado da conta
def sorteia_valores():
    return random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# função que sorteia a conta que a thread vai realizar as operações
def sorteia_conta():
    return random.choice(contas)

# função que realiza as operações, recebe a conta em questão e a operação que será realizada
def banking_operations(conta, operacao):
    
    # se a operação for credito é usado um mutex para bloquear o acesso e desbloquear só depois que a operação finalizar
    if (
        operacao == "credito" and 
        conta.status
    ):
        lock.acquire()
        logging.info(f"Lock ativado {id}")

        conta.altera_status()
        time.sleep(1)
        conta.credito(sorteia_valores())
        time.sleep(1)
        conta.altera_status()

        lock.release()
        logging.info(f"Lock liberado {id}")

    # se a operação for debito é usado um mutex para bloquear o acesso e desbloquear só depois que a operação finalizar
    if (
        operacao == "debito" and 
        conta.status
    ): 
        lock.acquire()
        logging.info(f"Lock ativado {id}")

        conta.altera_status()
        time.sleep(1)
        conta.debito(sorteia_valores())
        time.sleep(1)
        conta.altera_status()

        lock.release()
        logging.info(f"Lock liberado {id}")

    # se for consulta é usado um semaforo para limitar o acesso a cinco threads ao mesmo tempo
    if (
        operacao == "consulta" and 
        conta.status
    ):
        S.acquire() # quando entra na região crítica
        logging.info(f"Thread {id} entrou no semáforo")

        time.sleep(1)
        valor = conta.consulta()
        print(valor, id)

        logging.info(f"Thread {id} consultou saldo")
        S.release() # quando sai da região crítica
        logging.info("Menos um na região crítica")

# basicamente a função que chama a função de operações
# o loop serve para que cada thread tenha a chance de operar em mais de uma conta
# durante a eexecução do programa
def banking(id):
    for _ in range(3):
        banking_operations(sorteia_conta(), sorteia_operacoes())


#condição inicial, peguei do exemplo que foi dado 
if __name__ == "__main__":

    threads = [] #armazena os descritores das threads
    cria_contas(quantidade_de_contas=5)

    logging.info("Main    : before creating thread")
    for id in range(1,10):
        t = threading.Thread(target=banking, args=(id,)) #inicializa a thread, informa o nome da função e os parâmetros
        logging.info("Main    : before running thread")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
