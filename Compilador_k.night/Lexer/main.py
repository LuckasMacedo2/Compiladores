import sys
import lexer as lx
import os # Para voltar um nivel
for i in range(1, len(sys.argv)):
    caminho = os.path.abspath(os.path.dirname(__file__)) # Voltar um nivel
    l = len(caminho) - 1
    while caminho[l] != '\\':
        l = l - 1
    lexer = lx.Lexer(caminho[:l] + "\\" + sys.argv[i])
    lexer.scanner()
