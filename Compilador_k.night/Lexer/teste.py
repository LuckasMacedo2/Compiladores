#!/usr/bin/env python
# coding: utf-8

# -------------------------------------------------------------------------------------------------------------------------------
# Aluno: Lucas Macedo da Silva e Milena Bueno
# Professor: Fernando Abadia
# Compiladores - Turma A02
# Analisador de código
# lexer.py, main.py e validacoes.py
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
#
# A tabela token | lexema contém os seguintes campos
#
# if) Apenas a palavra if
#
#
# operador) Os seguintes caracteres: ( ) ; =
#
# operador_artmetico) Os operadores aritmeticos em si: + - * /
#
# numero) Os números em si: 1, 2, 0.123, ....
#
# caracter) Os caracteres especiais da tabela ascci que não se encaixam em nenhuma categoria citada anteriormente, como: !, @...
#
# reservada) Destinada a todas as palavras chaves da linaguagem nesta versão foi considerada a linguagem C++.
#
# comentario) Os comentarios foram ignorados.
#
# identificador) Valores que não se encaixam nas categorias acima e fazem sentido.
# 
# -> Todos os erros foram tratados, de forma que ao encontrar um erro, como caracteres invalidos, troca-se o caracter
# pelo valor da variavel global troca_car_erro, se for um numero o valor da mesma e adicionado no comeco de forma a forcar
# que o mesmo seja tratado como um identificador
#
# ---------------------------------------
# Versoes futuras:
# Retirar o then                            - OK
# Adicionar a exponenciacao ^, %	    - OK

# Adicionar strings                         - OK     
# Adicionar a Linguagem criada "K.night"    - OK

# Adicionar os demais caracteres irreconhecidos pela linguagem



# -------------------------------------------------- TESTES ---------------------------------------------------------------------

import os
import lexer as lx

# -------------------------------------------------------------------------------------------------------------------------------
def autor():
    """Retorna o Autor do Código"""

    print('-----------------------------------------------------------------------------------------------')
    print('|Autor: Lucas Macedo da Silva                                                                 |')
    print('|Versão: 5.1                                                                                  |')
    print('|Código para analisar um trecho de código e retornar a tabela token | lexema do mesmo         |')
    print('|Gerar um arquivo contendo os lexemas no seguinte formato: \'[lexema,]\' e um arquivo de erros. |')
    print('-----------------------------------------------------------------------------------------------')
# -------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------
def deleta_pasta(pasta):
    """
    Deleta a pasta criada que contem os arquivos
    """
    
    if os.name == 'nt':
        #os.system('rd /s /q ' + pasta)
        os.system('del /s /q ' + pasta)
    else:
        os.system('rm ' + pasta)

# -------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------
def testa_lexer(arquivo_entrada, arquivo_saida, arquivo_erro):

    lexer = lx.Lexer(arquivo_entrada)

    pasta = '.\\arquivos_analise_lexica\\'

    print(
        '-------------------------------------------------------------------------------------------------------------------------------')
    print('\nTeste')
    print('Arquivo: ', arquivo_entrada)
    print('\n')
    print(open(arquivo_entrada, encoding='latin-1').read())
    tabela = lexer.scanner()
    
    print('\n')
    print('Arquivo de saida')
    saida = open(pasta + arquivo_saida, encoding='latin-1')
    print(saida.read())
    print('\n')

    print('\n')
    print('Arquivo de erros')
    erros = open(pasta + arquivo_erro, encoding='latin-1')
    print(erros.read())
    print('\n')
    
    print('\n')
    print('Tabela')
    print(tabela)
    print('\n')
    
    saida.close()
    erros.close()
    
    print(
        '-------------------------------------------------------------------------------------------------------------------------------')
    print('\n')
    


    print ('Deletar Pasta?\n[1] Sim \n[Qualquer outra coisa] Nao\nOpcao: ', end = '')
    opc = input()
    if opc == '1':
        deleta_pasta(pasta)
    
    

def main():
    testa_lexer('teste.txt', 'arq_saida.txt', 'arq_erro.txt')
    exit()
    
main()


# ----------------------------------------------------- FIM TESTES ------------------------------------------------------------------
