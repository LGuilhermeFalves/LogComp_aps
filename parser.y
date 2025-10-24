%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern int yyparse();
extern FILE *yyin;
extern int line_num;

void yyerror(const char *s);
%}

%union {
    double number;
    char *string;
}

/* Token declarations */
%token <string> NAME STRING
%token <number> NUMBER

/* Keywords */
%token SE SENAO ENQUANTO MOSTRAR
%token ANDAR ASPIRAR VOLTARBASE CARREGAR ESPERAR
%token BATERIA SUJEIRA POSX POSY ESTANOBASE OBSTACULO

/* Operators */
%token EQ NE LT LE GT GE
%token ASSIGN PLUS MINUS MULT DIV

/* Delimiters */
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON COMMA

/* Precedence and associativity */
%left EQ NE
%left LT LE GT GE
%left PLUS MINUS
%left MULT DIV
%right UMINUS

%%

/* GERAL */
program:
    statements
    { printf("Análise sintática concluída com sucesso!\n"); }
    ;

statements:
    statement
    | statements statement
    ;

statement:
    compound_stmt
    | simple_stmt
    ;

compound_stmt:
    if_stmt
    | while_stmt
    | block
    ;

simple_stmt:
    assign_stmt
    | action_stmt
    | print_stmt
    | SEMICOLON
    ;

/* INSTRUÇÕES SIMPLES */

assign_stmt:
    NAME ASSIGN expr SEMICOLON
    { printf("Atribuição: %s = <expressão>\n", $1); free($1); }
    ;

print_stmt:
    MOSTRAR LPAREN expr RPAREN SEMICOLON
    { printf("Comando mostrar: <expressão>\n"); }
    | MOSTRAR LPAREN STRING RPAREN SEMICOLON
    { printf("Comando mostrar: %s\n", $3); free($3); }
    ;

/* AÇÕES DO ROBÔ */

action_stmt:
    move_stmt
    | clean_stmt
    | dock_stmt
    | charge_stmt
    | wait_stmt
    ;

move_stmt:
    ANDAR LPAREN RPAREN SEMICOLON
    { printf("Comando andar sem parâmetros\n"); }
    | ANDAR LPAREN expr COMMA expr RPAREN SEMICOLON
    { printf("Comando andar com parâmetros\n"); }
    | ANDAR LPAREN expr RPAREN SEMICOLON
    { printf("Comando andar com um parâmetro\n"); }
    | ANDAR LPAREN COMMA expr RPAREN SEMICOLON
    { printf("Comando andar com segundo parâmetro\n"); }
    ;

clean_stmt:
    ASPIRAR LPAREN RPAREN SEMICOLON
    { printf("Comando aspirar sem parâmetros\n"); }
    | ASPIRAR LPAREN expr RPAREN SEMICOLON
    { printf("Comando aspirar com parâmetros\n"); }
    ;

dock_stmt:
    VOLTARBASE LPAREN RPAREN SEMICOLON
    { printf("Comando voltarBase\n"); }
    ;

charge_stmt:
    CARREGAR LPAREN RPAREN SEMICOLON
    { printf("Comando carregar\n"); }
    ;

wait_stmt:
    ESPERAR LPAREN expr RPAREN SEMICOLON
    { printf("Comando esperar\n"); }
    ;

/* INSTRUÇÕES COMPOSTAS */

if_stmt:
    SE LPAREN expr RPAREN statement
    { printf("Condicional se\n"); }
    | SE LPAREN expr RPAREN statement SENAO statement
    { printf("Condicional se-senao\n"); }
    ;

while_stmt:
    ENQUANTO LPAREN expr RPAREN statement
    { printf("Loop enquanto\n"); }
    ;

block:
    LBRACE statements RBRACE
    { printf("Bloco de comandos\n"); }
    | LBRACE RBRACE
    { printf("Bloco vazio\n"); }
    ;

/* EXPRESSÕES */

expr:
    equality
    ;

equality:
    relational
    | equality EQ relational
    { printf("Operação de igualdade ==\n"); }
    | equality NE relational
    { printf("Operação de diferença !=\n"); }
    ;

relational:
    additive
    | relational LT additive
    { printf("Operação relacional <\n"); }
    | relational LE additive
    { printf("Operação relacional <=\n"); }
    | relational GT additive
    { printf("Operação relacional >\n"); }
    | relational GE additive
    { printf("Operação relacional >=\n"); }
    ;

additive:
    term
    | additive PLUS term
    { printf("Operação de adição +\n"); }
    | additive MINUS term
    { printf("Operação de subtração -\n"); }
    ;

term:
    factor
    | term MULT factor
    { printf("Operação de multiplicação *\n"); }
    | term DIV factor
    { printf("Operação de divisão /\n"); }
    ;

factor:
    primary
    | MINUS primary %prec UMINUS
    { printf("Negação unária -\n"); }
    ;

primary:
    NAME
    { printf("Variável: %s\n", $1); free($1); }
    | NUMBER
    { printf("Número: %f\n", $1); }
    | STRING
    { printf("String: %s\n", $1); free($1); }
    | LPAREN expr RPAREN
    { printf("Expressão entre parênteses\n"); }
    | BATERIA LPAREN RPAREN
    { printf("Sensor: bateria()\n"); }
    | SUJEIRA LPAREN RPAREN
    { printf("Sensor: sujeira()\n"); }
    | POSX LPAREN RPAREN
    { printf("Sensor: posX()\n"); }
    | POSY LPAREN RPAREN
    { printf("Sensor: posY()\n"); }
    | ESTANOBASE LPAREN RPAREN
    { printf("Sensor: estaNoBase()\n"); }
    | OBSTACULO LPAREN RPAREN
    { printf("Sensor: obstaculo()\n"); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe na linha %d: %s\n", line_num, s);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Erro ao abrir o arquivo: %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    } else {
        printf("Uso: %s <arquivo.robo>\n", argv[0]);
        printf("Ou entre com o código (termine com Ctrl+D):\n");
        yyin = stdin;
    }

    int result = yyparse();
    
    if (argc > 1) {
        fclose(yyin);
    }

    return result;
}
