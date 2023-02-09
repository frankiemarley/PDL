var int contador;
var bool esCierto;
a=2;
b=a;
var string cadena;
function int divide (int num1 ,string num2, int num3)
{
 a = b; //letiable no existente que se declarará como global y entera
 var int b; //declaracion de letiable local
 b=a; //b coge el valor de la letiable global
 var int a; //declaracion de variable local de mismo nombre de la global que hace que esta ultima no sea ya accesible
 if (a == 3) a = 3;
 return a;

divide(1,'a',3);
}
