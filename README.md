# RoboLang
Linguagem que permite programar o comportamento de um robô aspirador de pó

EBNF


program: [statements] ENDMARKER

# GERAL
# ==================

statements: statement+ 

statement:
    | compound_stmt
    | simple_stmt

compound_stmt:
    | if_stmt
    | while_stmt
    | block

simple_stmt:
    | assign_stmt
    | action_stmt
    | print_stmt
    | ';'

# SINSTRUÇÕES SIMPLES
# =================

assign_stmt:
    | NAME "=" expr

print_stmt:
    | "mostrar" "(" (expr | STRING) ")"

# ROBOT ACTIONS
# =============

action_stmt:
    | move_stmt
    | clean_stmt
    | dock_stmt
    | charge_stmt
    | wait_stmt

move_stmt:
    | "andar" "(" [expr] "," [expr] ")"   # opcional: dx, dy ou velocidade

clean_stmt:
    | "aspirar" "(" [expr] ")"           # opcional: intensidade/tempo

dock_stmt:
    | "voltarBase" "(" ")"

charge_stmt:
    | "carregar" "(" ")"

wait_stmt:
    | "esperar" "(" expr ")"

# INSTRUÇÕES COMPOSTAS
# ===================

if_stmt:
    | "se" "(" expr ")" statement ["senao" statement]

while_stmt:
    | "enquanto" "(" expr ")" statement

block:
    | "{" statements "}"

# EXPRESSÕES
# ===========

expr: equality

equality:
    | relational (("==" | "!=") relational)*

relational:
    | additive (("<" | "<=" | ">" | ">=") additive)*

additive:
    | term (("+" | "-") term)*

term:
    | factor (("*" | "/") factor)*

factor:
    | ["-"] primary

primary:
    | NAME
    | NUMBER
    | STRING
    | "(" expr ")"
    | "bateria" "(" ")"
    | "sujeira" "(" ")"
    | "posX" "(" ")"
    | "posY" "(" ")"
    | "estaNoBase" "(" ")"
    | "obstaculo" "(" ")"

# LEÉXICO
# ==============

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+/
STRING: /"[^"]*"/




