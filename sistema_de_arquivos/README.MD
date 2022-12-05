#Sistema de Arquivos Persistente

[![NPM](https://img.shields.io/npm/l/react)](https://github.com/alinemarchiori/op_systems/blob/master/LICENSE)

#Sobre o projeto

O sistema de arquivos é uma aplicação desenvolvida para a disciplina de Sistemas operacionais. 

O sistema é baseado em i-nodes e tem o objetivo de replicar, superficialmente, a forma que um sistema operacional trabalha com seus arquivos e diretórios.Para isso, o projeto informa a capacidade de memória total do sistema, a capacidade para cada i-node e quais são os dados que os mesmos devem possuir. A persistência é desenvolvida a partir de uma biblioteca Json que é salva a partir do nome do usuário.

#Desenvolvimento

A aplicação foi desenvolvida totalmente em Python


#Como executar o projeto

Pré-requisistos: Python3


```bash

#Executar o comando:

python sistema_de_arquivos_persistente.py

#Digitar o nome do usuário(User é apenas um exemplo, pode ser qualquer nome):

User

#Comandos(Arquivos):

(Criar Arquivo) touch Arquivo.txt
É incluído a extensão .txt caso o nome do arquivo não tenha.

(Remover Arquivo) rm Arquivo.txt
Pela extensão ser adicionada ao criar, os comando de arquivos são funcionarão se o arquivo tiver com a extensão.

(Escrever no Arquivo) echo “texto a ser escrito” >> Arquivo.txt

(Ler Arquivo) cat Arquivo.txt

(Copiar arquivo) cp Arquivo.txt Arquivo1.txt
Se não existir o segundo arquivo, ele cria.

(Renomear arquivo) mv Arquivo.txt Arquivo1.txt

#Comandos(Diretórios)

(Criar Diretório) mkdir diretório

(Remover Diretório) rmdir diretório
Você deve estar no diretório onde está localizado o diretório que deseja remover. 

(Listar conteúdo do Diretório) ls

(Trocar de Diretório) cd diretório 
Para entrar em um diretório
cd .. 
Para voltar ao diretório pai
cd .
Para voltar a raiz

(Renomear Diretório) mv diretório diretório1


#Digite sair, a qualquer momento, para parar a aplicação.

Sair

```


#Autores

Aline Marchiori, Beatriz Leal, Breno Soares, Cris Lima 


