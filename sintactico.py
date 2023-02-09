import lexico
import tablaSimbolos

class AnalizadorSinSem:
    #Constructor
    def __init__(self):
        self.ts = tablaSimbolos.TablaSimbolos()
        self.lx = lexico.AnalizadorLex(self.ts)
        self.sigToken = None
        self.fichParse = open("parse.txt","w+")

    #Funciones parse
    def P(self):
        first1 = [("PR",6), ("ID",None), ("PR",4), ("PR",12), ("PR",13), ("PR",11), ("PR",7), ("PR",9)]     #First(P)={break, id, if, input, let, print, return, switch }
        first2 = [("PR",8)]     #First(P)={function}
        first3 = [("$",None)]   #First(P)={$}

        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 1')
            self.B()
            self.P()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 2')
            self.F()
            self.P()
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 3')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')

    def B(self):
        first1 = [("PR",13)]    #First(let id T ;)={ let }
        first2 = [("PR",4)]     #First(if ( E ) S)={ if }
        first3 = [("PR",9)]     #First(switch ( E ) { D })={ switch }
        first4 = [("PR",6), ("ID",None), ("PR",12), ("PR",11), ("PR",7) ]   #First(S)={ break id input print return }

        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 4')
            self.equiparaToken(("PR",13))   
            self.equiparaToken(("ID",None))
            self.T()
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 5')
            self.equiparaToken(("PR",4))
            self.equiparaToken(("PARL",None))
            self.E()
            self.equiparaToken(("PARR",None))
            self.S()
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 6')
            self.equiparaToken(("PR",9))
            self.equiparaToken(("PARL",None))
            self.E()
            self.equiparaToken(("PARR",None))
            self.equiparaToken(("LLAVEL",None))
            self.D()
            self.equiparaToken(("LLAVER",None))
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 7')
            self.S()
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')

    def C(self):
        first1 = [("PR",6),("ID",None),("PR",4),("PR",12),("PR",13),("PR",11),("PR",7),("PR",9) ] #First(B C)={ break id if input let print return switch   }
        first2 = [("PR",10),("PR",5),("LLAVER",None),] #Follow(C)={ case default } }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 8')
            self.B()
            self.C()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 9')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta.')
            
    def D(self):
        first1 = [("PR",10)] #First(case ENT : C D)={ case }
        first2 = [("PR",5)] #First(default : C)={ default }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 10')
            self.equiparaToken(("PR",10))
            self.equiparaToken(("ENT",None))
            self.equiparaToken(("PUNTS",None))
            self.C()
            self.D()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 11')
            self.equiparaToken(("PR",5))
            self.equiparaToken(("PUNTS",None))
            self.C()
        else:
            raise Exception('ERROR Sintactico: sentencia case/default incorrecta.')


    def T(self):
        first1 = [("PR",1)] #First(int)={ int }
        first2 = [("PR",2)] #First(bool)={ bool }
        first3 = [("PR",3)] #First(string)={ string }
       
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 12')
            self.equiparaToken(("PR",1))
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 13')
            self.equiparaToken(("PR",2))
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 14')
            self.equiparaToken(("PR",3))
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. Se espera un tipo basico del lenguaje y se ha recibido.')


    def F(self):
        first1 = [("PR",8)] #First(function id H ( A ) { C })={ function }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 15')
            self.equiparaToken(("PR",8))
            self.equiparaToken(("ID",None))
            self.H()
            self.equiparaToken(("PARL",None))
            self.A()
            self.equiparaToken(("PARR",None))
            self.equiparaToken(("LLAVEL",None))
            self.C()
            self.equiparaToken(("LLAVER",None))
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')

    def S(self):
        first1 = [("ID",None)] #First( id S')={ id }
        first2 = [("PR",7)] # First( return X ;)={ return }
        first3 = [("PR",11)] #First( print ( E ) ;)={ print }
        first4 = [("PR",12)] #First( input id ;)={ input }
        first5 = [("PR",6)] #First( break ;)={ break }
       
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 16')
            self.equiparaToken(("ID",None))
            self.S_()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 17')
            self.equiparaToken(("PR",7))
            self.X()
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 18')
            self.equiparaToken(("PR",11)) 
            self.E()         
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 19')
            self.equiparaToken(("PR",12))
            self.equiparaToken(("ID",None))
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first5)):
            self.fichParse.write(' 20')
            self.equiparaToken(("PR",6))
            self.equiparaToken(("FIN",None))
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')


    def S_(self):
        first1 = [("ASIG",None)] #First(= E ;)={ = }
        first2 = [("ASIGSUM",None)] #First(+= E ;)={ += }
        first3 = [("PARL",None)] #First(( L ) ;)={ ( }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 21')
            self.equiparaToken(("ASIG",None))
            self.E();
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 22')
            self.equiparaToken(("ASIGSUM",None))
            self.E();
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 23')
            self.equiparaToken(("PARL",None))
            self.L()
            self.equiparaToken(("PARR",None))
            self.equiparaToken(("FIN",None))
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')

    def H(self):
        first1 = [("PR",2), ("PR",1), ("PR",3)] #First(T)={ bool int string }
        first2 = [("PARL",None)] #Follow(H)={ ( }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 24')
            self.T()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 25')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. El tipo de retorno de una funcion debe ser un tipo basico o vacio y se ha recibido.')
        

    def L(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None),("ENT",None),("boolean",None),("ID",None)] #First(E Q)={ ! ( boolean CAD ENT id }
        first2 = [("PARR",None)] #Follow(L)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 26')
            self.E()
            self.Q()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 27')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. Error en llamada de funcion. ')


    def Q(self):
        first1 = [("COM",None)] #First(, E Q)={ , }
        first2 = [("PARR",None)] #Follow(Q)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 28')
            self.equiparaToken(("COM",None))
            self.E()
            self.Q()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 29')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. Error en llamada de funcion. ')

    def X(self):
        first1 = [("NOT",None), ("PARL",None), ("CAD",None), ("ENT",None), ("boolean",None),("ID",None)] #First(E)={ ! (  CAD ENT boolean id }
        first2 = [("FIN",None)] #Follow(X)={ ; }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 30')
            self.E()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 31')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta')        

    def A(self):
        first1 = [("PR",2), ("PR",1),  ("PR",3)] #First(T id K)={ bool int string }
        first2 = [("PARR",None)] #Follow(A)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 32')
            self.T()
            self.equiparaToken(("ID",None))
            self.K()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 33')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. Parametros formales de declaracion de funcion incorrectos.')

    def K(self):
        first1 = [("COM",None)] #First(, T id K)={ , }
        first2 = [("PARR",None)] #Follow(K)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 34')
            self.equiparaToken(("COM",None))
            self.T()
            self.equiparaToken(("ID",None))
            self.K()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 35')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta. Parametros formales de declaracion de funcion incorrectos.')
        

    def E(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None), ("ENT",None), ("boolean",None),("ID",None)]#First(R E')={ ! (  CAD ENT boolean id }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 36')
            self.R()
            self.E_()
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')
    

    def E_(self):
        first1 = [("EQU",None)] #First(== R E')={ == }
        first2 = [("NOTEQU",None)] #First(!= R E')={ != }
        first3 = [("PARR",None),("COM",None),("FIN",None)] #Follow(E')={ ) , ; }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 37')
            self.equiparaToken(("EQU",None))
            self.R()
            self.E_()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 38')
            self.equiparaToken(("NOTEQU",None))
            self.R()
            self.E_()
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 39')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')


    def R(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None),("ENT",None),("boolean",None),("ID",None)] #First(U R')={ ! ( CAD ENT boolean id }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 40')
            self.U()
            self.R_()
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')


    def R_(self):
        first1 = [("SUM",None)] #First(+ U R') = { + }
        first2 = [ ("NOTEQU",None), ("PARR",None), ("COM",None), ("FIN",None),("EQU",None)] #Follow(R')={ != ) , ; == }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 41')
            self.equiparaToken(("SUM",None))
            self.U()
            self.R_()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 42')          
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')

    def U(self): #//
        first1 = [("NOT",None)] #First(! U)={ ! }
        first2 = [("ID",None)] #First(id U')={ id }
        first3 = [("PARL",None)] #First(( E ))={ ( }
        first4 = [("ENT",None)] #First(ENT)={ ENT }
        first5 = [("CAD",None)] #First(CAD)={ CAD }
        first6 = [("boolean",None)] #First(boolean)={ boolean }

        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 43')
            self.equiparaToken(("NOT",None))
            self.U()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 44')
            self.equiparaToken(("ID",None))
            self.U_()
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 45')
            self.equiparaToken(("PARL",None))
            self.E()
            self.equiparaToken(("PARR",None))
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 46')
            self.equiparaToken(("ENT",None))
        elif (self.tokenInFirst(first5)):
            self.fichParse.write(' 47')
            self.equiparaToken(("CAD",None))
        elif (self.tokenInFirst(first6)):
            self.fichParse.write(' 48')
            self.equiparaToken(("boolean",None))
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')


    def U_(self): 

        first1 = [("PARL",None)] # First(( L ))={ ( }
        first2 = [("NOTEQU",None), ("PARR",None), ("SUM",None), ("NOTEQU",None), ("COM",None), ("FIN",None), ("EQU",None)] #Follow(U')={ != ) + , ; == }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 49')
            self.equiparaToken(("PARL",None))
            self.L()
            self.equiparaToken(("PARR",None))
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 50')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta: Expresion mal construida.')

    #Funcion auxiliar equiparaToken:
    #Tiene como parametro de entrada una tupla (type,value) del token
    def equiparaToken(self,tok):
        if (tok[0] == self.sigToken[0] and tok[1] == self.sigToken[1]) or (tok[0] == self.sigToken[0] and self.sigToken[0] in ["CAD", "ID", "boolean", "ENT"]) :
            st1 = self.lx.lexer.token()
            if (st1 is not None): #Cargamos el primer token
                self.sigToken = (st1.type, st1.value)
                self.lx.anyadirToken(st1)
                #print(self.sigToken[0], self.sigToken[1]) #Para ver los tokens
            else:
                self.sigToken = ("$", None)
                print("$")
        else:
            raise Exception('ERROR Sintactico: token recibido distinto al esperado.')

    #Funcion auxiliar tokenInFirst:
    def tokenInFirst(self,first):
        if self.sigToken in first:
            return True
        elif self.sigToken[0] in ["CAD", "ID", "boolean", "ENT"]:
            return (self.sigToken[0], None) in first
        else:
            return False

    #Cierra todos los ficheros de salida
    def closeFiles(self):
        self.fichParse.close()
        self.lx.ftokens.close()
        self.ts.fichTS.close()

def main():
    an = AnalizadorSinSem()
    nombreFichero = input("Inserta nombre de fichero:")
    handle = open(nombreFichero)
    cadena = handle.read()
    an.lx.lexer.input(cadena)
    an.fichParse.write('Des')
    try:
        st1 = an.lx.lexer.token() #Cargamos el primer token
        if (st1 is not None):
            an.sigToken = (st1.type, st1.value)
            #print(an.sigToken[0], an.sigToken[1]) #Para ver el primer token
            an.lx.anyadirToken(st1)
            an.P()
            print('Compilación del fichero fuente \''+nombreFichero+'\' finalizada correctamente.\n')
            an.ts.volcarTS()
        else:
            print("Fichero fuente vacío \n")
        an.closeFiles()
    except Exception as error:
        #an.ts.imprimirTSG()
        an.ts.volcarTS()
        print('Error de compilacion:\n'+repr(error))
        an.closeFiles()
        return

if __name__ == '__main__':
	main()
