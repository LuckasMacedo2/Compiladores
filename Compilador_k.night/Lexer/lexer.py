#!/usr/bin/env python
# coding: utf-8

import validacoes as val # Arquivos com validacoes de caracteres e manipulacao dos mesmos

import os.path # Verifica se a pasta existe

class Lexer:
    
    # -------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, arquivo_entrada, arquivo_erros = 'arq_erro.txt', arquivo_saida = 'arq_saida.txt',
                 arquivo_limpo = 'arq_limpo.txt', arquivo_id = 'arq_id.txt', tabela_hash = '.\\Tabela_hash.txt'):
        pasta = os.path.abspath(os.path.dirname(__file__)) + '\\arquivos_lexer\\'
        if (not os.path.exists(pasta)):            
            os.system('mkdir ' + pasta)
        self.arquivo_id = pasta + arquivo_id
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_erros = pasta + arquivo_erros
        self.arquivo_saida = pasta + arquivo_saida
        self.arquivo_limpo = pasta + arquivo_limpo
        self.idx_id = 0
        self.tabela_hash = tabela_hash
    # -------------------------------------------------------------------------------------------------------------------------------

        
    # -------------------------------------------------------------------------------------------------------------------------------
    def lista_palavra_chaves(self):
        """Retorna uma lista contendo as palavras chaves da linguagem"""

        return "read print if else loop end".split()
    # -------------------------------------------------------------------------------------------------------------------------------


    # -------------------------------------------------------------------------------------------------------------------------------
    def categoria_palavra(self, palavra):
        """Retorna a Qual Categoria a palavra pertenci
            Categorias:
            -> numero
            -> comparador
            -> operador_aritmetico
            -> operador
            -> identificador
            -> caracter
			-> string
            Recebi como parametro uma string.

            Retorno categoria que que a string pertenci


            Por exemplo:
            >>>categoria_palavra ('abacaxi')
            >>>'identificador'

            >>>categoria_palavra('==')
            >>>'comparador'"""

        # --- Caracter Especial ---
        if (val.eh_caracter_especial(palavra[0])):

            if palavra[0] == "'":
                return 'string'
            
            comp = val.comparador(palavra)

            if comp != -1: # Nao e nenhum comparador ou atribuicao
                if comp == 1 or comp == 0: # ==, >=, <= ou !=
                    return 'comparador'
                else: # Atribuicao
                    return 'atribuicao'
            else:
                # --- Operadores aritmeticos ---
                if (val.eh_operador_aritmetico(palavra)): # +, -, / ou *
                    return 'operador_aritmetico'
                else:
                    # --- Caracter ---
                    # ), (, ; ou
                    if val.eh_operador (palavra):
                        return 'separador'

        else:
            # --- Numeros ---
            # 1, 2, ...., 0.1, 0.999,....
            if (val.eh_numero(palavra[0])):
                ok = val.auto_numeros(palavra)
                if (ok):
                    return 'constante'
                else: # Erro, transforma o numero em um identificador
                    return 'identificador'
                
        # --- Palavras reservadas da linguagem ---
        if (palavra in self.lista_palavra_chaves()):
            return 'reservada'
        else:
            # --- Identificador ---
            if (palavra != ''):
                return 'identificador'
    # -------------------------------------------------------------------------------------------------------------------------------


    # -------------------------------------------------------------------------------------------------------------------------------
    def cria_tabela(self):
        """Cria a tabela de token | lexema
            Retorna a tabela de token | lexema"""

        tabela = {'operador_aritmetico': [], 'operador_logico':[], 'comparador': [], 'atribuicao':[],
                  'separador':[], 'constante': [], 'identificador':[], 'reservada': [], 'string':[]}
        return tabela
    # -------------------------------------------------------------------------------------------------------------------------------


    # -------------------------------------------------------------------------------------------------------------------------------
    def adiciona_tabela(self, palavra, tabela, desc_saida):
        """Adciona o valor passado na tabela de tokens|lexemas
        Retorna uma string contendo os erros (se encontrados) e
        a saida do arquivo para aquele lexema formatada"""

        categoria = self.categoria_palavra(palavra)

        # Verifica os identificadores
        if categoria == 'identificador' or categoria == 'constante':
            s = self.criar_id(palavra)
            palavra = s[1:]
            desc_saida = desc_saida + '[{}] '.format(palavra)
            if s[0] == 'N':
                i = s.find(',')
                ident = s[1:i] + s[i+1:]
                tabela[categoria].append(ident)
        else:
            if not palavra in tabela[categoria]:  # Armazena apenas um valor de cada lexema, economizar espaço e melhorar o tempo de busca
                tabela[categoria].append(palavra)

            desc_saida = desc_saida + '[{},] '.format(palavra)
            
        return desc_saida
    # -------------------------------------------------------------------------------------------------------------------------------


    # --- Manipulacao do id ----
    # -------------------------------------------------------------------------------------------------------------------------------
    def criar_id(self, identificador):
        """Cria o id, e retorna-o a partir do arquivo de ids
           Retorna 'FidIndice'
           Onde:
               F = flag que define se o valor esta ou nao no arquivo
               id = string id
               Indice = valor para aquele id

            Por exemplo:
            >>>criar_id('abacaxi','arquivo_ids.txt')
            >>>Nid9

            'abacaxi' e um id novo, nao se encontra no arquivo de ids, e a primeira vez que foi utilizado no codigo
            N = novo
            id = id
            9 = valor do id referente aos outros ids
        """

        # No inicio da string de retorno existe um flag que indica se o id ja estava la
        # logo nao deve ser readicionado na tabela
        # O flag no inicio possui dois valores:
        # A -> indica que o valor ja esta no arquivo
        # N -> inidica que o valor e novo e, portanto, nao esta no aquivo

        # Cria o arquivo, caso nao exista
        try:
            arquivo = open(self.arquivo_id, 'r', encoding='latin-1')
        except IOError: # Cria o arquivo
            arq = open (self.arquivo_id, 'w',  encoding='latin-1')
            arq.write('')
            arq.close()
        arquivo = open(self.arquivo_id, 'r', encoding='latin-1')
        
        for linha in arquivo:
            indice = linha.find(',')
            if linha[indice+1:-1] == identificador:
                arquivo.close()
                return f'Aid,{linha[:indice+1]}'
        
        self.idx_id = self.idx_id + 1
        
        arquivo = open(self.arquivo_id, 'a')
        arquivo.write(f'{self.idx_id},{identificador}\n')
        arquivo.close()

        return f'Nid,{self.idx_id}'
                
            
        
    # -------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------------------------------------
    def cria_tabela_hash(self, tabela = {}):
        indice = {'operador_aritmetico': 1, 'operador_logico': 2, 'comparador': 3, 'atribuicao': 4,
                  'separador': 5, 'constante': 6, 'identificador': 7, 'reservada': 8, 'string': 9}
        s = ''
        for key in tabela.keys():
            v = tabela[key]
            s = s + str(indice[key]) + ';'
            for valor in v:
                s = s + valor + ';'
            s = s + '\n'

        arq_tabela_hash = open(self.tabela_hash, 'w')
        arq_tabela_hash.write(s)
        arq_tabela_hash.close()


    # -------------------------------------------------------------------------------------------------------------------------------

    # --- Cleaner e Scanner ---
    # -------------------------------------------------------------------------------------------------------------------------------
    def cleaner(self):
        """Limpa o arquivo a ser compilado"""
        arquivo = open(self.arquivo_entrada, 'r', encoding='latin-1')

        s = '' # String de saida
        erros  = 'Erros:\n' # String de erros
        
        num_linha = 0 # Numero da linha corrente
        
        
        for linha in arquivo:
            
            erro_na_linha = ''          # Erro em cada linha
            palavra = ''                # 'Buffer'
            l = len(linha)              # Tamanho da linha
            num_linha = num_linha + 1   # Numero da linha
            i = 0                       # Contador da linha
            palavra = ''                # Armazena os caracteres
            desc_saida = ''             # Palavras e separadores de cada linha
            while i < l:
               
                    
                if val.eh_comentario(linha[i:i+2]): # Verifica se e um comentario
                    i = l + 2
                else:
                    if val.caracter_invalido(linha[i]): # Erro, verifica se o caracter nao tem assento
                        palavra = palavra + val.troca_car_erro # Muda o caracter invalido pelo valor de troca_car_erro
                        erro_na_linha = erro_na_linha + 'caracter {} invalido |'.format(linha[i])
                    else:
                          
                        caracter_especial = val.eh_caracter_especial(linha[i])  # Caracteres especiais como ;, ., /, +, ...
                        
                        outro_sep = val.separadores(linha[i])  # ' ', '\n' ou '\t'
                        
                        cmp = val.comparador(linha[i:i + 2])  # >=, ==, <=, < ou > ou =
                            
                        if caracter_especial or outro_sep or cmp != -1:

                            
                            if palavra != '':
                                (ok, palavra_ok) = val.valida_numero(palavra)
                                if not ok: # Se ocorrer erro numerico
                                    erro_na_linha = erro_na_linha + 'numero {} invalido |'.format(palavra)
                                desc_saida = desc_saida + palavra_ok + ' '
                                palavra = ''
                                    
                            if cmp != -1:  # >=, ==, <=, >, < ou =
                                comp = ''
                                if cmp == 1:
                                    comp = linha[i:i+2]
                                    i = i + 2
                                else:
                                    comp = linha[i]
                                desc_saida = desc_saida + comp + ' '
                                
                            else:
                                if caracter_especial:
                                    if (linha[i] == "'"):
                                        (ok, index, string) = val.trata_string(linha[i:])
                                        if not ok:
                                            erro_na_linha = erro_na_linha + 'string invalida {} |'.format(linha[i: i+index-1]) 
                                        desc_saida = desc_saida + string + ' '
                                        i = i + index
                                    else:
                                        desc_saida = desc_saida + linha[i] + ' '
                                    
                                    
                        else:
                            palavra = palavra + linha[i]
                i = i + 1
                
            if desc_saida != '':
                s = s + desc_saida + '\n'

            if erro_na_linha != '':
                erros = '{} Erro na linha [{}]: {}\n'.format(erros, str(num_linha), erro_na_linha)
                erro_na_linha = ''
            
        if palavra != '':
            (ok, palavra_ok) = val.valida_numero(palavra)

            if not ok: # Se ocorrer erro numerico
                erro_na_linha = erro_na_linha + 'numero {} invalido |'.format(palavra)
                
            s = s + palavra_ok
            
        if erro_na_linha != '':
            erros = "{} Erro na linha [{}]: {}\n".format(erros, str(num_linha), erro_na_linha)

        # Arquivo de erros
        arquivo_erros = open(self.arquivo_erros, 'a', encoding='latin-1')
        arquivo_erros.write(erros)
        arquivo_erros.close()
        
        # Arquivo limpo
        arquivo_limpo = open(self.arquivo_limpo, 'a')
        arquivo_limpo.write(s + '\n')
        arquivo_limpo.close()
    # -------------------------------------------------------------------------------------------------------------------------------
    

    # -------------------------------------------------------------------------------------------------------------------------------
    def scanner(self):
        """
        Cria a tabela de token | lexema
        Categoriza os valores conforme o token

        Retorna a tabela se tudo ocorreu normalmente
        ou retorna {} e o erro, caso ocorrido algum erro

        Cria dois arquivos
            1) Contendo a saida formatada com os lexemas, no seguinte padrao: [lexema,]
            2) Contendo os erros encontrados durante a analise"""

        # Cria a tabela
        tabela = self.cria_tabela()

        # Lexema
        lexema = ""

        # String de saida e de erro
        str_saida = ''
        #str_erro = ''

        # Arquivo
        num_linha = 0
        
        # Limpa o arquivo
        self.cleaner()
        arquivo = open(self.arquivo_limpo, 'r')

        for linha in arquivo:
            #num_linha = num_linha + 1
            l = len(linha)  # Tamanho da linha
            i = 0 # Contador

            #desc_erro = ''
            desc_saida = ''
            lexema = ''
            
            while i < l:

                if linha[i] == "'":
                    (ok, index, string) = val.trata_string(linha[i:])
                    i = i + index + 1
                    desc_saida = self.adiciona_tabela(string, tabela, desc_saida)
                if val.separadores(linha[i]):

                    if lexema != '':
                        desc_saida = self.adiciona_tabela(lexema, tabela, desc_saida)
                    lexema = ''
                    
                else:
                    lexema = lexema + linha[i]
                
                i = i + 1

                

            if desc_saida != '':
                str_saida = str_saida + desc_saida + '\n'

        # ---- Armazenando os erros e o arquivo de saida -----
        desc_saida = ''
        #desc_erro = ''
        if lexema != '':
            desc_saida = self.adiciona_tabela(lexema, tabela, desc_saida)
            str_saida = str_saida[:-1] + desc_saida

        # Arquivo
        saida_txt = open(self.arquivo_saida, 'a')
        saida_txt.write(str_saida + '\n')
        saida_txt.close()

        tabela_hs = open(self.tabela_hash, 'a')
        tabela_hs.write(str(tabela))
        tabela_hs.close()

        self.cria_tabela_hash(tabela)

        return tabela
    # -------------------------------------------------------------------------------------------------------------------------------
