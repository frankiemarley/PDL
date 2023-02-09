import ply.lex as lex
import re
import tablaSimbolos

#Palabras reservadas
reservadas = ['INT','BOOLEAN','STRING','IF','DEFAULT','BREAK','RETURN','FUNCTION','SWITCH','CASE','PRINT','LET','INPUT']

#Tokens
tokens = reservadas + ['ID','ENT','CAD','SUM','LLAVEL','LLAVER','PARL','PARR','PUNTS','FIN','COM','NOT','ASIGSUM','ASIG','COMMENT','PR','EQU','NOTEQU']

#Token - String:
mapTokToStr = {
'(\'ENT\', None)' : 'entero',
'(\'CAD\', None)' : 'cadena',
'(\'BOOLEAN\', None)' : 'boolean',
'(\'SUM\', None)' : '+',
'(\'LLAVEL\', None)' : '{',
'(\'LLAVER\', None)' : '}',
'(\'PARL\', None)' : '(',
'(\'PARR\', None)' : ')',
'(\'FIN\', None)' : ';',
'(\'COM\', None)' : ',',
'(\'NOT\', None)' : '!',
'(\'ASIGSUM\', None)' : '+=',
'(\'ASIG\', None)' : '=',
'(\'EQU\', None)' : '==',
'(\'NOTEQU\', None)' : '!=',
'(\'PUNTS\', None)' : ':',
'(\'PR\', 1)' : 'int',
'(\'PR\', 2)' : 'boolean',
'(\'PR\', 3)' : 'string',
'(\'PR\', 4)' : 'if',
'(\'PR\', 5)' : 'default',
'(\'PR\', 6)' : 'break',
'(\'PR\', 7)' : 'return',
'(\'PR\', 8)' : 'function',
'(\'PR\', 9)' : 'switch',
'(\'PR\', 10)' : 'case',
'(\'PR\', 11)' : 'print',
'(\'PR\', 12)' : 'input',
'(\'PR\', 13)' : 'let', 
'(\'ID\', None)' : 'id',
'(\'EOF\', None)' : 'Fin de fichero'
}

def tokToStr(tok):
	if tok[0] in ["CAD", "ID", "BOOLEAN", "ENT"]:
		tok=(tok[0],None)
	return mapTokToStr[str(tok)]

#Tabla de palabras reservadas
valorReservadas = {'INT': 1, 'BOOLEAN': 2, 'STRING': 3, 
'IF': 4, 'DEFAULT': 5, 'BREAK': 6, 'RETURN': 7, 'FUNCTION': 8,
'SWITCH': 9, 'CASE': 10, 'PRINT': 11, 'INPUT': 12,  'LET': 13,
'TRUE': 'true', 'FALSE':'false' }


tablaDeSimbolos = None

#Expresiones Regulares

def t_COMMENT(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
	ncr = t.value.count("\n")
	t.lexer.lineno += ncr


def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_ASIGSUM(t):
	r'\+='
	t.value=None
	return t

def t_EQU(t):
	r'=='
	t.value=None
	return t

def t_SUM(t):
	r'\+'
	t.value=None
	return t

t_ignore = '\t '

def t_LLAVEL(t):
	r'{'
	t.value=None
	return t

def t_LLAVER(t):
	r'}'
	t.value=None
	return t

def t_PARL(t):
	r'\('
	t.value=None
	return t

def t_PARR(t):
	r'\)'
	t.value=None
	return t

def t_FIN(t):
	r';'
	t.value=None
	return t

def t_COM(t):
	r','
	t.value=None
	return t

def t_PUNTS(t):
	r':'
	t.value=None
	return t

def t_NOTEQU(t):
	r'!='
	t.value=None
	return t

def t_NOT(t):
	r'!'
	t.value=None
	return t

def t_ASIG(t):
	r'='
	t.value=None
	return t

#Funciones
def t_ID(t):
	r'[a-zA-Z]+[a-zA-Z_0-9]*'
	lexema = t.value
	t.value=valorReservadas.get(t.value.upper(), 0)
	#print('Entrando en tID')
	#print(t.value)
	#Vemos si es cte booleana o PR
	if(t.value!=0):
		if t.value=='true':
			t.type='BOOLEAN'
			t.value=1
		elif t.value=='false':
			t.type='BOOLEAN'
			t.value=0
		else:
			t.type='PR'
	else:
		t.value=tablaDeSimbolos.insertaNuevoID(lexema)
	return t

def t_ENT(t):
	r'\d+'
	t.type='ENT'
	if int(t.value) > 32767:
		raise Exception('ERROR Lexito en linea '+ str(t.lexer.lineno) +': Entero supera el tamaño máximo')
	t.value=int(t.value)
	return t

def t_CAD(t):
	r'(\"([^\\\n]|(\\(.|\n)))*?\")'
	if int(len(t.value)) > 64:
		raise Exception('ERROR Lexito en linea '+ str(t.lexer.lineno) +': Cadena supera el tamaño máximo')
	t.value = '\"' +t.value[1:-1] +'\"'
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

class AnalizadorLex:
	#Constructor
	def __init__(self, ts=None):
		self.lexer = lex.lex()
		self.ftokens = open("tokens.txt","w+")
		global tablaDeSimbolos
		tablaDeSimbolos = ts

	def anyadirToken(self, tok):
		self.ftokens.write('<' + tok.type + ','+ NoneOrString(tok.value) + '>\n')

#Funcion auxiliar que imprime vacio si es None o directamente el
#string argumento s en caso contrario
def NoneOrString(s):
	if s is None:
		return ''
	return str(s)

#Funcion Main
def main():
	analizador = lex.lex()
	global tablaDeSimbolos
	tablaDeSimbolos = tablaSimbolos.TablaSimbolos()

	nFichero = input("Inserta nombre de fichero:")
	handle = open(nFichero)
	cadena = handle.read()
	print(cadena)
	analizador.input(cadena)
	ftokens = open("tokens.txt","w+")

	tok = analizador.token()
	while tok is not None:
		#print(f'hola,{tok}')
		if not tok :
			print("Token erroneo:",tok)
			break
		print('<' + tok.type + ','+ NoneOrString(tok.value) + ',linea:'+str(analizador.lineno)+'>')
		ftokens.write('<' + tok.type + ','+ NoneOrString(tok.value) + '>\n')
		try:
			tok = analizador.token()
		except Exception as error:
			print(repr(error))
			ftokens.close()
			return
	ftokens.close()

if __name__ == '__main__':
	main()
