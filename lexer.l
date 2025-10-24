%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"

int line_num = 1;
%}

%option noyywrap

%%

[ \t]+              { }
\n                  { line_num++; }
"//".*              { }

"se"                { return SE; }
"senao"             { return SENAO; }
"enquanto"          { return ENQUANTO; }
"mostrar"           { return MOSTRAR; }
"andar"             { return ANDAR; }
"aspirar"           { return ASPIRAR; }
"voltarBase"        { return VOLTARBASE; }
"carregar"          { return CARREGAR; }
"esperar"           { return ESPERAR; }
"bateria"           { return BATERIA; }
"sujeira"           { return SUJEIRA; }
"posX"              { return POSX; }
"posY"              { return POSY; }
"estaNoBase"        { return ESTANOBASE; }
"obstaculo"         { return OBSTACULO; }

"=="                { return EQ; }
"!="                { return NE; }
"<="                { return LE; }
">="                { return GE; }
"<"                 { return LT; }
">"                 { return GT; }
"="                 { return ASSIGN; }

"+"                 { return PLUS; }
"-"                 { return MINUS; }
"*"                 { return MULT; }
"/"                 { return DIV; }

"("                 { return LPAREN; }
")"                 { return RPAREN; }
"{"                 { return LBRACE; }
"}"                 { return RBRACE; }
";"                 { return SEMICOLON; }
","                 { return COMMA; }

[a-zA-Z][a-zA-Z0-9_]*   { 
                            yylval.string = strdup(yytext); 
                            return NAME; 
                        }

[0-9]+("."[0-9]+)?      { 
                            yylval.number = atof(yytext); 
                            return NUMBER; 
                        }

\"[^\"]*\"              { 
                            yylval.string = strdup(yytext); 
                            return STRING; 
                        }

.                       { 
                            fprintf(stderr, "Erro léxico: caractere desconhecido '%s' na linha %d\n", yytext, line_num); 
                            return yytext[0];
                        }

%%
