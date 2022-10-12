
# tabela de processos -> PRONTOS E BLOQUEADOS


# lê arquivo
# chama o escalonador
# quando o processo estiver executando, sorteia pra saber se vai fazer entrada e saída
# SE entrada e saída == TRUE:
#     Sorteia dispositivo
#     Sorteia momento que vai realizar
#     "Executa"
#     fazer_entrada_e_saida()
# SENÃO:
#     "Executa"



# cada dispositivo vai ter uma thread (acho que foi isso que o professor sugeriu)

# as threads podem ser criadas antes de chamar o escalonador e poder ser guardadas numa lista
# quando sortear o dispositivo, apenas pegamos a thread que tiver o índice correspondendo ao 
# número do dispositivo e chamamos a função de fazer entrada e saída (só uma ideia)


"""
fazer_entrada_e_saida():
    while True:
        chegou algo na fila
        executa E/S
        processo => PRONTO
"""
