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
            self.B(False)
            self.P()
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 2')
            self.F()
            self.P()
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 3')
        else:
            raise Exception('ERROR Sintactico: sintaxis incorrecta en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')

    def B(self,bSwitch):
        first1 = [("PR",13)]    #First(let id T ;)={ let }
        first2 = [("PR",4)]     #First(if ( E ) S)={ if }
        first3 = [("PR",9)]     #First(switch ( E ) { D })={ switch }
        first4 = [("PR",6), ("ID",None), ("PR",12), ("PR",11), ("PR",7) ]   #First(S)={ break id input print return }

        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 4')
            self.equiparaToken(("PR",13))
            self.ts.declaracion = True
            pos = self.sigToken[1]
            self.equiparaToken(("ID",None))
            tTipo = self.T()
            self.ts.insertaTipoTS(pos,('let',tTipo))
            self.ts.insertaDespTS(pos,tTipo)      
            self.ts.declaracion = False
            self.equiparaToken(("FIN",None))
            bTipoRet='tipo_vacio'
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 5')
            self.equiparaToken(("PR",4))
            self.equiparaToken(("PARL",None))
            eTipo=self.E()
            self.equiparaToken(("PARR",None))
            if eTipo is not 'boolean':
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': La condición del \'if\' debe ser de tipo booleano y se ha introducido una expresión de tipo: '+str(eTipo)+'.')
            sSwitch=bSwitch
            sTipoRet=self.S(sSwitch)
            bTipoRet=sTipoRet
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 6')
            self.equiparaToken(("PR",9))
            self.equiparaToken(("PARL",None))
            eTipo=self.E()
            self.equiparaToken(("PARR",None))
            if eTipo is not 'int':
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': La condición del \'switch\' debe ser de tipo booleano y se ha introducido una expresión de tipo: '+str(eTipo)+'.')
            self.equiparaToken(("LLAVEL",None))
            dTipoRet=self.D()
            self.equiparaToken(("LLAVER",None))
            bTipoRet=dTipoRet
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 7')
            sSwitch=bSwitch
            sTipoRet=self.S(sSwitch)
            bTipoRet=sTipoRet
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')
        return bTipoRet

    def C(self,cSwitch):
        first1 = [("PR",6),("ID",None),("PR",4),("PR",12),("PR",13),("PR",11),("PR",7),("PR",9) ] #First(B C)={ break id if input let print return switch   }
        first2 = [("PR",10),("PR",5),("LLAVER",None),] #Follow(C)={ case default } }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 8')
            bSwitch=cSwitch
            c1Switch=cSwitch
            bTipoRet=self.B(bSwitch)
            c1TipoRet=self.C(c1Switch)
            if bTipoRet == c1TipoRet:
                cTipoRet=c1TipoRet
            elif bTipoRet is 'tipo_vacio':
                cTipoRet=c1TipoRet
            elif c1TipoRet is 'tipo_vacio':
                cTipoRet=bTipoRet
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': sentencias de retorno en funcion inconsistentes.')     
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 9')
            cTipoRet='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta.')
        return cTipoRet 

    def D(self):
        first1 = [("PR",10)] #First(case ENT : C D)={ case }
        first2 = [("PR",5)] #First(default : C)={ default }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 10')
            self.equiparaToken(("PR",10))
            self.equiparaToken(("ENT",None))
            self.equiparaToken(("PUNTS",None))
            cSwitch=True
            cTipoRet=self.C(cSwitch)
            d1TipoRet=self.D()
            if cTipoRet == d1TipoRet:
                dTipoRet=cTipoRet
            elif cTipoRet is 'tipo_vacio':
                dTipoRet=d1TipoRet
            elif d1TipoRet is 'tipo_vacio':
                dTipoRet=cTipoRet
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': sentencias de retorno en funcion inconsistentes dentro de sentencia switch.')        
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 11')
            self.equiparaToken(("PR",5))
            self.equiparaToken(("PUNTS",None))
            cSwitch=True
            cTipoRet=self.C(cSwitch)
            dTipoRet=cTipoRet
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sentencia case/default incorrecta.')
        return dTipoRet

    def T(self):
        first1 = [("PR",1)] #First(int)={ int }
        first2 = [("PR",2)] #First(boolean)={ boolean }
        first3 = [("PR",3)] #First(string)={ string }
       
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 12')
            self.equiparaToken(("PR",1))
            tTipo='int'
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 13')
            self.equiparaToken(("PR",2))
            tTipo='boolean'
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 14')
            self.equiparaToken(("PR",3))
            tTipo='string'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. Se espera un tipo basico del lenguaje y se ha recibido: \"' +lexico.tokToStr(self.sigToken)+'\".')
        return tTipo

    def F(self):
        first1 = [("PR",8)] #First(function id H ( A ) { C })={ function }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 15')
            self.equiparaToken(("PR",8))
            self.ts.declaracion = True
            pos = self.sigToken[1]
            self.equiparaToken(("ID",None))
            hTipo=self.H()
            self.ts.crearTSL(pos)
            self.equiparaToken(("PARL",None))
            aTipo=self.A()
            self.equiparaToken(("PARR",None))
            self.ts.insertaTipoTS(pos,('function',(aTipo,hTipo)))
            self.ts.declaracion = False
            self.equiparaToken(("LLAVEL",None))
            cTipoRet=self.C(False)
            if cTipoRet != hTipo:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': el tipo de retorno de la función declarado: '+hTipo+' no coincide con el tipo devuelto: '+cTipoRet+'.')
            self.ts.destruirTSL()
            self.equiparaToken(("LLAVER",None))
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')

    def S(self,sSwitch):
        first1 = [("ID",None)] #First( id S')={ id }
        first2 = [("PR",7)] # First( return X ;)={ return }
        first3 = [("PR",11)] #First( print ( E ) ;)={ print }
        first4 = [("PR",12)] #First( input id ;)={ input }
        first5 = [("PR",6)] #First( break ;)={ break }    
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 16')
            posTS = self.sigToken[1]
            tipoID=self.ts.buscaTipo(posTS)
            self.equiparaToken(("ID",None))
            line=str(self.lx.lexer.lineno)
            s_Tipo=self.S_()
            if tipoID[0] is 'function': #pp1
                if tipoID[1][0] != s_Tipo:
                    raise Exception('ERROR Semantico en linea '+ line +': llamada a función que pide '+str(tipoID[1][0])+ ' con parámetro incorrectos'+str(s_Tipo))
            elif tipoID[0] in ['let','arg']: #
                if type(s_Tipo)==list:
                    raise Exception('ERROR Semantico en linea '+ line +':la variable no es de tipo función y por lo tanto no puede hacerse una llamada.')
                elif tipoID[1] != s_Tipo:
                    raise Exception('ERROR Semantico en linea '+ line +': se intenta asignar a una variable de tipo '+str(tipoID[1])+ ' un valor de tipo '+str(s_Tipo))
            else:
                raise Exception('ERROR Semantico en linea '+ line +': error.')
            sTipoRet='tipo_vacio'
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 17')
            self.equiparaToken(("PR",7))
            if self.ts.TSactual is not self.ts.TSL:
                raise Exception('ERROR Semantico en linea '+  str(self.lx.lexer.lineno) +': sentencia return fuera de funcion')
            xTipo=self.X()
            sTipoRet=xTipo
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 18')
            self.equiparaToken(("PR",11)) 
            eTipo=self.E()  
            if eTipo not in['int','boolean','string']:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': print() debe llamarse con un argumento de tipo entero, booleano o string.')
            else:
                sTipoRet='tipo_vacio'
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 19')
            self.equiparaToken(("PR",12))
            posTS = self.sigToken[1]
            tipoID=self.ts.buscaTipo(posTS)
            self.equiparaToken(("ID",None))
            if tipoID[1] not in['int','string']:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': prompt() debe llamarse con una variable de tipo entero o string como argumento y ha recibido una variable de tipo'+tipoID[1]+'.')
            else:
                sTipoRet='tipo_vacio'
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first5)):
            self.fichParse.write(' 20')
            self.equiparaToken(("PR",6))
            if sSwitch is False:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': break fuera de sentencia switch.')
            else:
                sTipoRet='tipo_vacio'
            self.equiparaToken(("FIN",None))
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')
        return sTipoRet

    def S_(self):
        first1 = [("ASIG",None)] #First(= E ;)={ = }
        first2 = [("ASIGSUM",None)] #First(+= E ;)={ += }
        first3 = [("PARL",None)] #First(( L ) ;)={ ( }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 21')
            self.equiparaToken(("ASIG",None))
            eTipo=self.E();
            self.equiparaToken(("FIN",None))
            s_Tipo=eTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 22')
            self.equiparaToken(("ASIGSUM",None))
            eTipo=self.E();
            if eTipo is'int':
                s_Tipo=eTipo
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': la sentencia de asignacion con resta solo admite operandos enteros y no de tipo '+eTipo+'.')
            self.equiparaToken(("FIN",None))
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 23')
            self.equiparaToken(("PARL",None))
            lTipo=self.L()
            self.equiparaToken(("PARR",None))
            self.equiparaToken(("FIN",None))
            s_Tipo=lTipo
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')
        return s_Tipo

    def H(self):
        first1 = [("PR",2), ("PR",1), ("PR",3)] #First(T)={ boolean int string }
        first2 = [("PARL",None)] #Follow(H)={ ( }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 24')
            tTipo=self.T()
            hTipo = tTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 25')
            hTipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. El tipo de retorno de una funcion debe ser un tipo basico o vacio y se ha recibido: \"' +lexico.tokToStr(self.sigToken)+'\".')
        return hTipo

    def L(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None),("ENT",None),("boolean",None),("ID",None)] #First(E Q)={ ! ( boolean CAD ENT id }
        first2 = [("PARR",None)] #Follow(L)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 26')
            eTipo=self.E()
            qTipo=self.Q()
            if qTipo is 'tipo_vacio':
                lTipo=[eTipo]
            else:
                qTipo.insert(0,eTipo)
                lTipo=qTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 27')
            lTipo=['tipo_vacio']
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. Error en llamada de funcion. ')
        return lTipo

    def Q(self):
        first1 = [("COM",None)] #First(, E Q)={ , }
        first2 = [("PARR",None)] #Follow(Q)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 28')
            self.equiparaToken(("COM",None))
            eTipo=self.E()
            q1Tipo=self.Q()
            if q1Tipo is 'tipo_vacio':
                qTipo = [eTipo]
            else:
                q1Tipo.insert(0,eTipo)
                qTipo = q1Tipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 29')
            qTipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. Error en llamada de funcion. ')
        return qTipo

    def X(self):
        first1 = [("NOT",None), ("PARL",None), ("CAD",None), ("ENT",None), ("boolean",None),("ID",None)] #First(E)={ ! (  CAD ENT boolean id }
        first2 = [("FIN",None)] #Follow(X)={ ; }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 30')
            eTipo=self.E()
            xTipo=eTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 31')
            xTipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta')
        return xTipo

    def A(self):
        first1 = [("PR",2), ("PR",1),  ("PR",3)] #First(T id K)={ boolean int string }
        first2 = [("PARR",None)] #Follow(A)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 32')
            tTipo=self.T()
            pos = self.sigToken[1]
            self.equiparaToken(("ID",None))
            self.ts.insertaTipoTS(pos, ('arg',tTipo)) #
            self.ts.insertaDespTS(pos, tTipo)
            kTipo=self.K()
            if(kTipo is 'tipo_vacio'):
                aTipo = [tTipo]
            else:
                kTipo.insert(0,tTipo)
                aTipo = kTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 33')
            aTipo=['tipo_vacio']
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. Parametros formales de declaracion de funcion incorrectos.')
        return aTipo

    def K(self):
        first1 = [("COM",None)] #First(, T id K)={ , }
        first2 = [("PARR",None)] #Follow(K)={ ) }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 34')
            self.equiparaToken(("COM",None))
            tTipo=self.T()
            pos = self.sigToken[1]
            self.equiparaToken(("ID",None))
            self.ts.insertaTipoTS(pos,('arg',tTipo))
            self.ts.insertaDespTS(pos,tTipo)
            k1Tipo = self.K()
            if(k1Tipo is 'tipo_vacio'):
                kTipo = [tTipo]
            else:
                k1Tipo.insert(0,tTipo)
                kTipo = k1Tipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 35')
            kTipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta. Parametros formales de declaracion de funcion incorrectos.')
        return kTipo

    def E(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None), ("ENT",None), ("boolean",None),("ID",None)]#First(R E')={ ! (  CAD ENT boolean id }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 36')
            rTipo=self.R()
            e_Tipo=self.E_()
            if e_Tipo == 'tipo_vacio':
                eTipo=rTipo
            elif e_Tipo == 'boolean' and rTipo=='int':  
                eTipo='boolean'
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': expresion incorrecta')
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return eTipo

    def E_(self):
        first1 = [("EQU",None)] #First(== R E')={ == }
        first2 = [("NOTEQU",None)] #First(!= R E')={ != }
        first3 = [("PARR",None),("COM",None),("FIN",None)] #Follow(E')={ ) , ; }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 37')
            self.equiparaToken(("EQU",None))
            rTipo=self.R()
            e1_Tipo=self.E_()
            if(rTipo == 'int' and e1_Tipo in  'tipo_vacio'):
                e_Tipo='boolean'
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': el operador logico OR debe tener operandos booleanos.')
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 38')
            self.equiparaToken(("NOTEQU",None))
            rTipo=self.R()
            e1_Tipo=self.E_()
            if(rTipo == 'int' and e1_Tipo in  'tipo_vacio'):
                e_Tipo='boolean'
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': el operador logico OR debe tener operandos booleanos.')
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 39')
            e_Tipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return e_Tipo

    def R(self):
        first1 = [("NOT",None),("PARL",None),("CAD",None),("ENT",None),("boolean",None),("ID",None)] #First(U R')={ ! ( CAD ENT boolean id }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 40')
            uTipo=self.U()
            r_Tipo=self.R_()
            if r_Tipo =='tipo_vacio':
                rTipo = uTipo
            elif r_Tipo =='int' and uTipo == 'int':
                rTipo = 'int'
            else:
                 raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': expresion incorrecta')
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return rTipo

    def R_(self):
        first1 = [("SUM",None)] #First(+ U R') = { + }
        first2 = [ ("NOTEQU",None), ("PARR",None), ("COM",None), ("FIN",None),("EQU",None)] #Follow(R')={ != ) , ; == }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 41')
            self.equiparaToken(("SUM",None))
            uTipo=self.U()
            r1_Tipo=self.R_()
            if (uTipo=='int' and r1_Tipo in ['int', 'tipo_vacio']):
                r_Tipo='int'
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': el operador SUM debe tener operandos enteros.')   
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 42')          
            r_Tipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return r_Tipo

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
            u1_Tipo=self.U()
            if u1_Tipo is 'boolean':
                uTipo = 'boolean'
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': el operador unario logico \'!\'(NOT) debe un operando booleano.')
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 44')
            pos = self.sigToken[1]
            tipoID = self.ts.buscaTipo(pos)
            self.equiparaToken(("ID",None))
            u_Tipo=self.U_()
            if u_Tipo == 'tipo_vacio': #pp2
                uTipo=tipoID[1]
            elif tipoID[0] is 'function':
                if tipoID[1][0] == u_Tipo:
                    uTipo=tipoID[1][1]
                else:
                    raise Exception('ERROR Semantico en linea '+  str(self.lx.lexer.lineno) +': llamada a función que pide '+str(tipoID[1][0])+ ' con parámetro incorrectos'+str(u_Tipo))
            else:
                raise Exception('ERROR Semantico en linea '+ str(self.lx.lexer.lineno) +': expresion incorrecta' +u_Tipo)
        elif (self.tokenInFirst(first3)):
            self.fichParse.write(' 45')
            self.equiparaToken(("PARL",None))
            eTipo=self.E()
            self.equiparaToken(("PARR",None))
            uTipo=eTipo
        elif (self.tokenInFirst(first4)):
            self.fichParse.write(' 46')
            self.equiparaToken(("ENT",None))
            uTipo='int'
        elif (self.tokenInFirst(first5)):
            self.fichParse.write(' 47')
            self.equiparaToken(("CAD",None))
            uTipo='string'
        elif (self.tokenInFirst(first6)):
            self.fichParse.write(' 48')
            self.equiparaToken(("boolean",None))
            uTipo='boolean'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return uTipo

    def U_(self): 
        first1 = [("PARL",None)] # First(( L ))={ ( }
        first2 = [("NOTEQU",None), ("PARR",None), ("SUM",None), ("NOTEQU",None), ("COM",None), ("FIN",None), ("EQU",None)] #Follow(U')={ != ) + , ; == }
        if (self.tokenInFirst(first1)):
            self.fichParse.write(' 49')
            self.equiparaToken(("PARL",None))
            lTipo=self.L()
            self.equiparaToken(("PARR",None))
            u_Tipo=lTipo
        elif (self.tokenInFirst(first2)):
            self.fichParse.write(' 50')
            u_Tipo='tipo_vacio'
        else:
            raise Exception('ERROR Sintactico en linea '+ str(self.lx.lexer.lineno) +': sintaxis incorrecta: Expresion mal construida.')
        return u_Tipo

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
            raise Exception('ERROR Sintactico en linea'+ str(self.lx.lexer.lineno)+':  token recibido '+self.sigToken[0]+' distinto al esperado '+self.sigToken[1]+'.')

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
