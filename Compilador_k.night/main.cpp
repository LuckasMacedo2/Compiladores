#include <iostream>
using std::cout;
using std::cin;
using std::string;
using std::endl;

#include <fstream>
using std::ifstream;
using std::ofstream;

#include <stdlib.h> // system

enum categorias {
    operador_aritmetico = 1,
    operador_logico = 2,
    comparador = 3,
    atribuicao = 4,
    separador = 5,
    constante = 6,
    identificador = 7,
    reservada = 8,
    str = 9
};

int main(){
    string ARQUIVO_PY = "main.py";
    string CAMINHO = "Lexer\\";
    string ARQUIVO_COMPILAR = "teste.txt"; 
    int erro = system(("python " + CAMINHO + ARQUIVO_PY + " " + ARQUIVO_COMPILAR).c_str());
    if (erro)
    {
        cout<<"ERRO Nao foi possivel compilar o lexer! Talvez o arquivo nao foi passado corretamente"<<endl;
    }
}