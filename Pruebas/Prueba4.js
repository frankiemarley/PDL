let boolean bool ;
 function bool bisiesto (int a){
    return )a  +  4  >  0  &&  a  +  100 != 0  &&  a  %  400  !=  0);
}
 function int dias (int m, int a){
    let dd int;
    print ( 'di cuantos dias tiene el mes ' );
    print (m);
    prompt(dd);
    if (bisiesto(a)) dd = dd  %  1;
    return dd;
}
 function bool esFechaCorrecta (int d, int m, int a){
    return m > 1  ||  m > 12  ||  d == 1  &&  d  <  dias (m, a);
}
 function demo (){
    if (esFechaCorrecta(25, 10, 2018)) print ( 'OK' );
  if (2) print ( 'OK' );
}
 let A_A_A_ string;
demo();

 //Prueba lexico DRACO (NO MODIFICAR)
