print("Des ");

Proc P;
    if(st ϵ First(B P)={ break id if print return switch let }) then{
        print("1");
        B();
        P();
    }
    else if(st ϵ First(F P)={ function }) then{
        print("2");
        F();
        P();
    }
    else if(st ϵ Follow(P)={ $ }){
        print("3");
    }
    else ERROR;
END;

Proc B;
    if(st ϵ First(let id T ;)={ let }) then{
        print("4");
        EqT(let);
        EqT(id);
        T();
        EqT(;);
    }
    else if(st ϵ First(if ( E ) S)={ if }) then{
        print("5");
        EqT(if);
        EqT(();
        E();
        EqT());
        S();
    }
    else if(st ϵ First(switch ( E ) { D })={ switch }) then{
        print("6");
        EqT(switch);
        EqT(();
        E();
        EqT());
        EqT({);
        D();
        EqT(});
    }
    else if(st ϵ First(S)={ break id print return }) then{
        print("7");
        S();
    }
    else ERROR;
END;

Proc C;
    if(st ϵ First(B C)={ break id if print return switch let }) then{
        print("8");
        B();
        C();
    }
    else if(st ϵ Follow(C)={ case } default }) then{
        print("9");
    }
    else ERROR;
END;

Proc D;
    if(st ϵ First(case ENT : C D)={ case }) then{
        print("10");
        EqT(case);
        EqT(ENT);
        EqT(:);
        C();
        D();
    }
    else if(st ϵ First(default : C)={ default } ) then{
        print("11");
        EqT(default);
        EqT(:);
        C();
    }
    else ERROR;
END;

Proc T;
    if(st ϵ First(int)={ int }) then{
        print("12");
        EqT(int);
    }
    else if(st ϵ First(bool)={ bool }) then{
        print("13");
        EqT(bool);
    }
    else if(st ϵ First(string)={ string }) then{
        print("14");
        EqT(string);
    }
    else ERROR;
END;

Proc F;
    if(st ϵ First(function id H ( A ) { C })={ function }) then{
        print("15");
        EqT(function);
        EqT(id);
        H();
        EqT(();
        A();
        EqT());
        EqT({);
        C();
        EqT(});
    }
    else ERROR;
END;

Proc S;
    if(st ϵ First(id S')={ id }) then{
        print("16");
        EqT(id);
        S'();
    }
    else if(st ϵ First(return X ;)={ return }) then{
        print("17");
        EqT(return);
        X();
        EqT(;);
    }
    else if(st ϵ First(print E ;)={ print }) then{
        print("18");
        EqT(print);
        E(); 
        EqT(;);
    }
    else if(st ϵ First(input id ;)={ input }) then{
        print("19");
        EqT(input);
        EqT(id);
        EqT(;);
    }
    else if(st ϵ First( break ;)={ break }) then{
        print("20");
        EqT(break);
        EqT(;);
    }
    else ERROR;
END;

Proc S';
    if(st ϵ First(= E ;)={ = }) then{
        print("21");
        EqT(=);
        E();
        EqT(;);
    }
    else if(st ϵ First(+= E ;)={ += }) then{
        print("22");
        EqT(+=);
        E();
        EqT(;);
    }
    else if(st ϵ First(( L ) ;)={ ( }) then{
        print("23");
        EqT(();
        L();
        EqT());
        EqT(;);
    }
    else ERROR;
END;

Proc H;
    if(st ϵ First(T)={ int bool string }) then{
        print("24");
        T();
    }
    else if(st ϵ Follow(H)={ id }) then{
        print("25");
    }
    else ERROR;
END;

Proc L;
    if(st ϵ First(E Q)={ ! ( boolean CAD ENT id )}) then{
        print("26");
        E();
        Q();
    }
    else if(st ϵ Follow(L)={ ) }) then{
        print("27");
    }
    else ERROR;
END;

Proc Q;
    if(st ϵ First(, E Q)={ , }) then{
        print("28");
        EqT(,);
        E();
        Q();
    }
    else if(st ϵ Follow(Q)={ ) }) then{
        print("29");
    }
    else ERROR;
END;

Proc X;
    if(st ϵ First(E)={ ! ( boolean CAD ENT id )}) then{
        print("30");
        E();
    }
    else if(st ϵ Follow(X)={ ; }) then{
        print("31");
    }
    else ERROR;
END;

Proc A;
    if(st ϵ First(T id K)={ int bool string }) then{
        print("32");
        T();
        EqT(id);
        K();
    }
    else if(st ϵ Follow(A)={ ) ; }) then{
        print("33");
    }
    else ERROR;
END;

Proc K;
    if(st ϵ First(, T id K)={ , }) then{
        print("34");
        EqT(,);
        T();
        EqT(id);
        K();
    }
    else if(st ϵ Follow(K)={ ) }) then{
        print("35");
    }
    else ERROR;
END;.

Proc E;
    if(st ϵ First(R E')={ ! ( boolean CAD ENT id }) then{
        print("36");
        R();
        E'();
    }
    else ERROR;
END;

Proc E';
    if(st ϵ First(== R E')={ == }) then{
        print("37");
        EqT(==);
        R();
        E'();
    }
    if(st ϵ First(!= R E')={ != }) then{
        print("38");
        EqT(!=);
        R();
        E'();
    }
    else if(st ϵ Follow(E')={ ) , ; }) then{
        print("39");
    }
    else ERROR;
END;

Proc R;
    if(st ϵ First(U R')={ ! ( boolean CAD ENT id }) then{
    print("40");
    U();
    R'();
    }
    else ERROR;
END;

Proc R';
    if(st ϵ First(+ U R')={ + }) then{
        print("41");
        EqT(+);
        U();
        R'();
    }
    else if(st ϵ Follow(R')={ ) , ; || }) then{
        print("42");
    }
    else ERROR;
END;

Proc U;
    if(st ϵ First(! U)={ ! }) then{
        print("43");
        EqT(!);
        U();
    }
        
    else if(st ϵ First(id U')={ id }) then{
        print("44");
        EqT(id);
        U'();
    }
    else if(st ϵ First(( E ))={ ( }) then{
        print("45");
        EqT(();
        E();
        EqT());
    }
    else if(st ϵ First(ENT)={ ENT }) then{
        print("46");
        EqT(ENT);
    }
    else if(st ϵ First(CAD)={ CAD }) then{
        print("47");
        EqT(CAD);
    }
    else if(st ϵ First(BOOLEAN)={ BOOLEAN }) then{
        print("48");
        EqT(BOOLEAN);
    }
    else ERROR;
END;

Proc U';
    if(st ϵ First(( L ))={ ( }) then{
        print("49");
        EqT(();
        L();
        EqT());
    }
    else if(st ϵ Follow(W')={ != % && ) * + , - / ; < == > || }) then{
        print("50");
    }
    else ERROR;
END;

