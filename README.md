#Gerenciador de Processos: Escalonador

[![NPM](https://img.shields.io/npm/l/react)](https://github.com/alinemarchiori/op_systems/blob/master/LICENSE)

#Sobre o projeto

O gerenciador de processos, a partir de um algoritmo escalonador, é uma aplicação desenvolvida para a disciplina de Sistemas operacionais. 

O gerenciador recebe um arquivo com diversos processos, podendo receber mais em tempo de execução, o tipo de algoritmo de escalonamento e de fração de CPU que os processos receberão. A aplicação retorna o tempo necessário que cada processo precisou para ser executado em determinado algortimo.

#Desenvolvimento

A aplicação foi desenvolvida totamente em Python


#Como executar o projeto

Pré-requisistos: Python3


```bash

#Executar o comando:

python escalonador.py

#Escolher somente o número para definir o tipo de algoritmo:

1 por Alternancia Circular
2 por Prioridade
3 por Loteria

#Se necessário, incluir um processo seguindo o padrão:

NomedoProcesso|IdentificadordoProc|TempoDeExecução|Prioridades(ou bilhetes)|IdentificadordoUsua|QuantdeMemoria

#Digite sair, a qualquer momento, para parar a aplicação.

sair

```

#Observações

O algoritmo por prioridade segue o padrão de prioridades crescente, ou seja, quanto menor o número da prioridade maior é a sua prioridade, e consequentemente, será executado primeiro.

#Autores

Aline Marchiori, Beatriz Leal, Breno Soares
