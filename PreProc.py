import re
import sys

#Funcao para ler um arquivo .c
def lerArq(arq):
	try:
		arquivo = open(arq, "r")
		codigoCEmTexto = arquivo.read()
		return codigoCEmTexto
	except:
		return "Arquivo nao existente"

#Funcao para expandir os include's
def include(codigoTodo):
	nomesInc = re.findall(r'\#include\s?\<?\"?(\w+\.\w+)\>?\"?', codigoTodo)
	# print(nomesInc)

	for nomeInc in nomesInc:
		biblio = lerArq(nomeInc)
		codigoTodo = re.sub(r'\#include\s?\<?\"?{}\>?\"?'.format(nomeInc), biblio, codigoTodo)
		
	return codigoTodo

#Funcao para substituir as constantes por seus respectivos valores
def define(codigoTodo):
	defis = re.findall(r'\#define\s\s*(\w\w*)\s\s*(.*)', codigoTodo)

	for defi in defis:
		codigoTodo = codigoTodo.replace(defi[0], defi[1])
		codigoTodo = codigoTodo.replace("#define {} {}".format(defi[1], defi[1]), "")

	return codigoTodo

def trataCodigo(codigoTodo):
	#Expressao regular que remove comentarios de linha
	codigoTodo = re.sub(r'\/\/(.*)', "", codigoTodo)

	#Expressao regular que remove todos os espacos, quebras de linha e tabulacoes
	codigoTodo = re.sub(r'\s|\n|\t', " ", codigoTodo)

	#Expressao regular que remove comentarios de bloco
	codigoTodo = re.sub(r'\/\*(.*?)\*\/', "", codigoTodo)
	
	#Expressao regular que remove os espacos duplicados
	codigoTodo = re.sub(r'\s\s*', " ", codigoTodo)

	#Expressao regular que remove espacos desnecessarios
	codigoTodo = re.sub(r'\s*\;\s*', ";", codigoTodo)
	codigoTodo = re.sub(r'\s*\(\s*', "(", codigoTodo)
	codigoTodo = re.sub(r'\s*\)\s*', ")", codigoTodo)
	codigoTodo = re.sub(r'\s*\{\s*', "{", codigoTodo)
	codigoTodo = re.sub(r'\s*\}\s*', "}", codigoTodo)
	codigoTodo = re.sub(r'\s*\,\s*', ",", codigoTodo)
	codigoTodo = re.sub(r'\s*\=\s*', "=", codigoTodo)
	codigoTodo = re.sub(r'\s*\+\s*', "+", codigoTodo)
	codigoTodo = re.sub(r'\s*\-\s*', "-", codigoTodo)
	codigoTodo = re.sub(r'\s*\*\s*', "*", codigoTodo)
	codigoTodo = re.sub(r'\s*\\/\s*', "/", codigoTodo)

	return codigoTodo

nome = sys.argv[1]
textoEmC = lerArq(nome)

textoEmC = include(textoEmC)
textoEmC = define(textoEmC)

textoEmC = trataCodigo(textoEmC)

arqFinal = open("preprocessado.c", "w")
arqFinal.write(textoEmC)
