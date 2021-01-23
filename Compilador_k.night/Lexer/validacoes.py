# Arquivo que contem as verificacoes de caracteres e validacoes dos mesmos



# --------------------------------- Variaveis Globais ---------------------------------------------------------------------------
global troca_car_erro # Variavel que trata os erros, tornando o lexema errado em um identificador
troca_car_erro = 'a'
# ------------------------------END Variaveis Globais ---------------------------------------------------------------------------


# --- Validacoes ---
# -------------------------------------------------------------------------------------------------------------------------------
def valida_numero(palavra):
    """
    Valida o numero transformando-o em um identificador.

    Por exemplo
    >>>valida_num(11111)
    >>>(True, 11111)

    >>>valida_num(1a1)
    >>>(False, aa1)"""

    flag = 0 # Conta a quantidade de '.'
    flag2 = False # Verifica se houve alguma letra no numero
    word = ''
    r = True # Verifica se ocorreu erro
    
    if eh_numero(palavra[0]): # Verifica se e numero
        word = palavra[0] # Palavra similar ao lexema
        l = len (palavra) # Tamanho da palavra
        
        for i in range(1, l):
            pontos = 0 # Ocorreu erro de '.'
            if palavra[i] == '.':
                flag = flag + 1 # Contador de '.'
                if flag > 1:
                    r = False
                    pontos = 1 # Recebe 1 quando existe mais de um '.'
                
            if (eh_letra(palavra[i]) or palavra[i] == '_') and not flag2:
                r = False
                flag2 = True
                
            if pontos:
                word = word + troca_car_erro
            else:
                word = word + palavra[i]
                
    else:
        return r, palavra

    if flag > 1:
        indice = word.find('.')
        word = word[:indice] + troca_car_erro + word[indice+1:]
        flag2 = True
    
    if flag2:
        word = troca_car_erro + word
    
    return r, word
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def busca(palavra, caracter):
    l = len(palavra)

    for i in range(0, l):
        if palavra[i] == caracter:
            return i
    return -1
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def trata_string(linha):
    """
    Trata a string e retorna se comeca e termina com ' e a mesma tratada e a posicao em que termina

    Por exemplo:
    >>>trata_string('string')
    >>>(True, 7, 'string')

    >>>trata_string('abacaxi)
    >>>(False, 7, 'abacaxi')
    """

    index = busca(linha[1:], "'")

    if (index == -1):
        return (False, len(linha), linha[:-1] + "'")
    else:

        return (True, index + 1, linha[:index+1] + "'")
# -------------------------------------------------------------------------------------------------------------------------------



# --- Automato que reconhece numeros ---
# -------------------------------------------------------------------------------------------------------------------------------
def auto_numeros(numero):
    """Define se o valor passado é um valor numerico.
    Retorna uma tupla contendo (True ou False, mensagem)
    Recebi como paramêtro uma string contendo o número e a linha ao qual o mesmo pertenci


    Por exemplo:
    >>>auto_numeros(1)
    >>>True

    >>>auto_numeros(1a1)
    >>>False"""

    l = len(numero)  # Tamanho da palavra. l = |numero|
    i = 0  # Contador
    flag = 0  # Conta a quantidadde de '.' no numero, deve se existir apenas 1.

    # Verificando se o numero é 0 ou 0.XX....
    if (ord(numero[0]) == 48 and l >= 2):
        if (ord(numero[1]) != 46):  # Se comecar com 0 tem de possuir um ponto apos, ou ser o proprio zero
            return False
        else:
            flag = flag + 1

    # Percorrendo os caracteres
    while (i < l):
        if (ord(numero[i]) == 46):  # Verifica se é '.'
            flag = flag + 1  # Pode existir apenas um '.'
            if (flag > 2):
                return False
        else:
            # Não está dentro do intervalo na tabela ascii
            if (not (eh_numero(numero[i]))):
                return False
        i = i + 1
    return True
    # Se o numero for invalido ja retorna sem tratar ele
# -------------------------------------------------------------------------------------------------------------------------------


# --- Manipulacao de caracteres ---
# -------------------------------------------------------------------------------------------------------------------------------
def eh_numero(num):
    """Define se o valor esta entre (48, 57) que são os valores
    da tabela ascii destinada aos numeros.
    Recebi como paramêtro um caracter.

    Por exemplo:
    >>>eh_numero('4')
    >>>True

    >>>eh_numero('a')
    >>>False"""

    return ord(num) >= 48 and ord(num) <= 57
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def eh_caracter_especial(caracter):
    """Retorna se um numero e um caractere especial
    Recebi como paramêtro um caracter

    Por exemplo:
    >>>eh_caracter_especial(',')
    >>>True

    >>>eh_caracter_especial('a')
    >>>False"""

    #lim1 = (ord(caracter) >= 33 and ord(caracter) <= 45 or ord(caracter) == 47)  # !, ", #, $, %, &, ', (, ), *, +, ,, -, /
    #lim2 = (ord(caracter) >= 58 and ord(caracter) <= 64)  # :, ; <, =, >,  ?
    #lim3 = (ord(caracter) >= 91 and ord(caracter) <= 93)  # [, \, ]
    #lim4 = (ord(caracter) >= 123 and ord(caracter) <= 126)  # {, |, }
    return caracter in "'+-*/%(),;<>=[]{}"
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def eh_letra(caracter):
    """Define se o valor esta entre (65, 90) que são os valores
    da tabela ascii destinada as letras maiusculas.
    Recebi como parametro um caracter que e convertido automaticamente para
    letra maiuscula


    Por exemplo:
    >>>eh_numero('a')
    >>>True

    >>>eh_numero('1')
    >>>False"""

    return (ord(caracter.upper()) >= 65 and ord(caracter.upper()) <= 90)
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def caracter_invalido(caracter):
    """ Verifica se o caracter e invalido
    ou seja se contem acentuacoes, etc

    Por exemplo:
    >>>caracter_invalido('a')
    >>>True

    >>>caracter_invalido('á')
    >>>False
    
    """
    return ord(caracter) > 127 # Esta fora do alfabeto da tabela ascii
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def eh_comentario(palavra):
    """ Verifica se a palavra passada e o simbolo de comentario
    ou seja, verifica se e '//'

    >>>eh_comentario('//')
    >>>True
    >>>eh_comentario('aa')
    >>>False
    """

    if palavra == '//':
        return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def comparador(palavra):
    """Verifica se o valor passado como parametro e um comparador
    '==', '>=', '<=', '<' ou '>'

    Por exemplo:
    >>>comparador('==')
    >>>1

    >>>comparador('=')
    >>>False"""
    l = len(palavra)
    # 1 -> !=, >=, <=, ==
    # 0 -> <, >
    # 3 -> =
    # -1 -> Nenhum deles

    if palavra == '!=' or palavra == '>=' or palavra == '<=' or palavra == '==':
        return 1
    elif palavra[0] == '<' or palavra[0] == '>':
        return 0
    elif palavra[0] == '=':
        return 2
    return -1
            
        
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def eh_operador (palavra):
    if (palavra == ')' or palavra == '(' or palavra == ';' or palavra == ','):
        return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def eh_operador_aritmetico(palavra):
    if (palavra == '+' or palavra == '-' or palavra == '/' or palavra == '*' or palavra == '%' or palavra == '^'):
        return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def letra_ou_numero(caracter):
    """Verifica se o caracter e uma letra ou um numero ou o caracter '.'

    Por exemplo:
    >>>letra_ou_numero('0')
    >>>True

    >>>letra_ou_numero('a')
    >>>True

    >>>letra_ou_numero('.')
    >>>True

    >>>letra_ou_numero('+')
    >>>False"""

    if eh_letra(caracter) or eh_numero(caracter) or caracter == '.':
        return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------
def separadores(caracter):
    """Verifica se o caracter e ' ', '\n' ou '\t'
    que sao separadores

    Por exemplo:
    >>>outros_separadores(' ')
    >>>True

    >>>outros_separadores('a')
    >>>False"""

    if caracter == ' ' or caracter == '\n' or caracter == '\t':
        return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------
