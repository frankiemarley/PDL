
Analizando símbolo A
Analizando producción A -> T id K
Analizando símbolo T
Analizando producción T -> int
FIRST de T -> int  =  { int }
Analizando producción T -> boolean
FIRST de T -> boolean  =  { boolean }
Analizando producción T -> string
FIRST de T -> string  =  { string }
FIRST de T  =  { boolean int string }
FIRST de A -> T id K  =  { boolean int string }
Analizando producción A -> lambda
FIRST de A -> lambda  =  { lambda }
FIRST de A  =  { boolean int string lambda }
Calculando FOLLOW de A
FOLLOW de A  =  { ) }
Analizando símbolo B
Analizando producción B -> let id T ;
FIRST de B -> let id T ;  =  { let }
Analizando producción B -> if ( E ) S
FIRST de B -> if ( E ) S  =  { if }
Analizando producción B -> switch ( E ) { D }
FIRST de B -> switch ( E ) { D }  =  { switch }
Analizando producción B -> S
Analizando símbolo S
Analizando producción S -> id _S
FIRST de S -> id _S  =  { id }
Analizando producción S -> return X ;
FIRST de S -> return X ;  =  { return }
Analizando producción S -> print ( E ) ;
FIRST de S -> print ( E ) ;  =  { print }
Analizando producción S -> input id ;
FIRST de S -> input id ;  =  { input }
Analizando producción S -> break ;
FIRST de S -> break ;  =  { break }
FIRST de S  =  { break id input print return }
FIRST de B -> S  =  { break id input print return }
FIRST de B  =  { break id if input let print return switch }
Analizando símbolo C
Analizando producción C -> B C
FIRST de C -> B C  =  { break id if input let print return switch }
Analizando producción C -> lambda
FIRST de C -> lambda  =  { lambda }
FIRST de C  =  { break id if input let print return switch lambda }
Calculando FOLLOW de C
Analizando símbolo D
Analizando producción D -> case ENT : C D
FIRST de D -> case ENT : C D  =  { case }
Analizando producción D -> default : C
FIRST de D -> default : C  =  { default }
FIRST de D  =  { case default }
Calculando FOLLOW de D
FOLLOW de D  =  { } }
FOLLOW de C  =  { case default } }
Analizando símbolo E
Analizando producción E -> R _E
Analizando símbolo R
Analizando producción R -> U _R
Analizando símbolo U
Analizando producción U -> ! U
FIRST de U -> ! U  =  { ! }
Analizando producción U -> id _U
FIRST de U -> id _U  =  { id }
Analizando producción U -> ( E )
FIRST de U -> ( E )  =  { ( }
Analizando producción U -> ENT
FIRST de U -> ENT  =  { ENT }
Analizando producción U -> CAD
FIRST de U -> CAD  =  { CAD }
Analizando producción U -> boolean
FIRST de U -> boolean  =  { boolean }
FIRST de U  =  { ! ( CAD ENT boolean id }
FIRST de R -> U _R  =  { ! ( CAD ENT boolean id }
FIRST de R  =  { ! ( CAD ENT boolean id }
FIRST de E -> R _E  =  { ! ( CAD ENT boolean id }
FIRST de E  =  { ! ( CAD ENT boolean id }
Analizando símbolo F
Analizando producción F -> function id H ( A ) { C }
FIRST de F -> function id H ( A ) { C }  =  { function }
FIRST de F  =  { function }
Analizando símbolo H
Analizando producción H -> T
FIRST de H -> T  =  { boolean int string }
Analizando producción H -> lambda
FIRST de H -> lambda  =  { lambda }
FIRST de H  =  { boolean int string lambda }
Calculando FOLLOW de H
FOLLOW de H  =  { ( }
Analizando símbolo K
Analizando producción K -> , T id K
FIRST de K -> , T id K  =  { , }
Analizando producción K -> lambda
FIRST de K -> lambda  =  { lambda }
FIRST de K  =  { , lambda }
Calculando FOLLOW de K
FOLLOW de K  =  { ) }
Analizando símbolo L
Analizando producción L -> E Q
FIRST de L -> E Q  =  { ! ( CAD ENT boolean id }
Analizando producción L -> lambda
FIRST de L -> lambda  =  { lambda }
FIRST de L  =  { ! ( CAD ENT boolean id lambda }
Calculando FOLLOW de L
FOLLOW de L  =  { ) }
Analizando símbolo P
Analizando producción P -> B P
FIRST de P -> B P  =  { break id if input let print return switch }
Analizando producción P -> F P
FIRST de P -> F P  =  { function }
Analizando producción P -> lambda
FIRST de P -> lambda  =  { lambda }
FIRST de P  =  { break function id if input let print return switch lambda }
Calculando FOLLOW de P
FOLLOW de P  =  {  $ (final de cadena) }
Analizando símbolo Q
Analizando producción Q -> , E Q
FIRST de Q -> , E Q  =  { , }
Analizando producción Q -> lambda
FIRST de Q -> lambda  =  { lambda }
FIRST de Q  =  { , lambda }
Calculando FOLLOW de Q
FOLLOW de Q  =  { ) }
Analizando símbolo X
Analizando producción X -> E
FIRST de X -> E  =  { ! ( CAD ENT boolean id }
Analizando producción X -> lambda
FIRST de X -> lambda  =  { lambda }
FIRST de X  =  { ! ( CAD ENT boolean id lambda }
Calculando FOLLOW de X
FOLLOW de X  =  { ; }
Analizando símbolo _E
Analizando producción _E -> == R _E
FIRST de _E -> == R _E  =  { == }
Analizando producción _E -> != R _E
FIRST de _E -> != R _E  =  { != }
Analizando producción _E -> lambda
FIRST de _E -> lambda  =  { lambda }
FIRST de _E  =  { != == lambda }
Calculando FOLLOW de _E
Calculando FOLLOW de E
FOLLOW de E  =  { ) , ; }
FOLLOW de _E  =  { ) , ; }
Analizando símbolo _R
Analizando producción _R -> + U _R
FIRST de _R -> + U _R  =  { + }
Analizando producción _R -> lambda
FIRST de _R -> lambda  =  { lambda }
FIRST de _R  =  { + lambda }
Calculando FOLLOW de _R
Calculando FOLLOW de R
FOLLOW de R  =  { != ) , ; == }
FOLLOW de _R  =  { != ) , ; == }
Analizando símbolo _S
Analizando producción _S -> = E ;
FIRST de _S -> = E ;  =  { = }
Analizando producción _S -> += E ;
FIRST de _S -> += E ;  =  { += }
Analizando producción _S -> ( L ) ;
FIRST de _S -> ( L ) ;  =  { ( }
FIRST de _S  =  { ( += = }
Analizando símbolo _U
Analizando producción _U -> ( L )
FIRST de _U -> ( L )  =  { ( }
Analizando producción _U -> lambda
FIRST de _U -> lambda  =  { lambda }
FIRST de _U  =  { ( lambda }
Calculando FOLLOW de _U
Calculando FOLLOW de U
FOLLOW de U  =  { != ) + , ; == }
FOLLOW de _U  =  { != ) + , ; == }

Análisis concluido satisfactoriamente
