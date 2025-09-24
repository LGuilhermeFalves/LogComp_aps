# LogComp_aps
Linguagem que permite programar o comportamento de um robô aspirador de pó

EBNF

programa = { comando } ;

comando = atribuicao | se | enquanto | acao | imprimir ;

atribuicao = "coloque" identificador ":=" expressao ;
se = "se" condicao "entao" { comando } "fim" ;
enquanto = "enquanto" condicao "faca" { comando } "fim" ;

acao = "andar" | "aspirar" | "voltarBase" | "carregar" ;
imprimir = "mostrar expressao" ;

condicao = expressao operador expressao ;
expressao = numero | identificador ;
operador = "=" | "<" | ">" ;

identificador = letra { letra | digito } ;
numero = digito { digito } ;
letra = "a" | … | "z" ;
digito = "0" | … | "9" ;



